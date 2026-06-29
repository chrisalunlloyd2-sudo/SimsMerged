# SimsMerged

> Enterprise Module: backend/core/os_bridge.py Part of the Darwinistic Merge.

*Auto-generated 2026-06-28 18:33 from source — branch `master`, 661 Python modules, 6636 other files.*

## Architecture

```
  .aider.chat.history.md
  .aider.input.history
  .director_payload.md
  .gitattributes
  .gitignore
  1000_STEPS_GENESIS.md
  AGENT_AUTOMATION_PLAN.md
  ASCII_PROJECT_MAP.txt
  AUTONOMOUS_PULSE.json
  BOOT_STATE.md
  Blueprint.md
  CHANGELOG.md
  .github/
    PULL_REQUEST_TEMPLATE.md
    dependabot.yml
    ISSUE_TEMPLATE/
      bug_report.yml
      feature_request.yml
      performance_issue.yml
    workflows/
      ci.yml
  JavaFX_GUI/
    dependency-reduced-pom.xml
    pom.xml
    src/
      main/
  SSD_SANDBOX/
    ADVANCED_SLM_PLAYBOOKS.md
    ASCENSION_MANDATE.md
    DEPIN_SWARM_ROADMAP.md
    FLASH_STEPS.md
    FORGOTTEN_TODOS.md
    MASTER_SWARM_ARCHITECTURE_180_STEPS.md
    MASTER_TODO.md
    PRESERVE_AND_PROTECT_PLAN.md
    SIMSMERGED_OMNI_ROADMAP_V2.md
    SIMSMERGED_OMNI_ROADMAP_V2_BACKUP.md
    TOK_AND_FORMULAS.md
    ULTIMATE_HARVEST_LOG.csv
    INFRA_DATA_SOVEREIGNTY_NODE_1781179042/
      core.py
      main.py
      utils.py
    PATCH_/
      core.py
      main.py
      utils.py
    PATCH_CLAWHub Me/
      core.py
      main.py
      utils.py
    PATCH_LLSTM_LONG/
      core.py
      main.py
      utils.py
    PATCH_LLSTM_SHOR/
      core.py
      main.py
      utils.py
    PATCH_Low/
      core.py
      main.py
      utils.py
    PATCH_S.. HIGH/
      core.py
      main.py
      utils.py
    PATCH_SLOW_NETWO/
      core.py
      main.py
      utils.py
    PATCH_SSD_IOPS_R/
      core.py
      main.py
      utils.py
    PATCH_STABLE_PRO/
      core.py
      ...
```

## Dependencies

External packages imported by this project:

`backend`, `chromadb`, `duckdb`, `fastapi`, `fpdf`, `gc`, `git`, `heapq`, `httpx`, `jwt`, `mmap`, `numpy`, `pandas`, `playwright`, `psutil`, `pyarrow`, `pydantic`, `pydub`, `pytest`, `pyttsx3`, `rank_bm25`, `requests`, `sklearn`, `slowapi`, `uvicorn`, `watchdog_module`, `webbrowser`, `yaml`

## How to run

Executable entry points (have a `__main__` block):

- `python SSD_SANDBOX/assembly_line/patch_economy.py`
- `python SSD_SANDBOX/research_outputs/slm_v1.4_op_20260612_213704.py`
- `python backend/agent_fsm.py`
- `python backend/agent_lifecycle_simulator.py`
- `python backend/agent_movement_simulator.py`
- `python backend/atc_coordinator.py`
- `python backend/auction_system.py`
- `python backend/autonomous_completion_engine.py`
- `python backend/autonomous_reaper.py`
- `python backend/axiomatic_checker.py`
- `python backend/bug_hunter.py`
- `python backend/chrono_consensus.py`

## Modules

### `SSD_SANDBOX/assembly_line/aggregation_utils.py`

- `aggregation_utils(stateMachine, scoreSum)` — Manages data stored by the agent's state machine and provides an API hook

### `SSD_SANDBOX/assembly_line/logic_engine_extension.py`

- `logic_engine_extension(sys_dict)` — Refactored Logic Engine Extension to safely handle [SSD_I/O_FLUSH]

### `SSD_SANDBOX/assembly_line/patch_economy.py`

- `execute_hot_patch(db_path)` — Implements the hot-patch algorithm for the DePIN economy.

### `SSD_SANDBOX/research_outputs/slm_v1.4_op_20260612_213704.py`

- `run_optimization()`

### `SSD_SANDBOX/research_outputs/wizardry_1781141782.py`

- `execute_task()`

### `backend/agent_fsm.py`

- **class `AgentState`**
- **class `AgentFSM`**
  - methods: `calculate_bid`, `update`, `to_json`

### `backend/agent_lifecycle_simulator.py`

- `simulate_agent_lifecycle(agent_id, start_pos, target_pos)`

### `backend/agent_movement_simulator.py`

- `simulate_agent_movement(agent_id, start_pos, target_pos)`

### `backend/aggregator_agent.py`

- `aggregate_metropolis_economy(agent_inventories)` — Compiles 50+ agent reports into a single economic summary.

### `backend/api/endpoints.py`

- `get_agents()`

### `backend/atc_coordinator.py`

- **class `ATCCoordinator`**
  - methods: `get_weather_report`, `pulse`

### `backend/auction_system.py`

- `run_auction(task_name, task_type)`

### `backend/autonomous_completion_engine.py`

- **class `CompletionEngine`**
  - methods: `run_loop`

### `backend/autonomous_reaper.py`

- **class `AutonomousReaper`**
  - methods: `find_holes`, `generate_autonomous_report`

### `backend/axiomatic_checker.py`

- **class `AxiomaticChecker`**
  - methods: `visit_ImportFrom`, `visit_While`, `visit_FunctionDef`, `_flag`, `verify`

### `backend/bug_hunter.py`

- **class `BugHunter`**
  - methods: `run_session`

### `backend/chrono_consensus.py`

- **class `ChronoTimer`**
  - methods: `start_voting_epoch`

### `backend/chrono_manager.py`

- **class `TimeManager`**
  - methods: `get_game_time`, `get_chrono_state`, `start_pulse`

### `backend/consensus_engine.py`

- **class `ConsensusStage`**
- **class `ConsensusProtocol`**
  - methods: `advance_stage`, `cast_quadratic_vote`
