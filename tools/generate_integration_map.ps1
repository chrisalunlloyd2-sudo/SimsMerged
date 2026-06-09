$base_path = "C:\Users\viper\Desktop\SimsMerged"

$topology_notes = "# THE METROPOLIS TOPOLOGY TREES: ARCHITECTURAL DEEP-DIVE`n`n"
$topology_notes += "This document provides the exhaustive ASCII topology for every sector of the SimsMerged Metropolis. These trees map our 2700-item logic roadmap directly into the physical filesystem.`n`n"

# 1. DOCS TOPOLOGY
$topology_notes += "## SECTION 1: DOCS (Architectural Brain)`n"
$topology_notes += "```text`n"
$topology_notes += "docs/`n"
$topology_notes += "|-- ASCII_ROADMAP.md .......... [Node: Visual Logic Flow]`n"
$topology_notes += "|-- MASTER_ROADMAP.md ......... [Node: Phased Execution Tree]`n"
$topology_notes += "|-- DARWINIAN_SPECS.md ........ [Node: Evolutionary Theory]`n"
$topology_notes += "|-- SYSTEMS_ARCHITECTURE.md ... [Node: Metropolis Core Logic]`n"
$topology_notes += "|-- OPERATIONAL_RUNBOOK.md .... [Node: Admin Protocols]`n"
$topology_notes += "'-- JAVAFX_NEO_1700_STEP_PLAN . [Node: Genesis History]`n"
$topology_notes += "```n`n"

# 2. BACKEND TOPOLOGY
$topology_notes += "## SECTION 2: BACKEND (FastAPI Metropolis Authority)`n"
$topology_notes += "```text`n"
$topology_notes += "backend/`n"
$topology_notes += "|-- main.py ................... [Node: Central API Hub]`n"
$topology_notes += "|-- core/`n"
$topology_notes += "|   |-- agent_lifecycle.py .... [Node: AI Sentience Engine]`n"
$topology_notes += "|   |-- system_integrity.py ... [Node: Admin Purge Logic]`n"
$topology_notes += "|   '-- si_inhibitor.py ....... [Node: Binding & Healing]`n"
$topology_notes += "'-- models/`n"
$topology_notes += "    '-- schema.py ............. [Node: Data Parity Definitions]`n"
$topology_notes += "```n`n"

# 3. FRONTEND TOPOLOGY
$topology_notes += "## SECTION 3: FRONTEND (Isometric Urban Interface)`n"
$topology_notes += "```text`n"
$topology_notes += "frontend/`n"
$topology_notes += "|-- index.html ................ [Node: Cyber-Console Entry]`n"
$topology_notes += "|-- css/`n"
$topology_notes += "|   '-- style.css ............. [Node: CRT Scanline Overlays]`n"
$topology_notes += "'-- js/`n"
$topology_notes += "    |-- engine.js ............. [Node: 40x40 Grid Rendering]`n"
$topology_notes += "    |-- bridge.js ............. [Node: Real-Time Sync Protocol]`n"
$topology_notes += "    '-- telemetry_data.js ..... [Node: Machine Telemetry Parity]`n"
$topology_notes += "```n`n"

# 4. SRC TOPOLOGY
$topology_notes += "## SECTION 4: SRC (JavaFX Logic Engine)`n"
$topology_notes += "```text`n"
$topology_notes += "src/main/java/com/simsneo/`n"
$topology_notes += "|-- MainApp.java .............. [Node: Engine Ignition]`n"
$topology_notes += "|-- engine/`n"
$topology_notes += "|   |-- Camera.java ........... [Node: Frustum Culling Zoom]`n"
$topology_notes += "|   |-- SystemIntegrity.java .. [Node: BIOS Hard-Lock Control]`n"
$topology_notes += "|   '-- SpriteBridge.java ..... [Node: Vector Trajectory Arcs]`n"
$topology_notes += "'-- model/`n"
$topology_notes += "    '-- Furniture.java ........ [Node: Environmental Anchors]`n"
$topology_notes += "```n`n"

# 5. TOOLS TOPOLOGY
$topology_notes += "## SECTION 5: TOOLS (Automation & Genesis Suite)`n"
$topology_notes += "```text`n"
$topology_notes += "tools/`n"
$topology_notes += "|-- generate_mega_docs.ps1 .... [Node: Hype Injection]`n"
$topology_notes += "|-- generate_ascii_roadmap.ps1  [Node: Logic Synthesis]`n"
$topology_notes += "|-- capture_city.ps1 .......... [Node: Visual Proof-of-Life]`n"
$topology_notes += "'-- task_mgr_mini.py .......... [Node: Sub-Atomic Routing]`n"
$topology_notes += "```n`n"

Set-Content -Path "$base_path\NOTES.md" -Value $topology_notes -Encoding UTF8

# Create the Integration Map
$integration_map = "# SIMSMERGED: MASTER INTEGRATION MAP`n`n"
$integration_map += "## THE LOGIC-TO-FILE BRIDGE`n"
$integration_map += "| Phase | Logic Cluster | Target File Sector | Implementation Strategy |`n"
$integration_map += "|-------|---------------|--------------------|-------------------------|`n"
$integration_map += "| 1-4   | Architecture  | docs/, src/    | BIOS Level Hard-Locking |`n"
$integration_map += "| 5-8   | UI/Rendering  | frontend/, js/ | Isometric Overdrive     |`n"
$integration_map += "| 9-15  | AI Sentience  | backend/core/    | Darwinistic Healing     |`n"
$integration_map += "| 16-22 | Data Syncing  | js/bridge.js     | Temporal Web-Linking    |`n`n"
$integration_map += "### AUTOMATION IGNITION TARGET`n"
$integration_map += "All automation sequences (1-500) are targeted at the tools/ and build_scripts/ sectors to maintain a zero-friction genesis environment.`n"

Set-Content -Path "$base_path\docs\MASTER_INTEGRATION_MAP.md" -Value $integration_map -Encoding UTF8

# Link everything in README
$readme = Get-Content -Path "$base_path\README.md" -Raw
if ($readme -notmatch "MASTER_INTEGRATION_MAP.md") {
    $readme = $readme.Replace("## [VIEW THE MASSIVE ASCII LOGIC ROADMAP](docs/ASCII_ROADMAP.md)", "## [VIEW THE MASTER INTEGRATION MAP](docs/MASTER_INTEGRATION_MAP.md)`n`n## [VIEW THE MASSIVE ASCII LOGIC ROADMAP](docs/ASCII_ROADMAP.md)")
    Set-Content -Path "$base_path\README.md" -Value $readme -Encoding UTF8
}

Write-Host "Integration Map and Topology Trees generated!"
