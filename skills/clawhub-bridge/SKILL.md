---
name: clawhub-bridge
description: Bridge for synchronizing the SimAgentCity deterministic database layout with the global OpenClaw (ClawHub) registry. Use when agents need to export local genetic SOPs, task XP, or SLM weights to the decentralized hub or import global behavioral anchors.
---

# ClawHub Bridge Skill

This skill facilitates the bi-directional mapping between the localized **SimAgentCity** deterministic JSON/SQLite database and the **OpenClaw** global registry (**ClawHub**).

## Core Workflows

### 1. Database Mapping
The local database uses a high-fidelity deterministic layout for task parameters, agent XP, and SLM weights.
- **Local Source:** `backend/data/ai_attributes.json`, `agents_population.json`, `blockchain_ledger.json`.
- **Global Target:** ClawHub IPFS-backed JSON schemas.

### 2. Exporting Genetic SOPs
When an agent reaches high XP thresholds, its local weights and task completion SOPs are hashed and queued for ClawHub synchronization.
- **Protocol:** `ClawSync-v1.2`
- **Validation:** Every export must be verified by the local **Bank Monitor** and signed with the agent's private key.

### 3. Importing Global Anchors
Agents query ClawHub for "Golden Path" weights and behavioral heuristics to improve their local stability scores.

## Reference Materials

- [DETERMINISTIC_SCHEMA.md](references/deterministic_schema.md): Detailed mapping of the local JSON fields to ClawHub standards.
- [CLAW_SYNC_PROTOCOL.md](references/claw_sync_protocol.md): Technical spec for the synchronization handshake.

## Tools

- `scripts/bridge_to_clawhub.py`: CLI tool for manual synchronization and integrity checks.