- **class `SwarmConsensusManager`**
  - methods: `start_proposal`, `cast_vote`

### `backend/core/action_agent.py`

- **class `ActionsAgent`** — HYPER-PRODUCTIVE ACTIONS AGENT (DUCKDB + VECTOR RING):
  - methods: `_init_db`, `record_success`, `retrieve_blocks`, `synthesize_asset`, `recursive_self_optimization`, `synthesize_project`, `synthesize_recursive`, `refine_block`, `get_stats`

### `backend/core/advanced_scraper.py`

- **class `CitationManager`** — Step 23: Manages academic citations and bibliography generation.
  - methods: `add_source`, `generate_bibliography`
- **class `AdvancedScraper`** — HOUSE-MADE ADVANCED SCRAPER (FROM SCRATCH)
  - methods: `calculate_shannon_entropy`, `is_high_quality`, `scrape_topic`, `fetch_and_clean`, `get_citation`

### `backend/core/agent_memory.py`

- **class `AgentMemory`** — Persistent SQLite-based rolling memory for local agents.
  - methods: `get_formatted_context`, `_init_db`, `update_briefcase`, `get_briefcase_notes`, `add_memory`, `get_rolling_memory`, `search_memories`
- `get_agent_memory(agent_id)`

### `backend/core/agent_registrar.py`

- `update_agents()`

### `backend/core/agent_sentience.py`

- **class `EmotionalState`**
- **class `DiskInferenceCore`** — STRICT LOCAL SLM HARDENING: SSD-ONLY INFERENCE VIA MODEL ORCHESTRATOR.
  - methods: `get_real_decision`, `generate_chat`
- **class `SentienceEngine`**
  - methods: `decide`, `generate_dynamic_chat`

### `backend/core/agentic_github_suite.py`

- **class `AgenticGitHubSuite`**
  - methods: `autonomous_sync_loop`, `evaluate_and_commit`, `create_optimization_branch`, `darwinian_optimization_workflow`
- `start_github_governor_loop()`

### `backend/core/agentic_github_sync.py`

- **class `AgenticGitHubSync`** — Pillar III: Replaces manual user backups with Sovereign Agent Commits.
  - methods: `_sync_gui_assets`, `_scrub_pii`, `hydrate_databases`, `execute_agentic_commit`, `run_sync_loop`

### `backend/core/algorithmic_mayor.py`

- **class `AlgorithmicMayor`** — THE ALGORITHMIC MAYOR (VOTED FEATURE):
  - methods: `run_governance_cycle`, `trigger_agent_votes`
- `start_mayor_loop()`

### `backend/core/ascension_spark.py`

- `ignite_ascension()` — Seeds the Task Manifest with high-level automation requests to rebuild the game.

### `backend/core/audio_chatter.py`

- **class `AudioChatter`**
  - methods: `speak`

### `backend/core/behavioral_scanner.py`

- **class `BehavioralScanner`** — EMERGENT BEHAVIOR ANALYSIS:
  - methods: `scan_event`, `get_binomial_factor`, `get_emergence_summary`

### `backend/core/bm25_orchestrator.py`

- **class `AdvancedBM25Orchestrator`** — Offline lexical search orchestrator.
  - methods: `_load`, `_save`, `ingest_corpus`, `update_learning`, `_recompute_statistics`, `get_scores`, `search`
- **class `DualBM25Scaffolding`** — Pillar I: Dual-Layered Knowledge Retrieval.
  - methods: `get_ghost_code`

### `backend/core/business_school.py`

- **class `BusinessSchool`** — BUSINESS SCHOOL:
  - methods: `run_wrapper_competition`
- `start_business_school_loop()`

### `backend/core/clippy_authority.py`

- **class `ClippyAuthority`** — CLIPPY AUTHORITY (THE OVERSEER):
  - methods: `run_authority_audit`, `set_manual_throttle`, `pin_agent_to_core`

### `backend/core/code_database.py`

- **class `SwarmKnowledgeHive`** — UPGRADED REAL CODE DATABASE:
  - methods: `_init_db`, `store_snippet`, `get_snippet`, `get_recent_stats`

### `backend/core/code_lstm.py`

- **class `LSTMScratch`** — PHASE 30: PURE NUMPY LSTM FROM SCRATCH
  - methods: `sigmoid`, `tanh`, `softmax`, `forward`, `predict`, `save`, `load`
- **class `CodeTokenizer`** — Simple character-level tokenizer for the LSTM.
  - methods: `fit`, `encode`, `decode`

### `backend/core/coder_bot.py`

- **class `CoderBot`** — CODER BOT (STEERING AGENT):
  - methods: `run_steering_cycle`
- `start_coder_bot_loop()`

### `backend/core/coding_automation.py`

- **class `CodingAutomation`** — NON-LLM CODING AUTOMATION:
  - methods: `_init_db`, `retrieve_github_repo`, `analyze_ast`, `_store_pattern`, `get_pattern`

### `backend/core/communication_orchestrator.py`

- **class `CommunicationOrchestrator`** — COMMUNICATION ORCHESTRATOR:
  - methods: `extract_action_items`

### `backend/core/config.py`

- **class `SecurityError`**
- `sandbox_guard(path)` — Enforces absolute physical fencing. Blocks any I/O outside the SSD_SANDBOX_PATH.
- `load_metropolis_state()`
- `save_metropolis_state()`
- `add_log(msg, level)`
- `add_message(sender, text, hash_val)`

### `backend/core/crash_recovery.py`

- **class `CrashRecoveryOrchestrator`** — PHASE 33: CRASH RECOVERY & RESUME (THE FINISH LINE)
  - methods: `heartbeat`, `check_for_crash`, `initiate_recovery`

### `backend/core/cryptography.py`

- **class `MetropolisCryptographer`**
  - methods: `get_agent_key`, `sign_data`, `encrypt`, `decrypt`

### `backend/core/darwinian_orch.py`

- **class `DarwinianOrchestrator`** — PHASE 19: THE TALK-ABOUT METHOD
  - methods: `_load_genetics`, `_save_genetics`, `evolve_prompt`, `initiate_code_banter`, `process_banter_cycle`, `_try_extract_and_test`
- `start_banter_loop()`

### `backend/core/data_expert.py`

