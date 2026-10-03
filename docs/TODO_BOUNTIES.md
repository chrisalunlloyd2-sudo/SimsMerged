# Seed Bounties (Phase 13 game logic)

Source: `TODO(role:id)` markers in `backend/game/behavioral_economy.py`. Grep them: `grep -rn "TODO(" backend/game`.
Post one: `python backend/core/delegation/bounty_dispatcher.py post T13-01 "<text>" 10 developer`

| ID | Role | Task |
|----|------|------|
| T13-01 | developer | Real host telemetry reader (CPU/IO), optional + fail-soft |
| T13-02 | architect | Decide reward curve (diminishing returns, streaks) |
| T13-03 | critic | Review daylight-penalty vs sleep logic double counting |
| T13-04 | developer | Weight resource grants by Treasury balance |
| T13-05 | architect | Extend negotiation to RAM and storage |
| T13-06 | developer | Publish `hud_snapshot()` over `gui_hooks.json` |
| T13-07 | critic | Confirm no JavaFX field removed/renamed |
| T13-08 | developer | Bridge `TreasuryPoints` to existing `backend/core/treasury.py` (DC ledger) and `DePINLedger` |
| T13-09 | architect | Tie bounty payouts in `bounty_dispatcher.approve()` to Treasury Points |
