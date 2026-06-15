# EXHAUSTIVE METROPOLITAN CATALOG: SIMSMERGED ARCHITECT EDITION (v1.4)

This document catalogs every functioning architectural component, behavioral protocol, and data-flow trajectory currently active in the SimsMerged Metropolis. v1.4 introduces Real-Machine Bio-Sync and the Treasury Point Economy.

---

## 🏛️ SECTION 1: ARCHITECTURAL TOPOLOGIES (THE 6 CITIES)

### City 1: Silicon Central (The Compute City)
*   **CPU_CORE:** The primary execution logic. Features live load % and core count telemetry.
*   **CACHE_L1 (Instruction):** Ultra-fast instruction buffer. Linked via red-laser local bus.
*   **CACHE_L2 (Shared):** Mid-level data cache.
*   **CACHE_L3 (Last Level):** Large-capacity silicon buffer.
*   **IMC (Memory Controller):** The gateway between compute and memory matrix.

### City 2: Memory Matrix (The RAM City)
*   **DIMM (Physical RAM):** High-speed volatile memory modules. Reflects real-machine GB capacity.
*   **PAGE_TABLE:** Virtual-to-Physical memory mappers. Includes live Swap/Pagefile utilization stats.

### City 3: The Graphics Grid (The GPU City)
*   **GPU_CU (Compute Unit):** Parallel matrix-math clusters.
*   **VRAM (Frame Buffer):** Graphical data buffer. Linked via high-velocity PCIE arcs.
*   **RT_CORE:** Dedicated hardware for simulated ray-tracing trajectories.

### City 4: Storage Hive (The Disk City)
*   **NVME (SSD):** High-speed non-volatile storage. Reflects real-machine Disk_C utilization.
*   **MFT (Journaling):** Master File Table nodes managing data integrity and system logs.

### City 5: Kernel Hub (The OS City)
*   **HAL (Hardware Abstraction):** The logical bridge between software and silicon.
*   **REG_HIVE (Registry):** The central configuration database for all metropolitan nodes.
*   **DRIVER_STORE:** The binary repository for hardware-software communication.
*   **SYS32:** Core OS binaries, essential for grid stability.

### City 6: Protocol Port (The Network City)
*   **MODEM_HW:** The physical networking gateway.
*   **DNS_RESOLVER:** Logic node for resolving global data addresses.
*   **PROXY_WALL:** An administrative traffic filter and security gateway.

---

## 🧠 SECTION 2: AI AGENTIC NETWORK (THE INHABITANTS)

### High-Priority Special Agents
*   **ADMIN_ROOT:** The system authority. Autonomously identifies and **deletes** low-level background processes to reclaim resources.
*   **SI_AGENT (Suicide Inhibitor):** Detects **Depressed Kernels** (stability < 20%) and physically **Binds** to them with a magenta visual chain to prevent systemic failure.

### Specialized AI Kernels
*   **NURSE / DOCTOR:** Specialized healers. They seek out depressed kernels (secured by the SI) and restore their stability metrics.
*   **BOUNCER:** The security force. They actively hunt and evict **Rogue Processes (Bugs)** from the grid.
*   **RAM WATCHER:** Stationary sentinels resident on DIMM nodes, monitoring memory pressure.
*   **PACKET COURIER:** Navigates the global network stack to ensure protocol delivery.

---

## 🔗 SECTION 3: NEURAL BUS & TRANSPORTATION (DATA FLOW)

### Visual Data Trajectories
*   **LOCAL BUS (Straight/Fast):** High-speed data movement within the Compute City (Cores to Caches).
*   **SYSTEM BUS (Solid Neon):** High-bandwidth pipelines connecting IMC to Memory DIMMs.
*   **PCIE ARCS (Parabolic High-Velocity):** Long-range data "leaps" connecting CPU to GPU and SSD.
*   **NETWORK PROTOCOLS (Dashed Arcs):** Parabolic trajectories exiting the Modem (TCP/IP=Reliable, UDP=Wobble/Jitter).

### Urban Metaphor Mapping
*   **TCP/IP:** Data moves as "Walking" packets (reliable, systematic).
*   **UDP:** Data moves as "Bike" packets (fast, high-frequency, jittery).
*   **HTTP/WEB:** Data moves as "Car" packets (standard metropolitan transit).

---

## 🛡️ SECTION 4: SECURITY & SAFETY HARD-LOCKS

*   **BIOS IMMUTABLE:** All BIOS/UEFI settings are hard-coded and locked at the silicon level. No GUI or agent command can modify these values.
*   **INFRASTRUCTURE LOCK:** Physical hardware (CPU, RAM, GPU, Modem) is anchored to the grid and cannot be moved or deleted.
*   **ISOLATION LAYER:** All detailed agentic and network topologies are stored in `local_env/` and permanently blocked from GitHub visibility.

---

## 🕹️ SECTION 5: INTERACTION SUITE

*   **POINTER MODE:** Standard navigation and component deployment.
*   **EDIT_FINGER MODE:** High-fidelity selection state allowing real-time injection of parameters into existing nodes.
*   **INFORMATION VEIL:** Exhaustive hover-tooltip providing technical descriptions and nominal telemetry for every node.
*   **CYBER-CONSOLE:** Real-time scrolling system log for audit trails and event monitoring.

---

## 💰 SECTION 6: THE BEHAVIORAL ECONOMY (NEW v1.4)

*   **TREASURY_POINTS (TP):** The global currency of the Metropolis. Earned via agent labor and neural processing.
*   **CYBER_BANK:** The central ledger (`blockchain_ledger.json`) tracking all TP transactions.
*   **DEPIN_DIVIDEND:** Autonomous distribution of points to agents based on grid uptime.
*   **RESOURCE_FENCE:** Economic limits on CPU/RAM usage; agents must pay TP to unlock higher-fidelity kernels.

---

## 🛡️ SECTION 7: SECURITY & SAFETY HARD-LOCKS (EXPANDED)

*   **BIOS IMMUTABLE:** All BIOS/UEFI settings are hard-coded and locked at the silicon level.
*   **PII_SCRUBBER:** Active scanner in `SystemIntegrity.java` preventing local path leaks.
*   **NOCTURNAL_LOCK:** Hard-coded active hours (8 PM - 8 AM) for SSD-intensive processing.

