# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Configuration for the Sprite Triplet Subsystem (Phase 1)

import os

class TripletConfig:
    # Ollama Concurrent Port Mappings
    OLLAMA_PORTS = {
        "L1_MASTER": int(os.getenv("OLLAMA_PORT_L1", 11434)),
        "L2_ORCHESTRATOR": int(os.getenv("OLLAMA_PORT_L2", 11435)),
        "L3_SMOLL": int(os.getenv("OLLAMA_PORT_L3", 11436)),
    }

    # Model Parameters
    MODELS = {
        "L1_MASTER": "qwen:500m",  # Drives the Tok Tree Macro Commands
        "L2_ORCHESTRATOR": "qwen:250m",  # Uses BM25 RAG & translates to procedural steps
        "L3_SMOLL": "qwen:135m"  # Directly interfaces with Mock IDE
    }

    # API Rate Limiting & Context
    RATE_LIMIT_DELAY = 1.0  # Base delay in seconds
    L2_CONTEXT_LIMIT = 4096
    L3_CONTEXT_LIMIT = 2048

    # Synthetic IDE Endpoint
    MOCK_IDE_URL = "http://127.0.0.1:8001/api/v1/ide/submit"
