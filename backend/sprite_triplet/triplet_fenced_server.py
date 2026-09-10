# [TIMESTAMP: 2026-06-11T12:45:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: Gemini-CLI-Architect]

import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any

from .triplet import SpriteTriplet
from .omniscient_steer import omniscient_steer
from .resource_governor import resource_governor
from .pattern_recognition import pattern_engine
from ..core.model_test_lab import model_test_lab
from ..core.geometry_analyzer import geometry_analyzer
from ..core.research_synthesis import synthesis_engine
from .config import add_log, add_message
from .tok_tree import tok_tree

app = FastAPI(title="Metropolis Triplet Fenced Server")
triplet = SpriteTriplet()

class CascadeRequest(BaseModel):
    instruction: str
    agent_id: Optional[str] = "unknown_agent"
    tags: Optional[list] = []

class SteerRequest(BaseModel):
    query: str
    agent_id: Optional[str] = "unknown_agent"
    tags: Optional[list] = []

class LabRequest(BaseModel):
    code: str

@app.on_event("startup")
async def startup_event():
    # Start the Resource Governor (CPU < 50% limit)
    resource_governor.start()
    add_log("[TRIPLET_SERVER] Fenced Server Online. Resource Governor Active.")

@app.on_event("shutdown")
async def shutdown_event():
    resource_governor.stop()
    add_log("[TRIPLET_SERVER] Fenced Server Offline.")

@app.post("/api/v1/model-lab/stress-test")
async def run_lab_test(request: LabRequest):
    """Conducts a Geometric Stress Test on code."""
    results = model_test_lab.run_geometric_stress_test(request.code)
    return {"status": "success", "results": results}

@app.post("/api/v1/model-lab/thumb-vars")
async def run_thumb_vars(request: LabRequest):
    """Automates variable thumbing in code/data."""
    results = model_test_lab.thumb_for_variables(request.code)
    return {"status": "success", "results": results}

@app.post("/api/v1/research/synthesize")
async def start_research(topic: str, agent_id: Optional[str] = "Research_Director"):
    """Starts the multi-chapter synthesis process (Phase 7)."""
    asyncio.create_task(synthesis_engine.generate_comprehensive_paper(topic, agent_id))
    return {"status": "started", "message": f"Synthesis for '{topic}' initiated in background."}

@app.post("/api/v1/triplet/cascade")
async def run_cascade(request: CascadeRequest):
    """Executes the ARCHITECT -> TRANSLATOR -> CODER cascade."""
    add_log(f"[TRIPLET_SERVER] Initiating Cascade: {request.instruction[:50]}...")

    # Step 41: Tok Tree Augmentation
    augmented_instruction = tok_tree.augment_prompt(request.instruction, request.tags)

    if omniscient_steer.process_ask(augmented_instruction):
        return {"status": "steered", "message": "Handled by Omniscient Steer (Non-LLM)"}

    result = await triplet.run_cascade(augmented_instruction)

    # Step 45: Connect DMAIC-Analyzer directly to EconomySystem
    if dmaic_engine:
        expected_patterns = { "function_def": r"def\s+[a-zA-Z_]\w*\s*\(" }
        required_tokens = ["def"]
        try:
            grade = dmaic_engine.grade_logic(result['l3_payload'], expected_patterns, required_tokens)
            if grade["passed"]:
                # Notify Main server to update action for EconomySystem
                requests.post("http://127.0.0.1:8000/api/agent/action", json={"agent_id": request.agent_id, "action": "dmaic_compile_success"}, timeout=2)
                add_log(f"[TRIPLET_SERVER] Agent {request.agent_id} passed DMAIC validation! Massive TP multiplier applied.")
        except Exception as e:
            add_log(f"[TRIPLET_SERVER] DMAIC integration error: {str(e)}")

    pattern_engine.store_pattern(
        pattern_id=f"cascade_{hash(request.instruction)}",
        category="code_cascade",
        data=result['l3_payload'],
        metadata={"instruction": request.instruction, "agent": request.agent_id}
    )

    # Ingest the successful result into the Tok Tree for future runs
    tok_tree.insert_context(f"Success for '{request.instruction}': {result['l3_payload'][:100]}...", request.tags + ["cascade_result"])

    return {"status": "success", "data": result}

@app.post("/api/v1/steer")
async def steer_query(request: SteerRequest):
    """Manual trigger for the Omniscient Steer."""
    augmented_query = tok_tree.augment_prompt(request.query, request.tags)
    handled = omniscient_steer.process_ask(augmented_query)
    return {"status": "success" if handled else "ignored", "handled": handled}

@app.get("/api/v1/telemetry/geometry")
async def get_telemetry_geometry():
    """Returns the latest geometric manifold analysis of the system."""
    import psutil
    telemetry = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent
    }
    analysis = geometry_analyzer.analyze_manifold(telemetry)
    return {"status": "success", "analysis": analysis}

@app.post("/api/v1/qwen/cli")
async def run_qwen_cli(command: str, tags: list = []):
    """Executes a command via the Qwen Coder CLI wrapper."""
    cli_path = "C:\\Users\\viper\\Desktop\\SimsMerged\\backend\\bin\\qwen-coder.ps1"
    if not os.path.exists(cli_path):
        raise HTTPException(status_code=500, detail="Qwen Coder CLI not found. Run setup_qwen_coder.ps1 first.")

    # Step 41: Tok Tree Augmentation
    augmented_command = tok_tree.augment_prompt(command, tags)

    add_log(f"[QWEN_CLI] Executing: {command}")

    # Using the augmented command safely
    # Note: Escaping double quotes if they exist in the augmented_command
    safe_command = augmented_command.replace('"', '\\"')
    process = await asyncio.create_subprocess_shell(
        f"powershell.exe -NoProfile -Command \"& '{cli_path}' \\\"{safe_command}\\\"\"",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()

    if process.returncode == 0:
        tok_tree.insert_context(f"CLI Success: {stdout.decode()[:100]}", tags + ["cli_result"])

    return {
        "status": "success" if process.returncode == 0 else "error",
        "output": stdout.decode(),
        "error": stderr.decode()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)
