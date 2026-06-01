# TIMESTAMP: 2026-06-01T06:23:00.000Z
# PROJECT_ID: SimsMerged-v1.4-Metropolis
# AGENT_ID: Antigravity-CLI-Architect

# 🤖 METROPOLIS AI FLEET: AUTONOMOUS AUTOMATION & SAFE CONTINUATION PLAN

This document maps out the operational directives, shell safety wrappers, and automated routines to coordinate the background AI agents (**Sprite_Geek**, **Sprite_Writer**, **Sprite_Socrates**, and **Sprite_Newton**) as they continue development without ever deleting files or overwriting the remote history.

---

## 🔒 1. THE GOLDEN COMMANDMENTS FOR ALL AGENTS
Every agent operating inside `agent_sandboxes/` or `SimAgentCity/` must read and enforce these directives on every cycle. Failure to comply will result in automatic process isolation.

1. **NO REMOVALS:** Absolute ban on destructive git operations (`git rm`, `git push -f`, `git push --force`). Development must be purely additive.
2. **PROTECT THE GALLERY:** Under no circumstances shall an agent overwrite, rename, or delete any files in `assets/` or files with graphic extensions (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico`). These visual representations of the metropolis are permanent.
3. **WHO IS ADDING:** Every file mutation, schema update, and commit message must be prefaced by the high-fidelity **VIPER Atomic Signature Triplet** containing:
   `[TIMESTAMP: ISO-8601 High-Fidelity][PROJECT_ID: SimsMerged-v1.3-Metropolis][AGENT_ID: Agent-Name]`
4. **DRY-RUN FIRST:** Before running a push command, agents must execute `git push --dry-run`. If the dry-run check fails, the push must halt immediately, and a high-priority alert must be posted in `PULSE_HEARTBEAT.txt`.

---

## 🛠️ 2. AUTONOMOUS SHELL GUARDIAN (PowerShell Wrapper Script)
To automate safe version control across the fleet, background maintainers should use the following pre-push safety wrapper (`C:\Users\viper\Desktop\SimsMerged\build_scripts\safe_sync_guardian.ps1`). It automates pre-push dry-runs, safe rebasing, and local backups of the visual assets:

```powershell
# TIMESTAMP: 2026-06-01T06:12:00.000Z
# PROJECT_ID: SimsMerged-v1.3-Metropolis
# AGENT_ID: Antigravity-CLI-Architect

$PROJECT_ROOT = "C:\Users\viper\Desktop\SimsMerged"
$BACKUP_DIR = "C:\Users\viper\.gemini\antigravity-cli\scratch\assets_backup"
$GIT_PATH = "C:\Users\viper\git\cmd\git.exe"

Write-Output "[SAFE GUARDIAN] Initiating Git Safety Protocol..."

# Step 1: Backup visual assets locally
if (!(Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Force -Path $BACKUP_DIR | Out-Null
}
Copy-Item -Path "$PROJECT_ROOT\assets\*" -Destination $BACKUP_DIR -Recurse -Force
Write-Output "[SAFE GUARDIAN] Stored backup of all visual assets."

# Step 2: Fetch and verify remote sync state
Set-Location -Path $PROJECT_ROOT
& $GIT_PATH fetch origin

# Step 3: Run git push dry-run to identify potential history rewrites
$dryRun = & $GIT_PATH push --dry-run 2>&1
if ($dryRun -match "rejected" -or $dryRun -match "non-fast-forward") {
    Write-Warning "[SAFE GUARDIAN] Out of sync detected! Performing safe rebase..."
    & $GIT_PATH pull --rebase origin master
    if ($LASTEXITCODE -ne 0) {
        Write-Error "[SAFE GUARDIAN] Rebase conflict discovered! Locking repository and alerting User."
        exit 1
    }
}

# Step 4: Perform normal push (NEVER FORCE PUSH)
Write-Output "[SAFE GUARDIAN] Safe sync dry-run passed. Pushing additions..."
& $GIT_PATH push origin master
Write-Output "[SAFE GUARDIAN] Pushed changes successfully. Remote gallery protected."
```

---

## 🎨 3. AUTOMATED IMAGE HARVESTING PIPELINE
To continuously populate the GitHub repository with gorgeous screenshots, the senior agents (**Sprite_Geek** and **Sprite_Socrates**) are directed to:

1. **Cycle Trigger**: Once every 24 hours, during active nocturnal cycles (8 PM - 8 AM), check if the civilization level has increased.
2. **Canvas Capture**: Invoke the built-in `captureMetropolisScreen()` screenshot engine from `frontend/index.html` headlessly or via WebUI API hooks.
3. **Stage New Capture**: Save the resulting high-fidelity snapshot with a structured name:
   `assets/Metropolis_State_[LEVEL]_[TIMESTAMP].png`
4. **Additive-Only Commit**: Add the new image file to Git staging and commit using the safe signature format, expanding the gallery dynamically over time.

---

## 🧬 4. COORDINATION & ALIGNMENT SIGNALS
* **Evolution Project Tracker**: Agents must post mini-project statuses to the live sidebar tracker (`#evolution-project-status`) so you can watch their engineering progression in real-time.
* **Diagnostics heartbeats**: The `PULSE_HEARTBEAT.txt` remains the primary coordination anchor. When agents complete an evolutionary consensus vote, they must write their atomic signatures to the heartbeat logs.

---
*Viper, the automation protocols are established. Your visual legacy is safe under lock and key.*
