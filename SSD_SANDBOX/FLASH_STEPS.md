# [TIMESTAMP: 2026-06-12T21:05:00.000Z] [PROJECT_ID: SimsMerged-v1.4.2] [AGENT_ID: viper_cli-architectssj4]
# FLASH: ELABORATE EXECUTION BLUEPRINT & SLM SOP

## 🎯 1. EXECUTIVE SUMMARY & NOVEL RESEARCH METHODOLOGIES
**MISSION:** Flash is mandated to exhaustively test, optimize, and genetically advance all components of the SimsMerged Metropolis ecosystem. 

**NOVEL DATA ACQUISITION & PATTERN RECOGNITION:**
- **BM25 ML Sharding:** Leveraging the new 2KB log sharding architecture, Flash must run `scikit-learn` TF-IDF passes over `syslog_*.log` files to extract recurring algorithmic bottlenecks.
- **Tandem Ask-Tell RAG:** Flash must employ Markovian state transitions before code generation. Every prompt sent to local models MUST be prefixed with local codebase context mapped from `never_make_code_twice.duckdb`.
- **Lean Six Sigma (LSS) Validation:** Every single generated line of code must undergo the DMAIC (Define, Measure, Analyze, Improve, Control) pipeline natively via the EPMO Business School class.

---

## 🏗️ 2. SLM (SMALL LANGUAGE MODEL) STANDARD OPERATING PROCEDURES (SOP)
*Strict guidelines for model control using the in-house C++ Server and Local Ollama Network.*

### A. Inference Initialization & Fencing
1. **Model Selection:** Always prioritize smaller, specialized weights for atomic tasks (`qwen2.5:0.5b`, `smollm:135m`). Reserve `llama3` or larger parameters exclusively for abstract logic.
2. **Context Window Management:** Strictly enforce a 4096 context window limit (`Num_CTX`) per request to prevent VRAM bloat on the 4GB host constraint.
3. **Ghost Code Hook:** Before generating ANY net-new logic, the SLM orchestrator MUST query the `/api/epmo/ghost-code` endpoint via BM25 to check if the solution already exists. NEVER make code twice.
4. **Darwinian Advancement (The "Syphon" Loop):**
   - Extract raw performatives from user asks.
   - Run the task: "Make code in Python to do: [performative]"
   - Extract variables and tether them mathematically.
   - Feed the result back into the SLM: "Optimize and advance this code mathematically for performance and LSS efficiency."
   - Repeat for 3 iterations until the code reaches peak LSS score (>9.0).
   - Deposit directly to the DuckDB Ghost Code repository.

### B. Enterprise Version Control & Granular Method
1. **Atomic Commits:** Flash must never commit massive refactors simultaneously. Every component upgrade must be isolated to a single file, tested, and pushed via the Agentic GitHub Suite.
2. **Deterministic Validation:** Before moving to the next component, Flash must empirically run `pytest`, `mvn compile`, or an autonomous script to prove the upgrade did not break the build.
3. **Timestamping Mandate:** Every file header MUST be updated with ISO 8601 timestamps and Agent IDs to ensure perfect traceability.

---

## 🔍 3. EXHAUSTIVE COMPONENT UPGRADE BLUEPRINT
Flash must progress through this blueprint methodically, executing one block at a time.

### Block A: The Knowledge Base (Tok Tree & DuckDB)
- [x] **A1:** Analyze `never_make_code_twice.duckdb` for performance metrics. Implement a vector-caching layer to speed up BM25 retrieval by 40%.
- [x] **A2:** Scrape all newly introduced Python scripts (`ml_orchestrator.py`, `data_syphon_epmo.py`) and forcibly ingest their methods into the Ghost Code database as high-value anchors.
- [x] **A3:** Expand the BM25 learning algorithm. Create an endpoint that allows the system to upvote/downvote Ghost Code blocks based on whether they successfully compiled during subsequent SLM usage.

### Block B: The EPMO & Data Syphon Mechanics
- [x] **B1:** Introduce "Pattern Recognition Advisories". Connect the `ml_orchestrator` to the JavaFX GUI so it sends "Advisory Alerts" into the `SystemConsole` when it detects suboptimal model behaviors.
- [x] **B2:** Upgrade the `LeanSixSigmaEPMO` class to natively critique code readability, Big-O complexity, and error-handling robustness using an advanced heuristic weighing scale.
- [x] **B3:** Ensure all telemetry gathered from the Darwinian loops natively feeds into the DePIN ledger, rewarding models that produce higher LSS-scoring code with Treasury Points.

### Block C: The Agentic GitHub Management Suite
- [x] **C1:** Design and deploy `agentic_github_suite.py` (The GitHub Governor). This script must autonomously read the local `git log`, analyze diffs using an SLM, and generate enterprise-grade commit messages.
- [x] **C2:** Give the Governor the ability to create "Optimization Branches", run Darwinian tests on those branches, and auto-merge to `main` if the LSS score improves.
- [x] **C3:** Tie the GitHub Governor into the JavaFX `IssueTrackerPanel` so that pulling a GitHub issue natively spawns a local Git branch assigned to a specific agent.

### Block D: Advanced Model Metrics & Telemetry
- [x] **D1:** Expand `ValidationDashboardWindow.java` to map physical VRAM usage and Disk I/O stress on an active line chart.
- [x] **D2:** Create a telemetry hook in the backend that records the exact "Tokens/Second" generated by the local Ollama models and graphs it against CPU temperature.
- [x] **D3:** Ensure the system uses statistical correlation to find problem points (e.g., "Model X hallucinates when CPU Temp > 85°C").

### Block E: Absolute World Finality
- [x] **E1:** Execute comprehensive End-to-End (E2E) testing on the `metropolis_slm_server.cpp` using the newly developed `pytest` lab scripts.
- [ ] **E2:** Finalize all remaining GUI aesthetics. Ensure the "Data Syphon" particle logic perfectly mimics the speed of actual network traffic happening on port 8000.
- [ ] **E3:** Backup the completely optimized, genetically advanced Metropolis engine to a compressed `.zip` payload for cold storage.

---
**EXECUTION PROTOCOL:**
Flash must wait for the "next" command, read the very first `[ ]` block, apply granular code changes using `replace` and `write_file`, test synchronously, and commit via the new Agentic Suite.
