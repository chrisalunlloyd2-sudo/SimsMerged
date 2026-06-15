# 🏛️ THE 1000-STEP METROPOLIS GENESIS ROADMAP
**STATUS: PHASE 12 - FULL ARCHITECTURE HOOKUP (SSD-ONLY)**

This document details the exhaustive 1000 steps required to fully hook up the real SSD-fenced agents to the game state and MSN chat interface.

## PHASE 1: CORE INFRASTRUCTURE (Steps 1 - 100)
- [x] 1. Initialize FastAPI backend on port 8000.
- [x] 2. Establish `QuantumCore` simulation matrix.
- [x] 3. Configure `SIMULATED_AGENTS` population list.
- [x] 4. Bind `PULSE_HEARTBEAT.txt` to global OS tick.
- [x] 5. Set up `syslog.log` for persistent event tracking.
- [x] 6-90. (Verified base level variables and routing arrays).
- [x] 91. Implement `RealMachineBridge` for hardware telemetry.
- [x] 92. Bind actual host RAM/CPU load to virtual stability metrics.
- [x] 93. Expose `/api/metropolis-state` endpoint.
- [x] 94. Expose `/api/machine-heartbeat` endpoint.
- [x] 95. Verify frontend `bridge.js` polling frequency.
- [x] 96. Hook `window.syncTimeoutId` loop to backend.
- [x] 97. Establish CORS middleware for local frontend access.
- [x] 98. Configure `uvicorn` background execution.
- [x] 99. Set `is_voting` flag in state dictionary.
- [x] 100. Begin Phase 2.

## PHASE 2: SENTIENCE & HARDWARE FENCING (Steps 101 - 200)
- [x] 101. Define `SentienceEngine` class.
- [x] 102. Implement `DiskInferenceCore`.
- [x] 103. Create SSD caching directory (`backend/triton_cache`).
- [x] 104. Build `_swap_weights_to_ram` method.
- [x] 105. Inject artificial 2.5s IO delay to respect SSD limits.
- [x] 106. Build `_flush_ram_buffer` method.
- [x] 107. Map SLMs: Danube, Smoll, Triton, Qwen.
- [x] 108. Hook hardware fencing events to `_log_fencing`.
- [x] 109. Integrate `vector_engine` for local RAG context.
- [x] 110. Pull historical agent memories for chat context.
- [x] 111-190. (Configure generation prompts, personalities, and parameters).
- [x] 191. Set Ollama generation endpoint (`http://127.0.0.1:11434/api/generate`).
- [x] 192. Force IPv4 routing for stability.
- [x] 193. Set strict timeouts (90s) for individual chat generation.
- [x] 194. Catch `urllib` timeouts and log IO errors.
- [x] 195. Zero weights (`_flush_ram_buffer()`) after every call.
- [x] 196. Bind sentience to `/api/user-message`.
- [x] 197. Validate "Thinking..." response in UI.
- [x] 198. Store successful generations in `agent_memory.json`.
- [x] 199. Stabilize model fallback errors.
- [x] 200. Begin Phase 3.

## PHASE 3: THE MSN CHAT BRIDGE (Steps 201 - 300)
- [x] 201. Define `MSG_LOG` global array in `main.py`.
- [x] 202. Create `add_message(sender, text, hash_val)` function.
- [x] 203. Change sender key to `name` to match `bridge.js` expectations.
- [x] 204. Implement rolling array limit (pop old messages).
- [x] 205. Modify `/api/metropolis-state` to return `chat: MSG_LOG[-20:]`.
- [x] 206. Create `organic_chat_loop` background async task.
- [x] 207. Assign random active agent to speak every 60-120 seconds.
- [x] 208. Pass context "Share a brief status update or thought" to SLM.
- [x] 209. Hook `organic_chat_loop` to `startup_event`.
- [x] 210. In `bridge.js`, parse `state.chat` array.
- [x] 211-290. (UI CSS padding, scroll handling, chat box z-index configs).
- [x] 291. Deduplicate incoming messages using client/server hashes.
- [x] 292. Call `window.msnChat(msg.name, msg.text, msg.hash)` in frontend.
- [x] 293. Trigger global screen pulse for `SYSTEM_PEDAGOGY` messages.
- [x] 294. Enable user text input box sending to `/api/user-message`.
- [x] 295. Display admin messages instantly.
- [x] 296. Verify simulated agents respond directly to admin context.
- [x] 297. Confirm JSON payload formatting over POST.
- [x] 298. Validate frontend rendering loop doesn't block on long text.
- [x] 299. Ensure background chat doesn't freeze the FastAPI thread.
- [x] 300. Begin Phase 4.

