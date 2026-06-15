import json

def aggregation_utils(stateMachine, scoreSum):
    """
    Manages data stored by the agent's state machine and provides an API hook
    that displays the safety ratings in real-time.
    """
    if isinstance(stateMachine, dict) and stateMachine.get("status") == "error":
        return json.dumps({
            "status": "error",
            "safety_rating": 0.0,
            "message": f"Error: {scoreSum} occurred in {stateMachine.get('name', 'unknown')}"
        })
    
    # Calculate a baseline safety rating
    rating = min(100.0, max(0.0, scoreSum * 1.5))
    
    return json.dumps({
        "status": "active",
        "safety_rating": rating,
        "message": "Safety rating aggregated successfully."
    })
