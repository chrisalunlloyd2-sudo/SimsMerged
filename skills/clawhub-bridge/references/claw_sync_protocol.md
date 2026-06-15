# ClawSync Protocol (v1.2)

## 1. Handshake Sequence
1. **Local Initialization**: Agent generates a `SyncIntent` hash using the `NeuromorphicOrchestrator`.
2. **Registry Verification**: `ClawHub` verifies the city `PROJECT_ID` and the agent's unique `AGENT_ID`.
3. **Atomic Commit**: Data is transferred via a zero-copy buffer to the `ClawHub` ingress.

## 2. Integrity Enforcement
- **ASIC Anchor**: Every sync must be timestamped with a successful Proof-of-Work nonce from the local ASIC hardware loop.
- **Rollback Protocol**: If the hub returns a `SYNC_COLLISION`, the local database enters a **RECOVERY** state to re-align weights.
