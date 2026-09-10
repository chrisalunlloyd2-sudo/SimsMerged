# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# [PERFORMATIVE: ATC_COORDINATOR]
# DESCRIPTION: Sector 1.1 - ATC Weather NOTAM Engine (Broadcast Enabled)

import psutil
import time
import logging
import json
import httpx
import asyncio

logger = logging.getLogger("ATC_Tower")
logger.setLevel(logging.INFO)

class ATCCoordinator:
    def __init__(self, chat_url="http://127.0.0.1:8000/api/v1/chat/send"):
        self.chat_url = chat_url
        self.ground_stop_active = False

    def get_weather_report(self):
        """Sector 1: Map CPU/SSD utilization to Weather NOTAMs."""
        cpu = psutil.cpu_percent(interval=None)
        ram = psutil.virtual_memory().percent
        io_wait = psutil.cpu_times().iowait if hasattr(psutil.cpu_times(), 'iowait') else 0.0

        notams = []

        # 1. Wind Shear (CPU)
        if cpu > 40:
            notams.append({
                "type": "WEATHER_NOTAM",
                "code": "WIND_SHEAR",
                "severity": "MODERATE",
                "instruction": "HALVE_THROUGHPUT",
                "msg": f"Wind Shear: CPU at {cpu}%"
            })

        # 2. Runway Icing (SSD Latency)
        if cpu > 70 or io_wait > 0.05:
            notams.append({
                "type": "WEATHER_NOTAM",
                "code": "RUNWAY_ICING",
                "severity": "CRITICAL",
                "instruction": "LOCK_FILE_WRITES",
                "msg": "Runway Icing: SSD Bottleneck."
            })

        # 3. Category 5 Storm (Ground Stop)
        if ram > 85 or cpu > 90:
            notams.append({
                "type": "WEATHER_NOTAM",
                "code": "CAT_5_STORM",
                "severity": "EXTREME",
                "instruction": "GROUND_STOP",
                "msg": "Category 5 Storm: SUSPENDING FLIGHTS."
            })
            self.ground_stop_active = True
        else:
            self.ground_stop_active = False

        return {
            "type": "WEATHER_UPDATE",
            "cpu": cpu,
            "ram": ram,
            "notams": notams,
            "ground_stop": self.ground_stop_active
        }

    async def pulse(self):
        logger.info("ATC Tower active. Broadcasting Weather NOTAMs...")
        async with httpx.AsyncClient() as client:
            while True:
                report = self.get_weather_report()

                try:
                    # Broadcast detailed report for UI
                    await client.post("http://127.0.0.1:8000/api/v1/agent/update", json=report)

                    # If new NOTAMs, post to chat
                    for n in report['notams']:
                        await client.post(self.chat_url, json={
                            "sender_id": "ATC_Tower",
                            "channel": "System",
                            "message": f"[NOTAM] {n['code']}: {n['msg']}"
                        })
                except Exception as e:
                    logger.error(f"ATC Broadcast failed: {e}")

                await asyncio.sleep(2)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tower = ATCCoordinator()
    try:
        asyncio.run(tower.pulse())
    except KeyboardInterrupt:
        logger.info("ATC Tower shutdown.")
