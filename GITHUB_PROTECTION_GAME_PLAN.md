# GITHUB PROTECTION & ASSET INTEGRITY PLAN
**TIMESTAMP:** 2026-06-01T02:18:00.000Z
**PROJECT_ID:** SimsMerged-v1.3
**AGENT_ID:** Antigravity-CLI-Architect

---

## 🛡️ THE GOLDEN RULE OF SAFE SHIPPING
To prevent any future data loss, history wipes, or picture deletions on GitHub, all agents working in the VIPER ecosystem MUST strictly adhere to this protection plan.

### 1. Absolute Ban on Force Pushing (`--force`)
* **MANDATE:** Under no circumstances shall any agent execute `git push --force`, `git push -f`, or `git push -u origin main --force`.
* **RATIONALE:** Force-pushing completely replaces the remote GitHub repository history with the local history. If the remote repository has wiki pictures, committed screenshots, custom release assets, or readme images that do not exist in the local directory, they will be **permanently deleted**.
* **SAFE WORKFLOW:**
  1. Always run `git fetch origin` before pushing.
  2. If there are upstream changes, perform `git pull --rebase` or `git merge` to integrate them safely.
  3. Resolve any conflicts locally and verify syntax before committing.
  4. Perform a standard `git push origin master` or `git push origin main`.

### 2. Assets Folder Locking & Anti-Deletion
* **MANDATE:** The `assets/` directories (specifically `C:\Users\viper\Desktop\SimsMerged\assets\`) contain the hard-worked visual screenshots and mockups of the simulated cities (e.g., `ACTUAL_METROPOLIS_CITY.png`, `Final_Boss_Environment_Screenshot.png`, etc.).
* **RULE:** No automated script, evolution loop, or cleanup script is allowed to delete, rename, or overwrite any files in the `assets/` directory or any files with graphic extensions (`.png`, `.jpg`, `.jpeg`, `.gif`, `.svg`, `.ico`) without explicit, interactive written user consent.

### 3. Dry-Run Verification Check
* **MANDATE:** Before pushing changes to a remote repository, agents should run `git push --dry-run` to identify if the branch is out of sync or if git expects an overwrite. If dry-run fails, stop and notify the user immediately.

### 4. Git Reflog and Local Backup
* **MANDATE:** Local git reflog is the safety net. If a bad push or reset occurs, the agent must inspect `git reflog` to recover the previous HEAD commit hash and restore it.

---
*Viper, your hard-worked pictures and repo integrity are locked and guarded. The Ledger remembers.*
