# SIMSMERGED ENTERPRISE MASTER PLAN: GRAND UNIFICATION
**STATUS:** ACTIVE | **PHASE:** ENTERPRISE EVOLUTION
**TARGET:** End-to-End Delivery, Installer Creation, & Beta Unification

This document synthesizes the architectural vision into a highly organized, mathematically grounded, and rigorously structured Master Plan. Logical inconsistencies have been resolved (e.g., ensuring SSD fencing operates via memory-mapped files to trick Ollama, resolving asynchronous wallet state deadlocks with atomic DePIN transactions, and structuring the Tok Tree as a Directed Acyclic Graph for command validation).

---

## PART I: ARCHITECTURAL SEGMENTATION

### 1. WebUI (The Isometric Interface)
- **Component:** `index.html` and related visual DOM elements.
- **Guardrails:** LOCKED. All future updates will be performed via strictly typed, isolated DOM injection scripts to prevent layout collapse. Visuals will be gradually decoupled from the backend state machine.

### 2. The Agentic Subsystem: "Sprite Triplet Architecture"
- **Cascading SLM Triplet:** 
  - **L1 (500M Master):** Driven by the Tok Tree (Control Tower). Issues macro-commands.
  - **L2 (250M Orchestrator):** Translates macro-commands into procedural steps.
  - **L3 (135m Smoll):** Directly interfaces with the Qwen Coder IDE CLI.
- **Concurrent Hosting:** Orchestrated via Ollama instance clustering with SSD-fenced memory mapping (bypassing RAM bloat).
- **Mock IDE Bridge:** A synthetic REST/WebSocket API intercepting Qwen IDE calls to validate code before topological insertion.
- **Pedagogical Memory (BM25 + Vector DB):** Every successful script is embedded and indexed. The L2 Orchestrator uses a RAG Chain-of-Thought layer to retrieve prior logic. *Rule: No code is written twice.*
- **DePIN Wallet (Resource Gating):** Token-based execution. 1 Token = 1 Inference Cycle. If the wallet is empty, the L3 agent is suspended. Funding is dynamically allocated by the Tok Tree.
- **Script Pyramid DB:** A fallback persistent terminal environment containing pre-vetted utility scripts.

### 3. Agentic Tok Communications (The Nervous System)
- **The Tok Tree:** The centralized Control Tower managed by the user, Clippy, or a high-parameter (7B) local model. Distributes tasks and injects DePIN tokens.
- **MSN Metropolis Protocol:** The chat-based UI where models act as "users".
- **Chat Extractor Module:** Monitors the topological coordinates of agents and translates their internal CoT into human-readable blips in the chat.
- **Inner Tok Layer:** A background surveillance daemon that records all inter-agent API calls and translates them into simulated "eavesdropped" conversations for analysis.
- **Bi-Directional Hooks:** Models can be tagged (`@AgentName`) in the chat to dynamically interrupt their current DePIN cycle and process new instructions.

### 4. Systems Entirety (The Heartbeat & Fence)
- **SSD Fencing:** Implementing `mmap` (memory-mapped files) to virtualize RAM. Ollama will be wrapped in a hypervisor-lite environment, forcing it to read/write to the NVMe SSD instead of consuming DDR.
- **Global Heartbeat Engine:** A sub-millisecond cron daemon (`pulse_core.py`) that syncs the Tok Tree, DePIN wallets, and L1/L2/L3 states.
- **Integration Validation:** Automated play-testing matrices to ensure flawless ecosystem function.

---

## PART II: 300-STEP PROGRESSION MATRIX

### SECTION A: SPRITE SUBSYSTEM (100 Next Steps)
*Focus: Triplet Architecture, SSD Fencing, BM25 Memory, DePIN Wallet*

**Phase 1: Triplet Scaffolding (1-10)**
1. Initialize virtual environments for L1, L2, and L3 models. 2. Configure concurrent Ollama ports. 3. Build L3 Qwen CLI wrapper. 4. Scaffold L2 to L3 translation API. 5. Scaffold L1 to L2 macro API. 6. Implement API rate limiting. 7. Map L1 instructions to L2 context limits. 8. Create synthetic Qwen IDE endpoint. 9. Route L3 outputs to synthetic IDE. 10. Write unit tests for Triplet cascade.

