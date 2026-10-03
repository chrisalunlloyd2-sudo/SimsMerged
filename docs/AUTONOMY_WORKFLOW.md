# Autonomy Workflow: Hermes, Alice, Claude over Tailscale

Roles (edit in `nodes.json`): Claude = Architect, Hermes = Developer, Alice = Critic.

## Daily loop (Nocturnal window 8 PM - 8 AM)
1. Post bounties: `python backend/core/delegation/bounty_dispatcher.py post B-001 "desc" 10 developer`
2. An agent claims one (atomic rename, so no double-claims, even over a shared/synced folder):
   `... claim B-001 hermes`
3. Agent works on its own branch, additive changes only, signature triplet on commits.
4. Critic reviews logic/direction (tests are trusted): `... approve B-001 alice yes "notes"`.
   Rejection re-opens the bounty; an agent cannot approve its own work.
5. Morning digest: `... digest` (counts, total paid, online Tailscale peers).

## Quota discipline
Use local Ollama nodes for polling/triage; escalate to Claude only for claimed
Architect bounties. Per-agent daily caps live in `nodes.json` (`daily_token_cap`).

## Tailscale
- Tag machines (`tag:laptop`, `tag:agent`) and ACL: only `tag:agent` -> laptop:11434.
- Use MagicDNS names in `nodes.json`; bind Ollama to the tailnet interface (`OLLAMA_HOST`).
- Laptop is the hub (holds `bounties/`); workers reach it via Tailscale SSH/shared folder.
- Replace `laptop.tailnet.ts.net` in `nodes.json` with your real tailnet name.

## Next
Wire `approve()` payout to `DePINLedger.fund_wallet` (see `backend/master_unification.py`).