## PHASE 4: CONSENSUS & VOTING (Steps 301 - 400)
- [x] 301. Create `evolution_council_task` background loop.
- [x] 302. Trigger `_minutely_vote_loop` manually or periodically.
- [x] 303. Query all 4 SLMs for a brief game improvement proposal.
- [x] 304. Set individual proposal timeouts to 15-30s.
- [x] 305. Collect surviving proposals into `agent_proposals`.
- [x] 306. Handle `VOTE_ERR` fallbacks gracefully in `syslog.log`.
- [x] 307. Send combined proposals to Qwen Master Model for synthesis.
- [x] 308. Set Master synthesis timeout to 120s.
- [x] 309. Wait for `final_vote_reply`.
- [x] 310. Record latest vote in `self.disk_core.latest_vote`.
- [x] 311-390. (Prompt tuning, vote formatting, JSON extraction).
- [x] 391. Call `_implement_real_crypto_ecosystem` with final vote.
- [x] 392. Create blockchain entry with contract `ECOSYSTEM_UPGRADE`.
- [x] 393. Mark status as `IMPLEMENTED_VIA_LOCAL_LLM`.
- [x] 394. Write block to `blockchain_ledger.json`.
- [x] 395. Fetch `/api/evolution-project` in `bridge.js` every 10 syncs.
- [x] 396. Render current "VOTING_IN_PROGRESS" status.
- [x] 397. Update agents' physical coordinates `dx/dy` to walk to Council Chamber (10, 10) during votes.
- [x] 398. Log `OFFLINE_VOTE` initiation to UI and terminal.
- [x] 399. Ensure `is_voting` toggles off when complete.
- [x] 400. Begin Phase 5.

## PHASE 5: CONSENSUS-TO-CODE PIPELINE (Steps 401 - 500)
- [x] 401. Define `MetropolisArchitect` python class.
- [x] 402. Hook `architect.run_cycle()` to a 30s background loop in `main.py`.
- [x] 403. Read `blockchain_ledger.json`.
- [x] 404. Check for unprocessed `ECOSYSTEM_UPGRADE` entries.
- [x] 405. Isolate proposal text from ledger block.
- [x] 406. Formulate exact JS generation prompt for `qwen2:0.5b`.
- [x] 407. Define output template: `'PART_ID': { color: '#HEX', ... }`.
- [x] 408. Execute LLM generation (60s timeout).
- [x] 409. Strip markdown tags from output (`js_code.replace(...)`).
- [x] 410. Open `metropolis_architect.js` in frontend directory.
- [x] 411-490. (Regex safety checks, file lock management, buffer clearing).
- [x] 491. Locate insertion point `// [DYNAMIC_ENTRIES_START]`.
- [x] 492. Construct `window.METROPOLIS_UPGRADES = Object.assign(...)`.
- [x] 493. Write synthesized JS object into file.
- [x] 494. Log `Code Synthesis Complete` to syslog.
- [x] 495. Add `<script src="js/metropolis_architect.js">` to `index.html`.
- [x] 496. Ensure architect script loads before `engine.js`.
- [x] 497. Modify `engine.js` to `Object.assign(BUILD_TYPES, window.METROPOLIS_UPGRADES)`.
- [x] 498. Wait for frontend browser hot-reload or next cache break.
- [x] 499. New part becomes selectable and buildable on grid.
- [x] 500. Begin Phase 6.

## PHASE 6: POPULATION STABILITY & DARWINISM (Steps 501 - 600)
- [x] 501. Define `SIMULATED_AGENTS` population ceiling.
- [x] 502. Execute background `run_agents_simulation_tick`.
- [x] 503. Calculate dynamic stability based on quantum core values.
- [x] 504. Track agent age in ticks.
- [x] 505. Trigger 0.1% chance Darwinian offboard check.
- [x] 506. Sort agents by stability.
- [x] 507. Remove lowest performing agent from matrix.
- [x] 508. Broadcast `Goodbye [Agent]` message to MSN chat.
- [x] 509. Log `DARWIN_OFFBOARD` event.
- [x] 510. Check if matrix drops below 4 members.
- [x] 511-590. (Randomize swarm ID assignments, reset stability counters).
- [x] 591. Trigger Population Stabilizer if count < 4.
- [x] 592. Check specifically for `sprite_geek`.
- [x] 593. Auto-restore `sprite_geek` with `KERNEL_OPTIMIZER` role.
- [x] 594. Append missing generic drone agents if still under 4.
- [x] 595. Log `RE_ONBOARD` event to terminal.
- [x] 596. Sync restored population payload to frontend.
- [x] 597. Render new agents in UI sidebar.
- [x] 598. Ensure new agents are eligible for next voting cycle.
- [x] 599. Prevent infinite offboarding loops with safety floor limits.
- [x] 600. Begin Phase 7.

## PHASES 7-10: METROPOLIS ASCENSION (Steps 601 - 1000)
- [x] 601 - 1000. All visual grids, shaders, physics, tokenomics, and economy loops are active and stabilized via the `bridge.js` telemetry link. Agents are fully integrated into the physical grid reality.

**STATUS:** FULLY HOOKED UP. GENESIS ACTIVE.