**Phase 2: SSD Fencing Implementation (11-20)**
11. Build `TritonDiskCache` module. 12. Hook Windows `CreateFileMapping`. 13. Map Ollama tensor allocations to disk. 14. Set page fault interceptors. 15. Optimize NVMe I/O chunking. 16. Implement slow-burn throttling logic. 17. Test RAM usage (must remain < 50MB). 18. Handle SSD write exhaustion grace periods. 19. Build SSD garbage collector. 20. Benchmark triplet inference on SSD.

**Phase 3: Pedagogical Memory & BM25 (21-30)**
21. Spin up local Faiss/Chroma instance. 22. Integrate BM25 sparse retrieval. 23. Build dense/sparse hybrid search engine. 24. Hook L2 CoT to search engine. 25. Build code-chunking tokenizer. 26. Ingest existing `ViperNotes` into Vector DB. 27. Implement "Code Reuse" strictness logic. 28. Add metadata tagging (success/fail rates) to vectors. 29. Build auto-pruning for deprecated logic. 30. Validate RAG outputs for L3 consumption.

**Phase 4: DePIN Wallet & Resource Gating (31-40)**
31. Create SQLite ledger for agent wallets. 32. Build cryptographic token generation. 33. Hook DePIN state to L3 execution loop. 34. Implement "Suspend on Empty" signal. 35. Build Tok Tree funding endpoint. 36. Add transaction hash validation. 37. Calculate inference cost per token. 38. Build token burn mechanism. 39. Implement DePIN crash recovery. 40. Test asynchronous wallet locks.

**Phase 5: Script Pyramid Integration (41-50)**
41. Design Script Pyramid schema. 42. Build REST bridge to Pyramid DB. 43. Create terminal emulation sandbox. 44. Allow L2 to execute Pyramid scripts. 45. Route stdout/stderr back to L2. 46. Implement infinite loop circuit breakers. 47. Build script parameterization engine. 48. Create success/failure feedback loop. 49. Integrate L3 code submission to Pyramid. 50. Validate Pyramid idempotency.

**Phase 6: Topological Wrapping (51-60)**
51. Define 2D/3D topological coordinate system. 52. Assign agents (x,y,z) coordinates. 53. Build filesystem mapper based on topology. 54. Restrict L3 writes to local topological zone. 55. Implement zone permission matrix. 56. Build cross-zone file request API. 57. Handle topological collision events. 58. Create topological state visualizer script. 59. Integrate topology with DePIN costs (distance = cost). 60. Unit test boundary fencing.

**Phase 7: Advanced Execution Metrics (61-70)**
61. Build sub-millisecond execution profiler. 62. Log AST complexity of generated code. 63. Track L2/L3 translation accuracy. 64. Export metrics to Prometheus format. 65. Build anomaly detection for hallucinating models. 66. Implement auto-rollback on severe errors. 67. Track DePIN burn rate over time. 68. Monitor SSD IOPS utilization. 69. Build efficiency scoring system. 70. Dashboard integration prep.

**Phase 8: Heartbeat Synchronization (71-80)**
71. Build L1 Liveness probe. 72. Build L2 Liveness probe. 73. Build L3 Liveness probe. 74. Hook probes to Central Pulse daemon. 75. Implement dead-letter queues for missed beats. 76. Build auto-resuscitation logic. 77. Sync DePIN deductions with heartbeats. 78. Implement clock-drift correction. 79. Handle system hibernation gracefully. 80. Stress-test heartbeat under heavy load.

**Phase 9: Edge-Case Hardening (81-90)**
81. Handle Ollama crash/restart mid-generation. 82. Handle SQLite DePIN lock contention. 83. Mitigate RAG prompt injection loops. 84. Prevent topological escape attempts. 85. Handle corrupted Vector DB indexes. 86. Build failover L3 fallback model. 87. Implement strict JSON schema enforcement on output. 88. Add entropy limits to prevent repetitive outputs. 89. Handle out-of-disk-space gracefully. 90. Full subsystem regression test.

