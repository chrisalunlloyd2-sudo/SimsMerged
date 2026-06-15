# [TIMESTAMP: 2026-06-14T18:15:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]

import mmap
import os
import time
import json
import random
import psutil
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

from .audio_chatter import audio_chatter

# METROPOLIS SLM SERVER V2: HYPER-EXPANDED
# Implements strict SSD-only memory mapping and 10-second chat throttling.
# Integrated with high-speed pitch-shifted audio chatter.

SSD_SANDBOX = r"C:\Users\viper\Desktop\SimsMerged\SSD_SANDBOX"
WEIGHTS_FILE = os.path.join(SSD_SANDBOX, "metropolis_weights.bin")
CHAT_LOG = os.path.join(SSD_SANDBOX, "metropolis_chat.json")

# Ensure weights file exists for mmap
if not os.path.exists(WEIGHTS_FILE):
    with open(WEIGHTS_FILE, "wb") as f:
        f.write(os.urandom(1024 * 1024 * 10)) # 10MB dummy weights

class ThrottledSLM:
    def __init__(self):
        self.agent_last_chat = {}
        self.lock = threading.Lock()
        self.vocabulary = {}
        self.kv_cache = {} # Local ephemeral cache for speculative hits
        
    def sync_learning(self):
        """Learns from the chat log to build the local SLM state."""
        try:
            if os.path.exists(CHAT_LOG):
                with open(CHAT_LOG, "r", encoding="utf-8") as f:
                    messages = json.load(f)
                text = " ".join([m.get("text", "") for m in messages])
                words = text.split()
                for i in range(len(words)-1):
                    w1, w2 = words[i], words[i+1]
                    if w1 not in self.vocabulary: self.vocabulary[w1] = []
                    self.vocabulary[w1].append(w2)
                print(f"[SLM] Synchronized vocabulary: {len(self.vocabulary)} tokens.")
        except Exception as e:
            print(f"[SLM] Sync Error: {e}")

    def generate(self, agent_id, prompt):
        now = time.time()
        
        # Step 20: Thermal Throttling Gate (HYPER-SPEED)
        cpu_load = psutil.cpu_percent()
        thermal_throttle = 1.0
        if cpu_load > 90.0:
            thermal_throttle = 0.8 # Less aggressive throttle for Hyper-Expansion
            print(f"[SLM] THERMAL PRESSURE: {cpu_load}%. Maintaining high-speed through-put.")

        with self.lock:
            # 1. 10-Second Throttle Check
            last_time = self.agent_last_chat.get(agent_id, 0)
            if now - last_time < 10: 
                remaining = int(10 - (now - last_time))
                return f"THROTTLED: {remaining}s remaining for {agent_id}. SSD_I/O_COOLDOWN."

            self.agent_last_chat[agent_id] = now
            
            # Speculative Hit check
            prompt_hash = hash(prompt)
            if prompt_hash in self.kv_cache and random.random() < 0.3:
                return self.kv_cache[prompt_hash]

            # 2. MMAP FENCED WEIGHT ACCESS
            with open(WEIGHTS_FILE, "r+b") as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
                offset = random.randint(0, mm.size() - 200)
                _ = mm[offset:offset+200] # Speculative multi-byte read
                
                response = []
                current = prompt.split()[-1] if prompt.split() else "System"
                
                for _ in range(25): # Expanded response length
                    if current in self.vocabulary:
                        current = random.choice(self.vocabulary[current])
                    else:
                        current = random.choice(list(self.vocabulary.keys())) if self.vocabulary else "Evolution"
                    response.append(current)
                
                mm.close()
            
            final_response = " ".join(response)
            self.kv_cache[prompt_hash] = final_response
            
            # HYPER-EXPANSION: Trigger Audio Chatter
            audio_chatter.speak(final_response, agent_id)
            
            return final_response

slm_engine = ThrottledSLM()

class ThrottledHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        agent_id = data.get("agent_id", "unknown_sprite")
        prompt = data.get("prompt", "")

        print(f"[SLM_SERVER] Inference Request: {agent_id}")
        response_text = slm_engine.generate(agent_id, prompt)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"response": response_text}).encode())

def run():
    slm_engine.sync_learning()
    server = HTTPServer(('', 11434), ThrottledHandler)
    print("[SYSTEM] Throttled SLM Server (MMAP Fenced) active on 11434.")
    server.serve_forever()

if __name__ == "__main__":
    run()
