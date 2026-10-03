# Orchestrator Map (read-only analysis; no files changed)

| File | Class / entry | Lines | Apparent role |
|------|---------------|-------|---------------|
| `backend/core/orchestrator.py` | `SelfHealingOrchestrator`, `start_orchestrator()` | 85 | Process supervision / self-healing |
| `backend/core/watchdog_orchestrator.py` | `CppServerWatchdog`, `start_orchestration()` | 63 | C++ engine watchdog |
| `backend/core/model_orchestrator.py` | `ModelOrchestrator` | 220 | Local model/SLM routing |
| `backend/core/ml_orchestrator.py` | `MLOrchestrator`, `start_ml_orchestrator_loop()` | 115 | ML loop |
| `backend/core/bm25_orchestrator.py` | `AdvancedBM25Orchestrator`, `DualBM25Scaffolding` | 147 | Retrieval / semantic memory |
| `backend/core/communication_orchestrator.py` | `CommunicationOrchestrator` | 57 | Agent messaging |
| `backend/core/headless_tools/headless_test_orchestrator.py` | `SovereignTestOrchestrator` | 48 | Headless tests |
| `orchestrator.js` (root) | script | 157 | Node-side task loop (uses `database/db_wrapper`, `depin_ledger`) |

Roles above are inferred from names and class headers; verify before relying on them.

## Overlap and suggestion
- Three distinct concerns are bundled under one name: **supervision** (orchestrator, watchdog), **intelligence** (model, ml, bm25) and **coordination** (communication, `orchestrator.js`).
- Proposed single entry point (additive, not yet built): `backend/core/delegation/` as the *coordination* layer, with the supervision and intelligence orchestrators left in place and invoked as bounty workers.
- Duplicate coordination logic: `orchestrator.js` and `communication_orchestrator.py` should eventually read the same `bounties/` queue.
