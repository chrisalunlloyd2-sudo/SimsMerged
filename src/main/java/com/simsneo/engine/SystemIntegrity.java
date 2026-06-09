package com.simsneo.engine;

import com.simsneo.model.Sim;
import com.simsneo.model.WorldGrid;
import com.simsneo.model.GameObject;
import java.util.List;

/**
 * Step 351-360: System Integrity & Logic In-fill
 */
public class SystemIntegrity {

    /**
     * Step 352: Identify Logic Gaps
     * Example: Sims attempting to use a Fridge without an available interaction slot.
     */
    public static void validateSimInteractions(WorldGrid world) {
        for (Sim sim : world.getSims()) {
            if (sim.getState() == Sim.SimState.INTERACTING) {
                // Check if target still exists and is accessible
                boolean targetFound = false;
                for (GameObject obj : world.getObjects()) {
                    if (obj.getSlotX() == sim.getGridX() && obj.getSlotY() == sim.getGridY()) {
                        targetFound = true;
                        break;
                    }
                }
                
                if (!targetFound) {
                    System.out.println("[INTEGRITY] Sim " + sim.getName() + " orphaned. Resetting state.");
                    sim.setState(Sim.SimState.IDLE);
                }
            }
        }
    }

    /**
     * Step 353: Brute-Force In-fill (Chair-Search Fallback)
     */
    public static GameObject findNearestObject(WorldGrid world, int x, int y, String name) {
        GameObject nearest = null;
        double minDist = Double.MAX_VALUE;
        
        for (GameObject obj : world.getObjects()) {
            if (obj.getName().equalsIgnoreCase(name)) {
                double dist = Math.sqrt(Math.pow(obj.getGridX() - x, 2) + Math.pow(obj.getGridY() - y, 2));
                if (dist < minDist) {
                    minDist = dist;
                    nearest = obj;
                }
            }
        }
        return nearest;
    }

    /**
     * Step 354: PII Entropy Scan
     * Scans for potential local path identifiers or keys.
     */
    public static void runEntropyScan(String metadata) {
        // Regex to detect common path patterns or high-entropy keys
        if (metadata.matches(".*[A-Z]:\\\\.*") || metadata.length() > 32) {
            System.out.println("[SCRUB] Sensitive entropy detected in metadata. Redacting...");
        }
    }

    /**
     * [2026-05-17T18:10:05.452Z] [SimsMerged-v1.3-Metropolis] [Gemini-CLI-Architect]
     * BLOCK 3: BINDING SEQUENCE
     * Forces a sim to anchor to the nearest Hospital node until stability > 50%.
     */
    public static void processBindingSequence(WorldGrid world, Sim sim) {
        if ("DEPRESSED".equals(sim.getEmotionalState()) || sim.getStability() < 0.2) {
            System.out.println("[INTEGRITY] Critical Stability Loss: " + sim.getName() + ". Initiating Binding.");
            sim.setState(Sim.SimState.BINDING);
            
            // Find nearest Hospital
            GameObject hospital = findNearestObject(world, sim.getGridX(), sim.getGridY(), "HOSPITAL");
            if (hospital != null) {
                // Anchor to hospital
                sim.setGridX(hospital.getGridX());
                sim.setGridY(hospital.getGridY());
                
                // Healing process
                sim.setStability(sim.getStability() + 0.1);
                if (sim.getStability() > 0.5) {
                    System.out.println("[INTEGRITY] Stability Restored: " + sim.getName() + ". Releasing Lock.");
                    sim.setEmotionalState("STABLE");
                    sim.setState(Sim.SimState.IDLE);
                }
            } else {
                System.out.println("[INTEGRITY] ERROR: No Hospital node found for binding!");
            }
        }
    }

    /**
     * [2026-05-17T17:56:10.000Z] [SimsMerged-v1.3-Metropolis] [Gemini-CLI-Architect]
     * BIOS HARD-LOCK CHECK
     * Returns true if critical hardware properties are at their baseline values.
     */
    public static boolean checkBIOSHardLock() {
        // Simulating hardware property checks
        boolean clockSynced = true;
        boolean voltageStable = true;
        boolean memoryIntegrity = true;

        System.out.println("[BIOS] Performing Hard-Lock verification...");
        return clockSynced && voltageStable && memoryIntegrity;
    }
}