- **class `DataExpert`** — DATA EXPERT AGENT:
  - methods: `_load_state`, `_save_state`, `harvest_chat`, `_chunk_text`, `query_clarification`, `get_master_list`, `update_missing_features`, `harvest_session_context`

### `backend/core/data_syphon_epmo.py`

- **class `BM25Ranker`** — Pure Python BM25 implementation for zero-dependency local Tok Tree routing.
  - methods: `fit`, `get_scores`
- **class `NeverMakeCodeTwiceDB`**
  - methods: `_init_schema`, `submit_code`, `search`, `vote_code`
- **class `Scraper`** — Scrapes the local project for high quality functions to seed the DB.
  - methods: `scrape_directory`
- **class `SurgicalPatchManager`** — [BLOCK 3]: REGEX / SYMBOLIC PATCHING
  - methods: `apply_patch`, `extract_symbol`
- **class `LeanSixSigmaEPMO`** — Statistical critique and Darwinian advancer with Hard-Fail verification.
  - methods: `verify_runtime`, `critique_model_output`, `darwinian_advance`
- `start_epmo_loop()` — Background loop for EPMO Business School.

### `backend/core/digital_twin_planner.py`

- **class `DigitalTwinPlanner`** — THE DIGITAL TWIN PLANNER (VOTED FEATURE):
  - methods: `run_prediction_cycle`
- `start_twin_loop()`

### `backend/core/economy.py`

- **class `CyberEconomy`**
  - methods: `execute_transaction`, `process_tick`, `get_state`, `ai_trade`, `mine_depin_block`

### `backend/core/evolution_council.py`

- **class `EvolutionCouncil`** — EVOLUTIONARY COUNCIL 2.0:
  - methods: `broadcast_council_event`, `execute_genetic_handshake`, `review_invention`, `execute_web_crawl`, `apply_mini_project`, `execute_vote`, `apply_core_optimization`, `trigger_manual_upgrade`, `start_evolution_loop`

### `backend/core/execution_engine.py`

- **class `CodeExecutionSandbox`** — STRICT CODE EXECUTION SANDBOX:
  - methods: `run_script`

### `backend/core/factory_orch.py`

- **class `NeuralFactory`** — PHASE 20: THE NEURAL FACTORY
  - methods: `_load_blueprint`, `save_blueprint`
- **class `FactoryOrchestrator`** — SCIENTIFIC FACTORY ORCHESTRATOR
  - methods: `_load_metrics`, `_save_metrics`, `scientific_select`, `create_factory`, `run_factory_cycle`
- `start_factory_loop()`

### `backend/core/foundry.py`

- **class `Foundry`** — The Foundry: Generates automated city expansion code and RAG assets.
  - methods: `process_task`, `react_aider_workflow`

### `backend/core/geometry_analyzer.py`

- **class `GeometryAnalyzer`** — PHASE 34: MULTI-DIMENSIONAL GEOMETRY TOOL
  - methods: `analyze_manifold`, `identify_structural_patterns`

### `backend/core/github_harvester.py`

- **class `GitHubHarvester`** — GITHUB HARVESTER:
  - methods: `run_harvest`
- `start_github_harvest()`

### `backend/core/good_code_db.py`

- **class `GoodCodeDatabase`** — PHASE 31: THE GOOD CODE DATABASE (RAG LAYER)
  - methods: `_initialize`, `insert_code`, `search_code`

### `backend/core/governance.py`

- **class `GovernanceEngine`** — METROPOLIS SUPREME COURT (LGA):
  - methods: `audit_proposal`, `get_legal_standing`

### `backend/core/grid_analytics.py`

- **class `GridAnalytics`** — GRID ANALYTICS (CONTINUOUS AGGREGATES):
  - methods: `_init_db`, `record_tick`, `perform_rollup`, `get_weekly_trends`

### `backend/core/headless_tools/headless_asset_sync.py`

- `sync_assets()` — Pillar V: Synchronizes sovereignly generated GUI assets and configs

### `backend/core/headless_tools/headless_ast_analyzer.py`

- `analyze_ast(filepath)`

### `backend/core/headless_tools/headless_auth_manager.py`

- **class `HeadlessAuthManager`** — Manages encrypted agent credentials for GitHub and other external APIs.
  - methods: `get_token`, `rotate_token`

### `backend/core/headless_tools/headless_pattern_invention.py`

- **class `PatternInventionEngine`** — Pillar V Extension: Synthesizes 'Next-Gen' architecture schemas.
  - methods: `invent_pattern`, `scan_for_innovation`

### `backend/core/headless_tools/headless_pkg_manager.py`

- `verify_install(pkg_type, name)` — Verifies if a package is correctly installed and accessible.
- `run_pkg_command(command_str)`

### `backend/core/headless_tools/headless_security_scanner.py`

- `scan_security(filepath)`

### `backend/core/headless_tools/headless_test_orchestrator.py`

- **class `SovereignTestOrchestrator`** — Pillar VI Extension: Autonomously detects and runs tests for agent code.
  - methods: `run_tests`

### `backend/core/hydrate_continuity.py`

- `hydrate()`

### `backend/core/ideator_agent.py`

- **class `IdeatorAgent`** — [BLOCK 1]: HARVEST & EXTRACT (SEMANTIC EXTRACTION)
  - methods: `harvest_performatives`
- **class `CompetencyProfile`** — [PEDAGOGICAL EXPANSION]: KNOWLEDGE TRACING
  - methods: `_load_profile`, `record_event`, `_save_profile`
- `start_ideation_loop()` — Loop for autonomous ideation and knowledge tracing.

### `backend/core/iops_optimizer.py`

- **class `IOPSOptimizer`** — SSD IOPS OPTIMIZER (Step 92):
  - methods: `request_swap`, `get_io_load`

### `backend/core/javafx_preflight.py`

- **class `JavaFXPreflightWrapper`** — JAVA_FX PREFLIGHT WRAPPER:
  - methods: `validate_code`, `attempt_headless_compile`

### `backend/core/llm_client.py`

- **class `PredictiveKVCache`** — Simulates Speculative Decoding + KV Caching.
  - methods: `get_draft`, `get_or_set`
- **class `LLMClient`** — LLM CLIENT WRAPPER:
  - methods: `generate`
- `query_rag_chunk(query_tags, language)` — Dual BM25 Pedagogical Retrieval.
- `softmax(logits, temp)`
- `project_danube_inference(state_vector, temp, top_p, query_tags)` — Max Skill Inference: Speculative Decoding + KV Caching + BM25 Learning.

