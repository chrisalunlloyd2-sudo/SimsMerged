# [TIMESTAMP: 2026-06-07T22:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import duckdb
import os
import json
import time
from .config import SSD_SANDBOX_PATH

ANALYTICS_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "grid_analytics.duckdb")

class GridAnalytics:
    """
    GRID ANALYTICS (CONTINUOUS AGGREGATES):
    - Uses DuckDB to simulate 'Timescale' continuous aggregates.
    - Performs periodic rollups of grid telemetry (CPU, TP, Stability).
    - Fulfills Step 80 of the Roadmap.
    """
    def __init__(self):
        self.conn = duckdb.connect(ANALYTICS_DB_PATH)
        self._init_db()

    def _init_db(self):
        # 1. Raw Telemetry Table
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS raw_telemetry (
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                cpu_load  DOUBLE,
                tp_balance DOUBLE,
                avg_stability DOUBLE,
                agent_count INTEGER
            )
        ''')
        
        # 2. Daily Aggregates (The 'Continuous Aggregate' simulation)
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS daily_rollups (
                date DATE PRIMARY KEY,
                max_cpu DOUBLE,
                total_tp_gain DOUBLE,
                min_stability DOUBLE
            )
        ''')

    def record_tick(self, cpu, tp, stability, agents):
        """Records a single telemetry tick."""
        self.conn.execute('''
            INSERT INTO raw_telemetry (cpu_load, tp_balance, avg_stability, agent_count)
            VALUES (?, ?, ?, ?)
        ''', (cpu, tp, stability, agents))

    def perform_rollup(self):
        """Manually triggers the 'Timescale' style aggregate rollup."""
        print("[ANALYTICS] Performing grid telemetry rollup...")
        self.conn.execute('''
            INSERT INTO daily_rollups
            SELECT 
                CAST(timestamp AS DATE) as date,
                MAX(cpu_load),
                MAX(tp_balance) - MIN(tp_balance),
                MIN(avg_stability)
            FROM raw_telemetry
            WHERE timestamp > now() - INTERVAL '24 hours'
            GROUP BY 1
            ON CONFLICT (date) DO UPDATE SET
                max_cpu = excluded.max_cpu,
                total_tp_gain = excluded.total_tp_gain,
                min_stability = excluded.min_stability
        ''')
        print("✅ [ANALYTICS] Rollup complete.")

    def get_weekly_trends(self):
        """Returns the last 7 days of performance trends."""
        return self.conn.execute('''
            SELECT * FROM daily_rollups ORDER BY date DESC LIMIT 7
        ''').fetchall()

grid_analytics = GridAnalytics()
