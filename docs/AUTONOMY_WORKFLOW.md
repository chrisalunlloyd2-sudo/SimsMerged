# 🌙 Autonomy Workflow: Claude · Hermes · Alice over Tailscale

> **TL;DR:** bounties go in, reviewed work comes out, you read one morning digest.

| Role | Agent | Does | Never does |
|------|-------|------|------------|
| 🏛️ Architect | **Claude** | Plans, splits work into bounties, resolves disputes | Routine polling (burns quota) |
| 🛠️ Developer | **Hermes** | Claims bounties, ships additive changes | Approves own work |
| 🔍 Critic | **Alice** | Reviews logic and direction, gates payout | Writes the code she reviews |

Roles, hosts and token caps live in [`nodes.json`](../nodes.json).

## The loop (Nocturnal window, 8 PM – 8 AM)

```mermaid
flowchart LR
    C[Claude: post bounty] --> O[(bounties/open)]
    O -->|atomic claim| H[Hermes works on own branch]
    H --> CL[(bounties/claimed)]
    CL --> A{Alice reviews}
    A -->|approve| D[(bounties/done) + payout]
    A -->|reject| O
    D --> M[☀️ Morning digest]
```

## Commands

```bash
B=backend/core/delegation/bounty_dispatcher.py
python $B post B-001 "Describe the task" 10 developer   # Claude
python $B claim B-001 hermes                             # Hermes
python $B approve B-001 alice yes "logic is sound"       # Alice (use 'no' to re-open)
python $B digest                                         # You, in the morning
```

## Guardrails (from your Golden Commandments)
- ➕ Additive only: no deletes, no force-push, `git push --dry-run` first.
- 🏷️ Every commit carries `[TIMESTAMP][PROJECT_ID][AGENT_ID]`.
- 🔒 Local-only inference (Ollama); no external AI APIs.
- 🙅 An agent cannot approve its own bounty.
- ✅ Tests are trusted; review focuses on logic and direction.

## 💸 Quota discipline
1. Local Ollama models do polling and triage.
2. Claude is only invoked for Architect bounties or rejected-twice disputes.
3. Per-agent daily caps in `nodes.json`; the dispatcher owner pauses posting when a cap is hit.

## 🕸️ Tailscale setup (5 steps)
1. Install Tailscale on every machine; enable MagicDNS.
2. Tag devices: `tag:laptop` (hub), `tag:agent` (workers).
3. ACL: allow `tag:agent` → `tag:laptop:11434` only.
4. Bind Ollama to the tailnet (`OLLAMA_HOST=0.0.0.0:11434`, firewall everything except `tailscale0`).
5. Put real MagicDNS names in `nodes.json`; check `digest` → `online_peers`.

## 🗺️ Roadmap
- [ ] Wire `approve()` payout to `DePINLedger.fund_wallet`
- [ ] Enforce `daily_token_cap`
- [ ] Morning digest delivered to a file/notification
- [ ] Consolidate `*orchestrator*.py` behind one task queue