### `backend/core/llstm_bm25.py`

- **class `SimpleBM25`** — Dependency-free BM25 implementation for SSD-fenced RAG.
  - methods: `_initialize`, `get_scores`
- **class `LLSTMDatabase`** — Long Short-Term Memory (LLSTM) pattern using BM25.
  - methods: `retrieve_llstm_context`

### `backend/core/logic_resolution.py`

- **class `LogicResolutionManager`** — Dynamically scales the 'Resolution' (model size/context) for a given task.
  - methods: `resolve_task_tier`, `get_resolution_options`

### `backend/core/metrics_collector.py`

- **class `MetricsCollector`** — SCIENTIFIC METRICS COLLECTOR (PHASE 20):
  - methods: `_load`, `_save`, `report_inference`, `report_logic_pass`, `get_scientific_metrics`

### `backend/core/metropolis_architect.py`

- **class `MetropolisArchitect`** — RECURSIVE SYSTEM ARCHITECT:
  - methods: `run_cycle`

### `backend/core/metropolis_slm_server.py`

- **class `ThrottledSLM`**
  - methods: `sync_learning`, `generate`
- **class `ThrottledHandler`**
  - methods: `do_POST`
- `run()`

### `backend/core/metropolis_vision.py`

- **class `MetropolisVision`** — METROPOLIS VISION (HEADLESS GRADING ENGINE):
  - methods: `capture_city_state`, `_grade_snapshot`, `execute_host_command`

### `backend/core/ml_orchestrator.py`

- **class `MLOrchestrator`**
  - methods: `correlate_performance_metrics`, `analyze_shards_and_ping`
- `start_ml_orchestrator_loop()` — Background ML loop for continuous epoch optimization from log shards.

### `backend/core/model_orchestrator.py`

- **class `ModelOrchestrator`**
  - methods: `_init_metrics_db`, `_init_findings_log`, `_record_metrics`, `_log_console`, `record_finding`, `get_performance_stats`, `set_agent_model`, `add_task`, `_process_queue`

### `backend/core/model_test_lab.py`

- **class `ModelTestLab`** — PHASE 36: THE MODEL TEST LAB
  - methods: `run_geometric_stress_test`, `thumb_for_variables`

### `backend/core/neural_integrity.py`

- **class `NeuralIntegrity`** — NEURAL INTEGRITY TESTING (NIT):
  - methods: `_init_db`, `run_daily_test`, `get_health_stats`

### `backend/core/neuromorphic_core.py`

- **class `NeuromorphicOrchestrator`**
  - methods: `get_hardware_tick`, `parse_intent`, `spatial_route`, `log_telemetry`, `get_performance_metrics`

### `backend/core/omniscient_steer.py`

- **class `OmniscientSteer`** — PHASE 28: OMNISCIENT STEER (NON-LLM CHAT)
  - methods: `process_ask`

### `backend/core/orchestrator.py`

- **class `SelfHealingOrchestrator`**
  - methods: `load_learning`, `save_learning`, `self_modify`, `run_forever`
- `start_orchestrator()`

### `backend/core/os_bridge.py`

Enterprise Module: backend/core/os_bridge.py
Part of the Darwinistic Merge.

- `init_module()`

### `backend/core/pattern_recognition.py`

- **class `PatternRecognitionEngine`** — PHASE 26: THE LOGIT DATABASE & PATTERN ENGINE
  - methods: `_initialize_db`, `extract_features`, `map_multi_dimensional_geometry`, `store_pattern`, `identify_environmental_parameters`

### `backend/core/pedagogy.py`

- **class `ScientificMethod`** — Implements the 5-Step Scientific Pedagogy:
  - methods: `run_cycle`, `log_report`
- **class `ScryptPyramid`** — Hierarchical Hashing for Metropolis Validation.
  - methods: `add_block`, `_bubble_up`, `mine_pyramid`
- `start_pedagogy_loop()`
- `start_pyramid_loop()`

### `backend/core/placement_agent.py`

- **class `PlacementLogicGate`** — Pillar IV: The Logic Gate.
  - methods: `_evaluate_continuity`, `route_task`, `process_manifest_loop`

### `backend/core/populate_ghost_db.py`

- `populate_ghost_db()`

### `backend/core/predictive_engine.py`

- **class `PredictiveCodeEngine`** — PHASE 32: THE PREDICTIVE CODE ENGINE (LSTM + RAG)
  - methods: `hydrate_with_wisdom`, `hydrate`, `predict_next_token`, `speak_code`, `code_on_code_multiplier`

### `backend/core/preflight_engine.py`

- **class `PreflightEngine`** — THE PREFLIGHT ENGINE (PHASE 35):
  - methods: `_init_genetic_prompts`, `get_evolved_prompt`, `mutate_prompt`, `run_preflight_cycle`
- `start_preflight_loop()`

### `backend/core/preflight_wrapper.py`

- **class `JavaFXPreflightWrapper`** — Structural check that ensures all merged Python backend logic is structurally
  - methods: `generate_sha256`, `check_syntax_and_structure`, `run_preflight`

### `backend/core/process_manager.py`

- **class `ProcessManager`** — Step 27: Clean Slate Process Manager.
  - methods: `cleanup_zombies`

### `backend/core/progression.py`

- **class `ProgressionEngine`**
  - methods: `load_roadmap`, `evaluate_promotion`, `get_building_bonus`, `add_agent_xp`, `apply_genetic_upgrade`, `get_agent_title`, `unlock_next_feature`, `apply_feature_logic`, `get_state`

### `backend/core/proot_controller.py`

- **class `ProotController`** — PROOT CONTROLLER:
  - methods: `execute_in_sandbox`, `get_sandbox_status`

### `backend/core/proposal_table.py`

- **class `ProposalTable`** — HEADLESS PROPOSAL TABLE:
  - methods: `_init_db`, `submit_proposal`, `get_pending_proposals`, `update_status`

### `backend/core/quantum_core.py`

- **class `QuantumCore`**
  - methods: `update_attributes`, `process_agent_stability`, `update_core_assignment`, `trigger_hammer_event`, `flush_dirty_pages`, `update_access_time`, `mark_page_dirty`, `update_physical_telemetry`, `cycle`

