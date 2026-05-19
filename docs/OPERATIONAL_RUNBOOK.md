# OPERATIONAL RUNBOOK: SIMSMERGED METROPOLIS

## 🎮 Interface Controls
- **Navigation:**
    - **Click + Drag:** Pan the metropolis camera.
    - **Mouse Wheel:** Zoom in/out of the 40x40 grid.
    - **Hover:** Activate the **Information Veil** for detailed node telemetry.
- **Interaction:**
    - **Right-Click:** Open the component-specific Suite logic menu.
    - **Pointer Mode:** Standard selection and deployment.
    - **Edit Finger:** Inject real-time parameters into active nodes.

## 🛠️ Administrative Operations
- **System Purge:**
    - Access the Cyber-Console and issue the `PURGE --LOW_LEVEL` command to clear stagnant background processes.
- **Agent Deployment:**
    - Use the Sidebar Build Menu to deploy additional Bouncers or Nurses to specific districts.
- **Telemetry Sync:**
    - The `bridge.js` protocol automatically syncs real-machine telemetry (CPU Load, RAM usage) into the simulation.

## 🚨 Troubleshooting
- **Depressed Kernels:** If stability drops across the grid, verify the SI_AGENT is active. If not, manually deploy a "Suicide Inhibitor" from the Admin Suite.
- **Packet Loss:** Check the Protocol Port (Network City) for Rogue Processes. Deploy Bouncers if necessary.
- **Backend Disconnect:** Ensure `uvicorn` is running on `127.0.0.1:8000`. If unavailable, the system will fallback to `local_env` static data.

---
*Operational Runbook v1.3*