**Phase 10: Sprite Finalization (91-100)**
91. Refactor Triplet bootstrap script. 92. Minify Python dependencies. 93. Create automated L1/L2/L3 weight download script. 94. Document API schemas. 95. Build subsystem health-check CLI. 96. Integrate with Windows Event Logs. 97. Finalize DePIN economic constants. 98. Freeze Triplet architecture codebase. 99. Security audit of L3 IDE bridge. 100. Sprite Subsystem Beta release tag.

---

### SECTION B: CHAT & BACKEND SUBSYSTEM (100 Next Steps)
*Focus: Tok Tree, Inner Tok Layer, MSN Metropolis Protocol, Fast API*

**Phase 1: Tok Tree (Control Tower) (1-10)**
1. Define Directed Acyclic Graph (DAG) for tasks. 2. Build 7B model API bridge for Tok Tree. 3. Implement task splitting algorithms. 4. Create DePIN funding logic based on task complexity. 5. Build manual override hooks for Viper/Clippy. 6. Implement priority queues for L1 instructions. 7. Build dependency resolution for tasks. 8. Add task timeout and revocation logic. 9. Build Tok Tree state persistence. 10. Test Tok Tree DAG resolution.

**Phase 2: Inner Tok Layer (Eavesdropping) (11-20)**
11. Build WebSocket interception daemon. 12. Hook into L1<->L2<->L3 JSON payloads. 13. Create LLM summarization pipeline for raw logs. 14. Map raw calls to conversational analogies. 15. Store inner monologues in separate SQLite table. 16. Build regex filters for sensitive data. 17. Implement real-time streaming of inner tok. 18. Add topological context to inner tok logs. 19. Build sentiment analysis on agent frustration. 20. Unit test interception overhead.

**Phase 3: MSN Metropolis Engine (21-30)**
21. Build core Chat API (FastAPI). 22. Implement "Agent as User" authentication schema. 23. Build room/channel topology. 24. Hook Inner Tok Layer to "System" channel. 25. Enable bi-directional `@Agent` tagging. 26. Build interrupt handler for tagged agents. 27. Implement "thinking..." typing indicators. 28. Store chat history in optimized graph DB. 29. Add rich-text formatting for code snippets. 30. Build chat search endpoint.

**Phase 4: Chat Extractor Module (31-40)**
31. Build daemon to monitor Agent (x,y,z) coordinates. 32. Correlate coordinate changes to task progress. 33. Generate automated chat updates (e.g., "Agent X moved to Sector Y"). 34. Hook Extractor to L3 output validation. 35. Translate compiler errors into chat apologies/updates. 36. Implement rate-limiting to prevent chat spam. 37. Add visual tags for DePIN balance updates. 38. Build Extractor summary digests (hourly). 39. Test Extractor under high topological volatility. 40. Refine automated tone (professional vs casual).

**Phase 5: Global Heartbeat & Synchronization (41-50)**
41. Build master `PulseCore` FastAPI endpoint. 42. Implement UDP broadcast for local agent sync. 43. Synchronize Tok Tree ticks with Sprite ticks. 44. Build system-wide pause/resume toggle. 45. Add DePIN inflation/deflation economic ticks. 46. Build lag-compensation for delayed inferences. 47. Implement consensus algorithms for agent disputes. 48. Hook PulseCore to Windows Time API. 49. Build visual pulse monitor in backend terminal. 50. Test system recovery from 5-minute freeze.

**Phase 6: Data Engineering & Analytics (51-60)**
51. Scaffold Apache Arrow for high-speed logging. 52. Build DePIN economic dashboard backend. 53. Track Vector DB hit/miss ratios. 54. Analyze Tok Tree DAG efficiency. 55. Build agent "Career Profile" generators. 56. Implement data anonymization for exports. 57. Create automated daily performance PDF reports. 58. Monitor SSD IOPS vs RAM virtualization metrics. 59. Build predictive models for L3 crash likelihood. 60. Finalize logging schemas.

