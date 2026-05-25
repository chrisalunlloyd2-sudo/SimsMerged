-- [TIMESTAMP: 2026-05-25T03:02:14.000Z][PROJECT_ID: SimsMerged-v1.3][AGENT: Sprite_Teacher_86]
-- Pedagogical Swarm Training: SQLite Schema compiled dynamically.
CREATE TABLE IF NOT EXISTS DePIN_Ledger (
    block_index INTEGER PRIMARY KEY,
    timestamp REAL,
    agent_name TEXT,
    action_type TEXT,
    prev_hash TEXT,
    block_hash TEXT,
    difficulty_target INTEGER DEFAULT 3
);