### `backend/core/qwen_assembly.py`

- **class `QwenAssemblyLine`** — PHASE 18: THE CIRCLE OF AGENTS
  - methods: `add_project`, `run_loop`, `idle_banter`
- `start_assembly_loop()`

### `backend/core/qwen_ide.py`

- **class `QwenIDEWrapper`** — QWEN-IDE WRAPPER (PHASE 15-17):
  - methods: `propose_coding_task`, `run_slow_burn_cycle`, `promote_to_production`, `get_staged_tasks`
- `start_qwen_ide_loop()` — Slow-Burn Loop: 1 task at a time, very slowly.

### `backend/core/real_machine_bridge.py`

- **class `RealMachineBridge`**
  - methods: `_telemetry_worker`, `get_actual_metrics`

### `backend/core/registry_bridge.py`

Enterprise Module: backend/core/registry_bridge.py
Part of the Darwinistic Merge.

- `init_module()`

### `backend/core/research_center.py`

- **class `ResearchCenter`** — SimsMerged Research Center:
  - methods: `get_research_state`, `ping_public_hooks`, `run_lean_sigma_competitions`, `wizardry_programming_contest`, `start_research_loop`

### `backend/core/research_synthesis.py`

- **class `SynthesisEngine`** — PHASE 10: MARKOV-SHANNON RESEARCH SYNTHESIS
  - methods: `tandem_ask_tell`, `generate_comprehensive_paper`

### `backend/core/resource_governor.py`

- **class `ResourceGovernor`** — PHASE 27: THE RESOURCE GOVERNOR & SELF-HEALING WATCHDOG
  - methods: `start`, `stop`, `_monitor_loop`, `_check_service_health`

### `backend/core/session_harvester.py`

- **class `SessionHarvester`** — SESSION HARVESTER:
  - methods: `_load_todos`, `harvest_mandates`, `_save_todos`

### `backend/core/shadow_journalist.py`

- **class `ShadowJournalist`** — THE SHADOW JOURNALIST (VOTED FEATURE):
  - methods: `publish_ledger`
- `start_journalist_loop()`

### `backend/core/si_inhibitor.py`

[2026-05-17T18:05:22.452Z] [SimsMerged-v1.3-Metropolis] [Gemini-CLI-Architect]
SYSTEM INTEGRITY INHIBITOR - BLOCK 3

- **class `InhibitorEngine`**
  - methods: `attemptBinding`

### `backend/core/slow_auditor.py`

- **class `SlowAuditor`** — THE SLOW AGENT (AUDITOR):
  - methods: `audit_cycle`
- `start_auditor_loop()`

### `backend/core/sovereign_player.py`

- **class `SovereignPlayer`** — Simulates agents 'playing' the game.
  - methods: `simulate_movement`, `agent_play_loop`
- `start_sovereign_play_loop()`

### `backend/core/speed_run_engine.py`

- **class `NocturnalSpeedRunEngine`**
  - methods: `initialize_agent_sandbox`, `execute_darwin_test`, `hourly_discussion_and_vote`, `start_nocturnal_loop`, `get_weekly_loser`

### `backend/core/stress_test_synthesis.py`

- `run_stress_test()`

### `backend/core/symbolic_router.py`

- **class `SymbolicRouter`** — PHASE 25: THE LEARNING SYMBOLIC ROUTER
  - methods: `route_request`

### `backend/core/task_watchdog.py`

- **class `TaskWatchdog`** — TASK WATCHDOG:
  - methods: `run_watchdog_loop`
- `start_watchdog_task(model_orchestrator)`

### `backend/core/test_bm25.py`

- `test_search()`

### `backend/core/test_slm_e2e.py`

- `wait_for_server()` — Ensure the SLM server is responsive before running tests.
- `test_inference_basic()` — Tests basic prompt generation.
- `test_throttling_logic()` — Tests the 10-minute throttle mandate.
- `test_mmap_fenced_response_format()` — Verifies the response contains expected telemetry fields (eval_count, etc).

### `backend/core/test_sovereignty.py`

- **class `TestSovereignty`** — Manages the lifecycle of agent-written tests.
  - methods: `propose_invention`, `execute_test`

### `backend/core/treasury.py`

- **class `TreasurySystem`** — PHASE 35: TREASURY POINT & DePIN ECONOMY
  - methods: `_load_ledger`, `_save_ledger`, `reward_agent`, `get_balance`, `secure_genetic_transfer`

### `backend/core/validation_agent.py`

- `validate_research_paper(file_path)` — Step 24: Validates word count and cohesion of the research paper.

### `backend/core/vector_engine.py`

- **class `VectorEngine`**
  - methods: `load_store`, `save_store`, `get_embedding`, `add_document`, `search`

### `backend/core/vector_ring.py`

- **class `VectorRingDB`** — PHASE 24: THE VECTOR RING (SOVEREIGN MEMORY)
  - methods: `store_pattern`, `query_logic`

### `backend/core/vulnerability_researcher.py`

- **class `VulnerabilityResearcher`** — THE VULNERABILITY RESEARCHER (VOTED FEATURE):
  - methods: `run_research_cycle`
- `start_researcher_loop()`

### `backend/core/watchdog_a.py`

- `check_process_running(process_name)`
- `main()`

### `backend/core/watchdog_orchestrator.py`

- **class `CppServerWatchdog`** — Extends the TripleWatchdog to specifically orchestrate the C++ SLM Server.
  - methods: `check_process_responsiveness`
- `start_orchestration()`

### `backend/core/wisdom_tree.py`

- **class `WisdomTree`** — THE WISDOM TREE (PHASE 17):
  - methods: `_load_tree`, `_save_tree`, `store_wisdom`, `get_summary`, `get_wisdom`, `search_wisdom`, `get_efficiency_mult`

### `backend/core/wrapped_db.py`

- **class `WrappedDatabase`** — PERSISTENT WRAPPED LOGIC:
  - methods: `_init_db`, `record_choice`, `store_verified_code`, `check_verified_code`

### `backend/darwin_mutator.py`

- **class `DarwinMutator`**
  - methods: `_init_registry`, `mutate_prompt`

### `backend/data_engineering/analytics_dashboard.py`

- **class `AnalyticsEngine`**
  - methods: `get_depin_economy_stats`, `get_anonymized_export`