**Phase 7: Security & Isolation (61-70)**
61. Implement JWT auth for all backend routes. 62. Build AES-256 encryption for script payloads. 63. Enforce strict CORS policies. 64. Isolate Ollama ports from public network. 65. Build SQL injection guards for Chat DB. 66. Add payload size limits to Chat API. 67. Implement IP rate limiting for external UI hooks. 68. Sandbox inner tok evaluation logic. 69. Audit FastAPI dependencies for CVEs. 70. Penetration test mock Qwen IDE.

**Phase 8: Extensibility Hooks (71-80)**
71. Build Webhook system for third-party integrations. 72. Create plugin architecture for MSN Metropolis. 73. Add generic RAG ingestion endpoints. 74. Build custom command `/slash` parser for Tok Tree. 75. Implement Discord/Slack bridge (optional). 76. Add Voice-to-Text capability for user inputs. 77. Build Text-to-Voice for agent chat replies. 78. Create "Agent Cloning" backend endpoint. 79. Implement system state export/import (JSON). 80. Test extensibility payload routing.

**Phase 9: Performance Optimization (81-90)**
81. Migrate core routing to Rust (PyO3) if Python bottlenecks. 82. Optimize SQLite with WAL mode and PRAGMAs. 83. Implement Redis caching for frequent chat queries. 84. Compress L1/L2 API payloads (msgpack). 85. Profile FastAPI async event loop. 86. Minimize JSON serialization overhead. 87. Optimize Vector DB query latency. 88. Implement garbage collection for old chat logs. 89. Tune UDP pulse network settings. 90. Benchmark backend at 10,000 requests/sec.

**Phase 10: Backend Finalization (91-100)**
91. Write exhaustive API documentation (Swagger/OpenAPI). 92. Build Dockerfile for isolated testing. 93. Create automated database migration scripts (Alembic). 94. Finalize `backend_startup.ps1`. 95. Conduct load testing with simulated 50-agent swarm. 96. Review error handling coverage. 97. Optimize startup boot sequence. 98. Clean up deprecated endpoints. 99. Security sign-off on DePIN ledger. 100. Backend Subsystem Beta release tag.

---

### SECTION C: FRONTEND & WEBUI SUBSYSTEM (100 Next Steps)
*Focus: Isometric DOM, Integration, Delivery & Installer*

**Phase 1: Isometric Engine Stabilization (1-10)**
1. Audit `index.html` DOM structure. 2. Lock core CSS namespaces to prevent overwrite. 3. Optimize 2:1 Isometric projection math in JS. 4. Implement WebGL hardware acceleration fallback. 5. Build sprite batching for high entity counts. 6. Optimize Z-index sorting algorithms. 7. Implement culling for off-screen topological zones. 8. Add smooth camera panning/zooming. 9. Build resolution-independent scaling. 10. Lock down Front-end state manager (Redux/Zustand).

**Phase 2: MSN Metropolis UI Integration (11-20)**
11. Design retro-futuristic chat interface. 12. Connect WebSocket to FastAPI Chat endpoint. 13. Implement real-time message rendering. 14. Add syntax highlighting for code blocks in chat. 15. Build Agent profile popovers (Stats, DePIN balance). 16. Implement `@mention` auto-complete. 17. Add visual typing indicators linked to L2/L3 logic. 18. Build Inner Tok toggle (show/hide internal monologue). 19. Add system alert toast notifications. 20. Optimize chat DOM for 1000+ messages.

**Phase 3: Visualizing the Agentic State (21-30)**
21. Map topological (x,y,z) data to isometric grid. 22. Create visual avatars for L1, L2, L3 agents. 23. Animate avatars based on Extractor module data. 24. Visualize DePIN token transfers (particle effects). 25. Show active RAG Vector searches (scanning animations). 26. Visualize Tok Tree DAG as a collapsible network map. 27. Add visual indicators for "Sleeping/No Funds" state. 28. Build interactive tooltips for all moving parts. 29. Implement UI layer toggles (Hide terrain, show connections). 30. Optimize canvas rendering loop.

