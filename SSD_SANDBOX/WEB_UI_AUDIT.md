# 🕵️ LEGACY WEB UI FEATURE AUDIT
**TIMESTAMP:** 2026-06-11T20:30:00.000Z
**PROJECT_ID:** Sims_JavaFX_Neo (Phase 18, Step 51)
**AGENT_ID:** viper_cli-architectssj4

## 📌 AUDIT OVERVIEW
An extensive audit of `C:\Users\viper\Desktop\SimsMerged\frontend` reveals several advanced Web UI components that must be ported to the JavaFX Neo engine to achieve feature parity.

## 📊 MISSING DATA VISUALIZATIONS & DASHBOARDS
1. **16-Core Virtual CPU Affinity Matrix:** 
   * Found in `resource_monitor.js`.
   * Features dynamic colored heatmaps for individual core loads.
   * *Target Implementation:* JavaFX Grid/Canvas inside the System Console.
2. **Historical Telemetry Charts:** 
   * Found in `resource_monitor.js`.
   * Real-time line charts tracking CPU and Memory usage over a 50-tick history.
   * *Target Implementation:* JavaFX LineChart.
3. **Urban Heat Island HUD:** 
   * Found in `gui_extensions.js`.
   * Displays "Core Temp" and "Albedo Rating" overlaid on the grid.
   * *Target Implementation:* Extend `com.simsneo.view.WorldRenderer` HUD.
4. **Agent Inspector Dossier:** 
   * Found in `index.html`.
   * In-depth profile tracking an agent's specific Wallet balance and Zone coordinates.

## ⚙️ MISSING CONTROL MECHANISMS
1. **Clippy Control Pad (Swarm Master Override):** 
   * Found in `gui_extensions.js`.
   * Actions: "BYPASS CONSENSUS", "FORCE HOT-PATCH", "HALT DEPIN SWARM".
   * *Target Implementation:* JavaFX God Mode Panel.
2. **Context Memory & Logit Controls:** 
   * Found in `gui_extensions.js`.
   * Buttons: "CLEAR_CONTEXT" (purges backend context memory) and "LOGIT_TRACKER".
3. **God Hand Controls:**
   * Found in `index.html`.
   * Actions: "PAUSE MATRIX", "SPAWN AGENT", "INJECT DEPIN".
   * *Target Implementation:* Extend JavaFX `SystemConsole`.

## 🚀 ACTION PLAN
Proceeding to Step 52 to isolate and port these legacy Web UI dashboards into JavaFX modular windows.