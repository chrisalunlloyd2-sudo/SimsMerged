# TIMESTAMP: 2026-06-09
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: viper_cli-architectssj4
# DESCRIPTION: Unit tests for Phase 1 Cascade testing

import pytest
import asyncio
import sys
import os

# Ensure backend module is resolvable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.sprite_triplet.triplet import SpriteTriplet

@pytest.mark.asyncio
async def test_triplet_cascade():
    """
    Tests the full flow from L1 macro instruction down to the L3 payload creation.
    We are expecting the mocked cascade to return structured text wrapping 
    through all three context boundaries.
    """
    triplet = SpriteTriplet()
    result = await triplet.run_cascade("Build a weather station GUI.")
    
    assert "l1_output" in result
    assert "l2_output" in result
    assert "l3_payload" in result
    
    # Asserting that L3 correctly wraps the mock code in a python definition 
    # to pass the Mock IDE validation rules we set up in Step 8.
    assert "def " in result["l3_payload"]

@pytest.mark.asyncio
async def test_l1_macro():
    triplet = SpriteTriplet()
    res = await triplet.l1_macro_process("Test instruction")
    assert "[MOCK_RESPONSE from qwen:500m]" in res

@pytest.mark.asyncio
async def test_l2_orchestrator():
    triplet = SpriteTriplet()
    res = await triplet.l2_orchestrator_process("Test L1 output")
    assert "[MOCK_RESPONSE from qwen:250m]" in res

@pytest.mark.asyncio
async def test_l3_smoll():
    triplet = SpriteTriplet()
    res = await triplet.l3_smoll_process("Test L2 output")
    assert "def execute_task()" in res
    assert "[MOCK_RESPONSE from qwen:135m]" in res
