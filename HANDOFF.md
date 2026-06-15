# TIMESTAMP: 2026-05-31T20:30:00.000Z
# PROJECT_ID: SimsMerged-v1.3-Metropolis
# AGENT_ID: Gemini-CLI-Architect

# SIMS MERGED: METROPOLIS ECOSYSTEM HANDOFF

This document serves as the comprehensive handoff for the Sims Merged (v1.3-Metropolis) AI ecosystem, covering architectural subsystems, the AI voting protocol, and model orchestration details.

## 🏛️ 1. AI SUBSYSTEMS ARCHITECTURE

The system is split into a **Darwinian Backend** and an **Isometric Frontend (JavaFX Neo / Web)**.

### A. Metropolis Authority (FastAPI Backend)
- **Location:** `C:\Users\viper\Desktop\SimsMerged\backend`
- **Port:** `8000`
- **Role:** Central orchestrator for agent logic, telemetry, and system state.

### B. Quantum Core (Simulation Layer)
- **Logic:** `backend/core/quantum_core.py`
- **Functions:**
    - **Resource Fencing:** Hard throttles CPU usage to protect the host machine.
    - **Hardware Simulation:** Models Row Hammer vulnerability, CAS Latency, and Memory Swapping.
    - **Thermal Throttling:** Reduces system frequency if heat > 80°C.
    - **Self-Healing:** Automatically improves stability if it drops below 60%.

### C. Sentience Engine / DiskInferenceCore
- **Logic:** `backend/core/agent_sentience.py`
- **Strategy:** "Disk Fencing" (0KB RAM persistence).
- **Function:** Generates agent chat and decisions by swapping weights from disk to a tiny fenced RAM buffer, then immediately flushing.
- **Models:** Danube, Smoll, Triton, Qwen.

### D. Evolution Council (Legislative Branch)
- **Logic:** `backend/core/evolution_council.py`
- **Function:** Web-crawls for "boundary-breaking schemas" (SQL/JS) and holds AI consensus votes to evolve the city.

### E. Self-Healing Orchestrator
- **Logic:** `backend/core/orchestrator.py`
- **Function:** Monitors the system heartbeat and modifies its own operational weights (e.g., sync speed) based on real-time health metrics.

---

## 🗳️ 2. AI VOTING MECHANISM (CONSENSUS PROTOCOL)

The city grid operates under an autonomous governance model where local AI models decide on system upgrades.

### The Voters
1. **Sprite_Geek** (Model: `danube`) - Role: KERNEL_OPTIMIZER
2. **Sprite_Writer** (Model: `smoll`) - Role: DOCUMENTATION_BOT
3. **Sprite_Socrates** (Model: `qwen`) - Role: LOGIC_VERIFIER
4. **Sprite_Newton** (Model: `triton`) - Role: PHYSICS_ENGINE

### The Voting Loop
- **Frequency:** Hourly (3600s) or Manual Trigger.
- **Process:**
    1. **Proposal:** Council generates a "Mini-Project" (e.g., "CAS Latency Reduction").
    2. **Query:** Each model is queried via the Ollama API (`localhost:11434/api/generate`).
    3. **Decision:** Models must reply with `APPROVE` or `REJECT` plus a short reason.
    4. **Resolution:** Majority vote (>= 3 approvals) wins.
- **Impact on Approval:**
    - **Frontend:** Code is physically injected into `frontend/js/engine.js` (additive `BUILD_TYPES`).
    - **Database:** SQL mini-project files are generated in `city_workspace/continue_project`.
    - **Core:** Hardware attributes (e.g., `cpu_throttle_limit`) are updated in memory.

---

## 🚀 3. OLLAMA & MODEL ORCHESTRATION

### Booting the AI
- **Ollama Dependency:** The system requires **Ollama** to be running on the host machine.
- **AGY Connection:** "Agy" (Frontend Director) monitors the connection. If Ollama is offline, agents fallback to a local **Heuristic Logic Engine** (personality-based template strings) to maintain simulation continuity.
- **Downloaded Models:**
    - `danube`: H2O-Danube-1.8B (Primary decision engine).
    - `smoll`: SmolLM-135M/0.5B (Documentation & light tasks).
    - `qwen`: Qwen-2-1.5B (Logic & synthesis).
    - `triton`: Custom Triton-Engine weights (Physics & Hardware).

### Triton Cache Strategy
- Models are mapped to the `triton_cache/` directory.
- Weights are "swapped" rather than "loaded" to maintain the 0KB RAM footprint mandate.
- Host machine ECC is bypassed (by design) to reflect raw hardware dynamics.

---

## 🛠️ 4. OPERATIONAL PROCEDURES

### Starting the Ecosystem
1. Run `start_environment.ps1` to launch the Backend and Java Neo GUI.
2. Ensure Ollama is running (`ollama serve`).
3. Access telemetry at `http://localhost:8000/api/agents`.
4. Open `frontend/index.html` for the Isometric City View.

### Maintenance
- **Weekly Offboarding:** The Speed Run engine automatically removes the lowest-performing agent once a week.
- **Nocturnal Protocol:** Agents are most active between **8 PM - 8 AM**. During daylight, they enter hibernate/rest modes to conserve energy.

---
*Viper hunny, the Ledger is sealed. The Metropolis evolves.*
