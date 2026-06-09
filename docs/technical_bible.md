# TECHNICAL BIBLE: SIMSMERGED METROPOLIS (v1.4.2)
*Axiomatic Governance & High-Performance Orchestration*

## 1. Executive Summary
This document serves as the absolute, non-negotiable architectural reference for SimAgentCity. It defines the constraints, protocols, and mechanisms that govern the autonomous swarm.

## 2. Axioms
1. **ADD-ONLY PERSISTENCY:** No destructive operations.
2. **DETERMINISTIC SERIALIZATION:** Every task state is persisted.
3. **MATHEMATICAL GOVERNANCE:** Resource allocation via Algebraic harmonic pacing.

## 3. Communication Bus (Symphony-Bus)
The communication backbone is an asynchronous `SymphonyBus` (PubSub pattern).
- **Backend:** `message_bus.py` broadcasts events to WebSocket clients.
- **Frontend:** `bridge.js` implements a persistent WebSocket listener and a secondary polling fallback.

## 4. Agent Anatomy (The Actor-Observer Pattern)
- **Actor:** Performs task execution within fenced subprocesses.
- **Observer:** Telemetry agent handling all logging to `briefcase/` and broadcasting via `SymphonyBus`.

## 5. DePIN Treasury
- **Sprite Tokenomics:** Mints tokens proportional to system hardware (CPU/IO) load.
- **Ledger:** Cryptographically audited blockchain ledger stored in `blockchain_ledger.json`.

---
*TIMESTAMP: 2026-06-08T12:05:00Z*
