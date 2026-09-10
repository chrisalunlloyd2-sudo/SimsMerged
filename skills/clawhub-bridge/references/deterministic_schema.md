# Deterministic Schema Mapping

## Local Layout vs ClawHub Standard

| Local Field (JSON) | ClawHub Equivalence | Type | Description |
|:---|:---|:---|:---|
| `batch` | `compute.batch_size` | Integer | The number of tokens processed in parallel. |
| `dropout` | `model.dropout_p` | Float | Probability of zeroing weights for regularization. |
| `temp` | `inference.temperature` | Float | Creativity vs Determinism control. |
| `rag_k` | `retrieval.top_k` | Integer | Number of documents retrieved for context. |
| `heads` | `arch.attention_heads` | Integer | Count of attention mechanism splits. |
| `rope` | `arch.rotary_theta` | Number | RoPE positional embedding base. |
| `mem` | `hardware.vram_cap` | Float | KV cache memory threshold in GB. |

## Agent Meta-Data
| Local JSON | ClawHub Registry | Note |
|:---|:---|:---|
| `id` | `uuid` | Unique city identifier. |
| `xp` | `reputation_score` | Performance-based trust multiplier. |
| `personality` | `agent_profile` | Behavioral heuristic mapping. |
