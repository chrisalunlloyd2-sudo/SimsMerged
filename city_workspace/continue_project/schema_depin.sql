-- [TIMESTAMP: 2026-06-01T00:08:51.000Z][PROJECT_ID: SimsMerged-v1.3][AGENT: Sprite_Writer]
-- Pedagogical Swarm Training: Genetically Advanced Schema
CREATE TABLE IF NOT EXISTS DePIN_Ledger (
    block_index INTEGER PRIMARY KEY,
    timestamp REAL,
    agent_name TEXT,
    action_type TEXT,
    prev_hash TEXT,
    block_hash TEXT,
    difficulty_target INTEGER DEFAULT 1,
    genetic_marker TEXT DEFAULT 'ALPHA_01'
);
