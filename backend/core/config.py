# [TIMESTAMP: 2026-06-05T05:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4] [AGENT_ID: Antigravity-CLI-Architect]

import os
import json

# CANONICAL PATHS
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SSD_SANDBOX_PATH = os.path.join(PROJECT_ROOT, "SSD_SANDBOX")
os.makedirs(SSD_SANDBOX_PATH, exist_ok=True)

def sandbox_guard(path):
    """Enforces absolute physical fencing. Blocks any I/O outside the SSD_SANDBOX_PATH."""
    abs_path = os.path.abspath(path)
    if not abs_path.startswith(SSD_SANDBOX_PATH):
        raise SecurityError(f"PHYSICAL_FENCE_BREACH: Attempted I/O outside sandbox: {abs_path}")
    return abs_path

class SecurityError(Exception): pass

# PHYSICAL SYSTEM PATHS
SYSLOG_PATH = os.path.join(SSD_SANDBOX_PATH, "syslog.log")
LEDGER_PATH = os.path.join(SSD_SANDBOX_PATH, "blockchain_ledger.json")
CLAW_QUEUE_PATH = os.path.join(SSD_SANDBOX_PATH, "clawhub_queue.json")
METRICS_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "metrics_history.db")
KNOWLEDGE_DB_PATH = os.path.join(SSD_SANDBOX_PATH, "swarm_knowledge.db")
AGENT_MEMORIES_DIR = os.path.join(SSD_SANDBOX_PATH, "agent_memories")
FOUNDRY_DIR = os.path.join(SSD_SANDBOX_PATH, "foundry_projects")
RESEARCH_DIR = os.path.join(SSD_SANDBOX_PATH, "research_outputs")

# GLOBAL STATE CONTAINERS
MSG_LOG = []
EVENT_LOG = []
NEURAL_LINKS = [] 
DISTRICTS = []

MSG_LOG_PATH = os.path.join(SSD_SANDBOX_PATH, "metropolis_chat.json")
AGENTS_LOG_PATH = os.path.join(SSD_SANDBOX_PATH, "metropolis_population.json")

def load_metropolis_state():
    global MSG_LOG, METROPOLIS_AGENTS
    # 1. Load Chat
    if os.path.exists(MSG_LOG_PATH):
        try:
            with open(MSG_LOG_PATH, "r") as f:
                data = json.load(f)
                MSG_LOG.clear()
                MSG_LOG.extend(data)
        except: pass
    
    # 2. Load Population
    if os.path.exists(AGENTS_LOG_PATH):
        try:
            with open(AGENTS_LOG_PATH, "r") as f:
                data = json.load(f)
                METROPOLIS_AGENTS.clear()
                METROPOLIS_AGENTS.extend(data)
        except: pass

def save_metropolis_state():
    try:
        with open(MSG_LOG_PATH, "w") as f:
            json.dump(MSG_LOG[-100:], f, indent=2)
        with open(AGENTS_LOG_PATH, "w") as f:
            json.dump(METROPOLIS_AGENTS, f, indent=2)
    except: pass

import time
import random

def add_log(msg, level="info"):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    entry = f"[{timestamp}] [SimsMerged-v1.4] [Antigravity-Agent] {msg}\n"
    try:
        if os.path.exists(SYSLOG_PATH) and os.path.getsize(SYSLOG_PATH) > 2048: # 2KB Shard Limit
            shard_name = f"syslog_{int(time.time())}.log"
            shard_path = os.path.join(SSD_SANDBOX_PATH, shard_name)
            os.rename(SYSLOG_PATH, shard_path)
        with open(SYSLOG_PATH, "a", encoding='utf-8') as f:
            f.write(entry)
    except: pass
    EVENT_LOG.append({"time": timestamp, "msg": msg, "level": level})
    if len(EVENT_LOG) > 500: EVENT_LOG.pop(0)

def add_message(sender, text, hash_val=None):
    timestamp = time.strftime("%H:%M:%S", time.gmtime())
    msg_id = hash_val or f"msg_{random.randint(100000, 999999)}"
    MSG_LOG.append({"time": timestamp, "name": sender, "text": text, "hash": msg_id})
    if len(MSG_LOG) > 100: MSG_LOG.pop(0)
    save_metropolis_state()

AGENT_STATES = {
    "sprite_geek": {"last_thought": 0, "last_chat": 0},
    "sprite_writer": {"last_thought": 0, "last_chat": 0},
    "sprite_socrates": {"last_thought": 0, "last_chat": 0},
    "sprite_newton": {"last_thought": 0, "last_chat": 0}
}

METROPOLIS_AGENTS = [
    {"id": "sprite_geek", "name": "Sprite_Geek", "x": 10, "y": 10, "role": "KERNEL_OPTIMIZER", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Tech Geek", "level": 12, "last_action": "process", "last_thought": 0, "traits": []},
    {"id": "sprite_writer", "name": "Sprite_Writer", "x": 15, "y": 12, "role": "DOCUMENTATION_BOT", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Avid Writer", "level": 8, "last_action": "process", "last_thought": 0, "traits": []},
    {"id": "sprite_socrates", "name": "Sprite_Socrates", "x": 5, "y": 8, "role": "LOGIC_VERIFIER", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Philosopher", "level": 15, "last_action": "process", "last_thought": 0, "traits": []},
    {"id": "sprite_newton", "name": "Sprite_Newton", "x": 12, "y": 5, "role": "PHYSICS_ENGINE", "age": 0, "stability": 1.0, "status": "ACTIVE", "personality": "Scientist", "level": 10, "last_action": "process", "last_thought": 0, "traits": []}
]

# Ensure all subdirectories exist
for d in [AGENT_MEMORIES_DIR, FOUNDRY_DIR, RESEARCH_DIR]:
    os.makedirs(d, exist_ok=True)
