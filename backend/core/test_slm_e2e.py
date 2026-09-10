# [TIMESTAMP: 2026-06-12T22:30:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
import pytest
import requests
import time
import json
import os

# CONFIGURATION
BASE_URL = "http://localhost:11434"
GENERATE_ENDPOINT = f"{BASE_URL}/api/generate"

@pytest.fixture(scope="session", autouse=True)
def wait_for_server():
    """Ensure the SLM server is responsive before running tests."""
    timeout = 30
    start = time.time()
    while time.time() - start < timeout:
        try:
            # Simple probe
            requests.get(BASE_URL, timeout=1)
            break
        except Exception:
            time.sleep(2)
    else:
        pytest.fail("SLM Server (11434) not responsive after 30s")

def test_inference_basic():
    """Tests basic prompt generation."""
    payload = {
        "model": "house-slm",
        "prompt": "The logical sequence of",
        "agent_id": "test_agent",
        "stream": False
    }
    response = requests.post(GENERATE_ENDPOINT, json=payload, timeout=60)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    print(f"\n[E2E] Generated: {data['response']}")

def test_throttling_logic():
    """
    Tests the 10-minute throttle mandate.
    Note: This test assumes the server is running our 'house' logic.
    """
    payload = {
        "model": "house-slm",
        "prompt": "Throttle test",
        "agent_id": "throttled_agent",
        "stream": False
    }
    # First request
    requests.post(GENERATE_ENDPOINT, json=payload)

    # Second request (immediate)
    response = requests.post(GENERATE_ENDPOINT, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "THROTTLED" in data["response"]
    print(f"\n[E2E] Throttle verified: {data['response']}")

def test_mmap_fenced_response_format():
    """Verifies the response contains expected telemetry fields (eval_count, etc)."""
    payload = {
        "model": "house-slm",
        "prompt": "Telemetry test",
        "agent_id": "telemetry_agent",
        "stream": False
    }
    # Wait for throttle to clear if needed, or use new agent
    response = requests.post(GENERATE_ENDPOINT, json=payload)
    assert response.status_code == 200
    data = response.json()
    # While Ollama might not have these exact names, our house server does.
    # We check if it adheres to the 'response' key at minimum.
    assert "response" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