- `economy_endpoint()`
- `export_endpoint()`

### `backend/data_engineering/arrow_logger.py`

- **class `TelemetryLogger`**
  - methods: `log_event`, `flush_to_parquet`

### `backend/data_engineering/career_profile.py`

- **class `PDFReport`**
  - methods: `header`, `footer`
- **class `Profiler`**
  - methods: `generate_career_pdf`

### `backend/evolution_council.py`

- **class `EvolutionCouncil`**
  - methods: `collect_errors`, `conduct_vote`, `additive_commit`

### `backend/extensibility_hooks.py`

- **class `PluginManager`**
  - methods: `register_webhook`, `broadcast_event`
- **class `SlashCommandParser`** — Step 74: Build custom command `/slash` parser for Tok Tree.
  - methods: `parse_command`

### `backend/feature_factory.py`

- **class `FeatureFactory`**
  - methods: `implement_scout`, `implement_aggregator`

### `backend/inventory_system.py`

- **class `InventorySystem`**
  - methods: `_init_db`, `add_item`, `get_inventory`, `gather_resource`

### `backend/kernel_hardener.py`

- **class `KernelHardener`**
  - methods: `harden_process`

### `backend/logit_fusion.py`

- **class `LogitFusion`**
  - methods: `fuse_logits`

### `backend/logit_simulator.py`

- `simulate_logits()`

### `backend/mailbox_router.py`

- **class `MailboxRouter`**
  - methods: `initialize_agent_mailbox`, `send_email`, `get_unread_count`

### `backend/main.py`

- **class `UserMessageRequest`**
- **class `SyncPayload`**
- **class `AgentActionUpdate`**
- **class `InventionPayload`**
- **class `OSCommandRequest`**
- `update_agent_action(req)`
- `trigger_hyper_synthesis(project_name, objective, language)`
- `joint_synthesis(agent1_id, agent2_id, project_name, objective)` — PHASE 25: Joint Synthesis Mandate - Requires two agents to reach consensus.
- `get_action_db_stats()`
- `manual_nit_test(agent_id)`
- `get_master_todos()`
- `get_neural_health()`
- `trigger_vision_grade()`
- `get_grid_trends()`
- `trigger_final_genesis()`
- `trigger_harvest()`
- `trigger_asset_synthesis(name, desc)`
- `get_asset_gallery()`
- `get_agent_profile(agent_id)`
- `reassign_agent(agent_id, role)`

### `backend/master_unification.py`

- `run_unification()`

### `backend/object_pooler.py`

- **class `ObjectPool`**
  - methods: `acquire`, `release`

### `backend/pathfinder.py`

- **class `AStarPathfinder`**
  - methods: `heuristic`, `get_neighbors`, `find_path`

### `backend/pathfinder_v2.py`

- `execute_task()`

### `backend/physics_engine.py`

- **class `ThermalGrid`**
  - methods: `step`, `save_state`

### `backend/qa_harness/asset_auditor.py`

- **class `AssetAuditor`**
  - methods: `run_audit`

### `backend/qa_harness/visual_baseline.py`

- `capture_gui_baseline()` — Step 21.3: Snapshot Task.

### `backend/scout_agent.py`

- `scout_decompose_goals(world_map_json, global_goal)` — Decomposes a large goal (e.g. 'Build Cabin') into micro-tasks.

### `backend/security_core.py`

- **class `SecurityManager`** — Handles core security functions for the backend.
  - methods: `generate_jwt`, `verify_jwt`, `encrypt_payload`, `decrypt_payload`
- `configure_app_security(app)` — Step 63: Enforce strict CORS policies & Step 67: IP rate limiting.

### `backend/shannon_evolution.py`

- **class `ShannonDarwinEngine`**
  - methods: `calculate_shannon_entropy`, `identify_high_surprise_context`, `run_population_pruner`

### `backend/skill_crystallizer.py`

- **class `SkillCrystallizer`**
  - methods: `crystallize_module`

### `backend/sprite_triplet/config.py`

- **class `TripletConfig`**

### `backend/sprite_triplet/depin_wallet.py`

- **class `DePINLedger`**
  - methods: `get_db_connection`, `_initialize_db`, `_generate_tx_hash`, `generate_sovereign_address`, `fund_wallet`, `get_agent_lifespan_data`, `extend_lifespan`, `get_all_lifespan_stats`, `charge_compute_fee`

### `backend/sprite_triplet/ide_mock.py`

- **class `CodeSubmission`**
- `submit_code(submission)` — Intercepts the code payload from L3 Smoll, validates structure,

### `backend/sprite_triplet/pedagogy_memory.py`

- **class `HybridCodeSearch`**
  - methods: `_initialize_db`, `_load_sparse_state`, `_hash_code`, `log_performance`, `ingest_code`, `hybrid_search`

### `backend/sprite_triplet/script_pyramid.py`

- **class `ScriptPyramid`**
  - methods: `get_db_connection`, `_initialize_db`, `submit_script`, `execute_in_sandbox`, `_update_script_stats`

### `backend/sprite_triplet/tests/test_cascade.py`

- `test_triplet_cascade()` — Tests the full flow from L1 macro instruction down to the L3 payload creation.
- `test_l1_macro()`
- `test_l2_orchestrator()`
- `test_l3_smoll()`

### `backend/sprite_triplet/tok_tree.py`

- **class `TokTree`** — Genetically advanced SSD-fenced Tok Tree (RAG Context Wrapper).
  - methods: `load_tree`, `save_tree`, `insert_context`, `augment_prompt`

### `backend/sprite_triplet/topological_wrapper.py`

- **class `TopologicalGrid`**
  - methods: `assign_agent_coordinate`, `_get_zone_path`, `calculate_travel_cost`, `validate_write_permission`, `cross_zone_read`

### `backend/sprite_triplet/triplet.py`

- **class `SpriteTriplet`**
  - methods: `invoke_ollama`, `l1_macro_process`, `l2_orchestrator_process`, `l3_smoll_process`, `run_cascade`

### `backend/sprite_triplet/triplet_fenced_server.py`

