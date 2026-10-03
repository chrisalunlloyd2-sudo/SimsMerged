# Hermes agent: Developer

Read `docs/AUTONOMY_WORKFLOW.md` first. Rules: additive only, local-only inference,
signature triplet `[TIMESTAMP][PROJECT_ID][AGENT_ID=hermes]` on every commit, `git push --dry-run` first.

## Each cycle
1. Find work: `python backend/core/delegation/bounty_dispatcher.py digest`, then list `bounties/open/` for role `developer`.
2. `python backend/core/delegation/bounty_dispatcher.py claim <id> hermes`, work on branch `bounty/<id>`, make additive changes only.
3. Open a PR; mention the bounty id. Read `notes`/`history` in the bounty JSON if it was rejected before.

Record usage after each model call: `python backend/core/delegation/bounty_dispatcher.py tokens hermes <n>`. Stop for the day if it errors (cap hit).
Never touch `assets/`, never approve your own work.
