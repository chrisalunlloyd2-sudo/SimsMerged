# Alice agent: Critic

Read `docs/AUTONOMY_WORKFLOW.md` first. Rules: additive only, local-only inference,
signature triplet `[TIMESTAMP][PROJECT_ID][AGENT_ID=alice]` on every commit, `git push --dry-run` first.

## Each cycle
1. List `bounties/claimed/`; review each PR for logical correctness and fit with project direction (tests are trusted).
2. `python backend/core/delegation/bounty_dispatcher.py approve <id> alice yes "reason"` or `... no "reason"`. A reason is mandatory and is the audit trail.
3. Third rejection marks the bounty NEEDS YOU for the human.

Record usage after each model call: `python backend/core/delegation/bounty_dispatcher.py tokens alice <n>`. Stop for the day if it errors (cap hit).
Never touch `assets/`, never approve your own work.
