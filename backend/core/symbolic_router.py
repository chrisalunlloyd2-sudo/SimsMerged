# [TIMESTAMP: 2026-06-11T02:50:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import re
import json
import asyncio
from typing import Dict, Any, List
from .vector_ring import vector_ring
from .llm_client import llm_client
from .geometry_analyzer import geometry_analyzer
from .config import add_message

class SymbolicRouter:
    """
    PHASE 25: THE LEARNING SYMBOLIC ROUTER
    - Intercepts coding/research requests.
    - Semantic match via Vector Ring.
    - Uses Geometry Analyzer for Structural Integrity Scoring.
    """
    def __init__(self, threshold: float = 0.85):
        self.similarity_threshold = threshold

    async def route_request(self, agent_id: str, prompt: str, language: str = "python") -> str:
        print(f"🚦 [SYMBOLIC_ROUTER] Analyzing request: {prompt[:50]}...")
        
        # 1. Query the Ring for existing logic
        matches = vector_ring.query_logic(prompt, language=language)
        
        if matches and (1.0 - matches[0]['distance']) > self.similarity_threshold:
            template = matches[0]['code']
            score = 1.0 - matches[0]['distance']
            
            # 2. Geometric Analysis of the Template
            analysis = geometry_analyzer.analyze_manifold({"prompt": prompt, "template_match": True})
            stability = analysis["stability_index"]
            
            print(f"✅ [ROUTER_HIT] Semantic match found (Score: {score:.2f}, Stability: {stability:.2f}).")
            
            # 3. Symbolic Swapping
            swap_prompt = (
                f"You are a SYMBOLIC SWAPPER. Take the following CODE TEMPLATE:\n\n{template}\n\n"
                f"Update only the variable names and specific logic parameters to fulfill this NEW REQUEST: {prompt}. "
                "Output ONLY the updated code. Do not synthesize new logic structures."
            )
            
            final_code = await llm_client.generate(swap_prompt, agent_id=agent_id)
            add_message(agent_id, f"♻️ [SYMBOLIC_REUSE] Recycled logic. Integrity: {stability:.2f}")
            return final_code
        
        # 3. Cache Miss: Fresh Synthesis
        print("❌ [ROUTER_MISS] No suitable template in Ring. Routing to SLM for fresh synthesis.")
        fresh_code = await llm_client.generate(prompt, agent_id=agent_id)
        
        # 4. Hydrate the Ring
        # Extract performative from prompt (naive)
        perf = "generic"
        if "procedural" in prompt.lower(): perf = "asset_synthesis"
        elif "optimize" in prompt.lower(): perf = "optimization"
        elif "fix" in prompt.lower(): perf = "bug_fix"
        
        vector_ring.store_pattern(fresh_code, language, perf, {"source_agent": agent_id})
        return fresh_code

symbolic_router = SymbolicRouter()