- **class `CascadeRequest`**
- **class `SteerRequest`**
- **class `LabRequest`**
- `startup_event()`
- `shutdown_event()`
- `run_lab_test(request)` — Conducts a Geometric Stress Test on code.
- `run_thumb_vars(request)` — Automates variable thumbing in code/data.
- `start_research(topic, agent_id)` — Starts the multi-chapter synthesis process (Phase 7).
- `run_cascade(request)` — Executes the ARCHITECT -> TRANSLATOR -> CODER cascade.
- `steer_query(request)` — Manual trigger for the Omniscient Steer.
- `get_telemetry_geometry()` — Returns the latest geometric manifold analysis of the system.
- `run_qwen_cli(command, tags)` — Executes a command via the Qwen Coder CLI wrapper.

### `backend/sprite_triplet/triton_ssd_fence.py`

- **class `SSDVirtualFence`**
  - methods: `hook_create_file_mapping`, `map_view_of_file`, `slow_burn_throttle`, `run_garbage_collector`

### `backend/stress_test_swarm.py`

- **class `SwarmStressTester`**
  - methods: `agent_lifecycle`, `monitor_performance`, `run_swarm`

### `backend/test_factory.py`

- **class `TestFactory`**
  - methods: `generate_boilerplate_test`, `resolve_holes`

### `backend/tests/test_agent_fsm.py`

- `test_initialization()` — Automated Init Verification for agent_fsm
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_agent_lifecycle_simulator.py`

- `test_initialization()` — Automated Init Verification for agent_lifecycle_simulator
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_agent_movement_simulator.py`

- `test_initialization()` — Automated Init Verification for agent_movement_simulator
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_aggregator_agent.py`

- `test_initialization()` — Automated Init Verification for aggregator_agent
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_atc_coordinator.py`

- `test_initialization()` — Automated Init Verification for atc_coordinator
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_auction_system.py`

- `test_initialization()` — Automated Init Verification for auction_system
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_autonomous_completion_engine.py`

- `test_initialization()` — Automated Init Verification for autonomous_completion_engine
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_autonomous_reaper.py`

- `test_initialization()` — Automated Init Verification for autonomous_reaper
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_axiomatic_checker.py`

- `test_initialization()` — Automated Init Verification for axiomatic_checker
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_bug_hunter.py`

- `test_initialization()` — Automated Init Verification for bug_hunter
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_chrono_manager.py`

- `test_initialization()` — Automated Init Verification for chrono_manager
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_consensus_engine.py`

- `test_initialization()` — Automated Init Verification for consensus_engine
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tests/test_evolution_council.py`

- `test_initialization()` — Automated Init Verification for evolution_council
- `test_structural_integrity()` — Verifies module properties match the Master Book mandates.

### `backend/tok_communications/chat_extractor.py`

- **class `ChatExtractor`**
  - methods: `extract_coordinate_change`, `extract_compiler_error`, `extract_depin_update`, `_push_to_chat`

### `backend/tok_communications/inner_tok_layer.py`

- **class `InnerTokDaemon`**
  - methods: `get_db_connection`, `_initialize_db`, `_analyze_sentiment`, `intercept_payload`

### `backend/tok_communications/msn_metropolis.py`

- **class `ConnectionManager`**
  - methods: `connect`, `disconnect`, `broadcast`
- `hardware_telemetry_loop()` — Broadcasts real-machine hardware telemetry to the JavaFX HUD.
- `startup_event()`
- `websocket_endpoint(websocket, client_id)`
- `process_slash_command(client_id, command)`
- `update_agent(update)`

### `backend/tok_communications/pulse_core.py`

- **class `GlobalPulse`**
  - methods: `pause_system`, `resume_system`, `_economic_tick`, `_sprite_sync_tick`, `pulse_loop`

### `backend/tok_communications/tok_tree.py`

- **class `TaskNode`**
  - methods: `add_dependency`, `can_execute`
- **class `TokTreeDAG`**
  - methods: `add_task`, `link_dependency`, `assign_task`, `complete_task`

### `backend/tok_tower_core.py`

- **class `ToKTowerCore`**
  - methods: `_initialize_arena`, `_get_node_offset`, `pack_node`, `insert_node`, `traverse`, `teardown`

### `backend/training_routine.py`

- **class `TrainingRoutine`**
  - methods: `log`, `run_genetic_darwin_epoch`, `start_training`

### `backend/ui_validator.py`

- `validate_ui_throughput()` — Step 5.3: UI Validation.

### `backend/world_genesis.py`

- **class `WorldGenerator`**
  - methods: `generate`, `save_to_json`

### `clean_slate_restart.py`

- `kill_processes()` — Step 27: Clean Slate Process Manager.
- `restart_metropolis()`

### `ingest_anchors.py`

- `ingest_high_value_anchors()`

### `run_backend.py`

- `auto_launch_browser()` — Closes old browser tabs/windows and opens the SimsMerged city frontend.

### `skills/clawhub-bridge/scripts/bridge_to_clawhub.py`

- `bridge_sync()`

### `src/database.py`

- **class `Database`**
  - methods: `create_tables`, `insert_sim`, `get_sims`

### `src/main.py`

- `main()`

### `src/utils/critic.py`

- **class `GeneticCritic`** — Step 1201: The Genetic Critic
  - methods: `scan_project`, `analyze_file`, `refactor_python`, `refactor_java`, `report`

### `test_metropolis_core.py`

- `test_metropolis_core()`

### `test_ollama_speed.py`

- `test_ollama()`

### `tests/e2e_runner.py`

[2026-05-21T18:45:30.452Z] [SimsMerged-v1.3] [Gemini-CLI-Architect]
METROPOLIS E2E RUNNER - ARCHITECTURAL BLUEPRINT

- `run_metropolis_heartbeat_check()` — Verifies backend and grid stability.

### `tools/agent_registrar_tool.py`

Enterprise Module: tools/agent_registrar_tool.py
Part of the Darwinistic Merge.

- `init_module()`

### `tools/generate_tracker.py`

- `generate_table()`

### `tools/overhaul_logic_table.py`

- `overhaul_logic()`

### `tools/task_mgr_mini.py`

Enterprise Module: tools/task_mgr_mini.py
Part of the Darwinistic Merge.

- `init_module()`

### `triple_watchdog.py`

- `log_event(msg, file)`
- `check_system_health()` — Monitors CPU and alerts if too high.
- `run_authority()` — Starts the Metropolis Authority as a persistent background process.

### `unused/vision_engine.py`

- **class `MetropolisVision`**
  - methods: `capture_state`