**Phase 4: The "God Hand" Controls (31-40)**
31. Build UI panel for Tok Tree manual overrides. 32. Implement drag-and-drop task assignment. 33. Add slider for manual DePIN token injection. 34. Build UI for pausing/resuming specific agents. 35. Create "Focus Camera on Agent" button. 36. Implement visual script injection (send code to agent). 37. Build global system pause toggle. 38. Add visual topological fencing tools (draw boundaries). 39. Create "Force Evolution" button for BM25 memory wipe. 40. Connect God Hand UI to backend JWT Auth.

**Phase 5: Telemetry & Dashboards (41-50)**
41. Design overlay for Global System Heartbeat. 42. Build real-time graph for SSD Fencing IOPS. 43. Visualize DePIN economy inflation/deflation curve. 44. Show Ollama VRAM/SSD allocation gauges. 45. Build Tok Tree task completion rate chart. 46. Implement error rate scatter plot. 47. Create Agent Leaderboard based on efficiency. 48. Build mini-map for global topological overview. 49. Implement customizable widget layout. 50. Optimize chart rendering (Chart.js/D3).

**Phase 6: Audio & Polish (51-60)**
51. Source/synthesize retro UI sound effects. 52. Implement spatial audio based on isometric coordinates. 53. Add chat notification sounds. 54. Create ambient "thinking" drones for L3 agents. 55. Build volume control mixer. 56. Add visual polish (bloom, chromatic aberration toggles). 57. Implement dark/light cyber themes. 58. Polish CSS transitions and animations. 59. Ensure UI responsiveness on varying window sizes. 60. Final visual pass on typographic hierarchy.

**Phase 7: End-to-End Game Testing Integration (61-70)**
61. Build automated UI testing suite (Playwright). 62. Create "Game Phase 1: Resource Gathering" test scenario. 63. Validate agent movement via UI coordinates. 64. Create "Game Phase 2: Structure Building" scenario. 65. Validate L3 code generation reflects on UI grid. 66. Create "Game Phase 3: Agent Economy" scenario. 67. Verify DePIN transactions display accurately. 68. Implement automated screenshot validation. 69. Build stress test: 50 agents active simultaneously. 70. Record performance metrics during test phases.

**Phase 8: Delivery Preparation & Installer Architecture (71-80)**
71. Audit total project file size and dependencies. 72. Select installer framework (Inno Setup / NSIS). 73. Write script to bundle Python environment (PyInstaller). 74. Write script to bundle Node/FastAPI backend. 75. Create automated Ollama setup/download hook. 76. Bundle necessary SLM weights (or create downloader). 77. Compile WebUI into standalone electron app (optional). 78. Write post-install scripts (registry edits, pathing). 79. Create desktop shortcuts and start menu items. 80. Build uninstaller logic.

**Phase 9: Documentation & Marketing Assets (81-90)**
81. Generate high-resolution UI screenshots. 82. Record 60fps video of swarm in action. 83. Write "Quick Start Guide" for end users. 84. Draft architectural whitepaper based on this plan. 85. Create engaging README.md with badges. 86. Build a simple promotional landing page template. 87. Document the DePIN tokenomics for users. 88. Write troubleshooting guide for SSD fencing. 89. Finalize EULA/License agreements. 90. Prepare GitHub release draft.

**Phase 10: Grand Unification & Beta Delivery (91-100)**
91. Execute final full-system integration test. 92. Run memory leak profiling across all tiers. 93. Perform final code review of L3 Mock API. 94. Compile final installer executable (`SimsMerged_Installer_v1.exe`). 95. Test installer on a clean virtual machine. 96. Verify post-install startup loops function correctly. 97. Triage and fix any remaining P1/P2 bugs. 98. Lock final version control tags. 99. Sign executables with digital certificate. 100. **BETA RELEASE DEPLOYMENT.**

---
*Generated by Gemini CLI Architect on 2026-06-09. Proceed to Phase 1 Execution upon user authorization.*
