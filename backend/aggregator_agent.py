# [PERFORMATIVE: AGGREGATOR_AGENT]
import json

def aggregate_metropolis_economy(agent_inventories):
    """Compiles 50+ agent reports into a single economic summary."""
    summary = {"total_wood": 0, "total_stone": 0, "active_pioneers": len(agent_inventories)}

    for agent_id, inv in agent_inventories.items():
        summary["total_wood"] += inv.get("Wood", 0)
        summary["total_stone"] += inv.get("Stone", 0)

    return summary