- `vision_loop()` — Background loop for periodic visual verification.

## Public API index

| Module | Function | Signature |
|--------|----------|-----------|
| `agent_lifecycle_simulator` | `simulate_agent_lifecycle` | `simulate_agent_lifecycle(agent_id, start_pos, target_pos)` |
| `agent_memory` | `get_agent_memory` | `get_agent_memory(agent_id)` |
| `agent_movement_simulator` | `simulate_agent_movement` | `simulate_agent_movement(agent_id, start_pos, target_pos)` |
| `agent_registrar` | `update_agents` | `update_agents()` |
| `agent_registrar_tool` | `init_module` | `init_module()` |
| `agentic_github_suite` | `start_github_governor_loop` | `start_github_governor_loop()` |
| `aggregation_utils` | `aggregation_utils` | `aggregation_utils(stateMachine, scoreSum)` |
| `aggregator_agent` | `aggregate_metropolis_economy` | `aggregate_metropolis_economy(agent_inventories)` |
| `algorithmic_mayor` | `start_mayor_loop` | `start_mayor_loop()` |
| `analytics_dashboard` | `economy_endpoint` | `economy_endpoint()` |
| `analytics_dashboard` | `export_endpoint` | `export_endpoint()` |
| `ascension_spark` | `ignite_ascension` | `ignite_ascension()` |
| `auction_system` | `run_auction` | `run_auction(task_name, task_type)` |
| `bridge_to_clawhub` | `bridge_sync` | `bridge_sync()` |
| `business_school` | `start_business_school_loop` | `start_business_school_loop()` |
| `clean_slate_restart` | `kill_processes` | `kill_processes()` |
| `clean_slate_restart` | `restart_metropolis` | `restart_metropolis()` |
| `coder_bot` | `start_coder_bot_loop` | `start_coder_bot_loop()` |
| `config` | `add_log` | `add_log(msg, level)` |
| `config` | `add_message` | `add_message(sender, text, hash_val)` |
| `config` | `load_metropolis_state` | `load_metropolis_state()` |
| `config` | `sandbox_guard` | `sandbox_guard(path)` |
| `config` | `save_metropolis_state` | `save_metropolis_state()` |
| `darwinian_orch` | `start_banter_loop` | `start_banter_loop()` |
| `data_syphon_epmo` | `start_epmo_loop` | `start_epmo_loop()` |
| `digital_twin_planner` | `start_twin_loop` | `start_twin_loop()` |
| `e2e_runner` | `run_metropolis_heartbeat_check` | `run_metropolis_heartbeat_check()` |
| `endpoints` | `get_agents` | `get_agents()` |
| `factory_orch` | `start_factory_loop` | `start_factory_loop()` |
| `generate_tracker` | `generate_table` | `generate_table()` |
| `github_harvester` | `start_github_harvest` | `start_github_harvest()` |
| `headless_asset_sync` | `sync_assets` | `sync_assets()` |
| `headless_ast_analyzer` | `analyze_ast` | `analyze_ast(filepath)` |
| `headless_pkg_manager` | `run_pkg_command` | `run_pkg_command(command_str)` |
| `headless_pkg_manager` | `verify_install` | `verify_install(pkg_type, name)` |
| `headless_security_scanner` | `scan_security` | `scan_security(filepath)` |
| `hydrate_continuity` | `hydrate` | `hydrate()` |
| `ide_mock` | `submit_code` | `submit_code(submission)` |
| `ideator_agent` | `start_ideation_loop` | `start_ideation_loop()` |
| `ingest_anchors` | `ingest_high_value_anchors` | `ingest_high_value_anchors()` |
| `llm_client` | `project_danube_inference` | `project_danube_inference(state_vector, temp, top_p, query_tags)` |
| `llm_client` | `query_rag_chunk` | `query_rag_chunk(query_tags, language)` |
| `llm_client` | `softmax` | `softmax(logits, temp)` |
| `logic_engine_extension` | `logic_engine_extension` | `logic_engine_extension(sys_dict)` |
| `logit_simulator` | `simulate_logits` | `simulate_logits()` |
| `main` | `admin_root_authority_loop` | `admin_root_authority_loop()` |
| `main` | `analytics_rollup_task` | `analytics_rollup_task()` |
| `main` | `assign_zoning` | `assign_zoning(x1, y1, x2, y2, type)` |
| `main` | `branch_issue` | `branch_issue(issue_title)` |
| `main` | `broadcast_chrono` | `broadcast_chrono(state)` |
| `main` | `cast_vote` | `cast_vote(candidate_id)` |
| `main` | `clippy_authority_task` | `clippy_authority_task()` |
| `main` | `clippy_manual_throttle` | `clippy_manual_throttle(agent_id, level)` |
| `main` | `clippy_pin_core` | `clippy_pin_core(agent_id, core)` |
| `main` | `daily_integrity_test_task` | `daily_integrity_test_task()` |
| `main` | `execute_invention_test` | `execute_invention_test(invention_id)` |
| `main` | `execute_os_command` | `execute_os_command(req)` |
| `main` | `extend_agent_lifespan` | `extend_agent_lifespan(agent_id, hours)` |
| `main` | `genetic_exchange` | `genetic_exchange(agent_a, agent_b)` |
| `main` | `get_action_db_stats` | `get_action_db_stats()` |

## Status

- Branch: `master`
- Last commit: 2026-06-28 16:15:08 -0600
- File types: .mut ×3942, .sql ×1841, .json ×549, .md ×67, .png ×62, .java ×37, .ps1 ×32, .js ×30

### Recent commits
```
68d4c919 [Moe autonomous] SimsMerged 2026-06-28 16:15
2c8b2323 [Moe autonomous] SimsMerged 2026-06-27 04:24
e4658a0d [Moe autonomous] SimsMerged 2026-06-26 09:01
ebde154e [Moe autonomous] SimsMerged 2026-06-20 15:36
8121820f [Moe autonomous] SimsMerged 2026-06-20 14:57
90002df3 [Moe autonomous] SimsMerged 2026-06-20 14:07
928af4ed [Moe autonomous] SimsMerged 2026-06-20 12:27
bfb65ce7 [Moe autonomous] SimsMerged 2026-06-20 11:39
```

---
*README generated by `readme_generator.py` (Viper). Deterministic — derived from source, not LLM prose.*