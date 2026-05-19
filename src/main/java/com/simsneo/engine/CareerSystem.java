package com.simsneo.engine;

import com.simsneo.model.Sim;
import java.util.HashMap;
import java.util.Map;

/**
 * Step 261-270: The Career System
 */
public class CareerSystem {
    
    public enum JobLevel {
        UNEMPLOYED(0),
        JUNIOR_CODER(50),
        SYSTEMS_ARCHITECT(500),
        ORCHESTRATOR(2000);

        public final int dailyPay;
        JobLevel(int pay) { this.dailyPay = pay; }
    }

    private Map<String, JobLevel> simJobs = new HashMap<>();

    public void assignJob(Sim sim, JobLevel level) {
        simJobs.put(sim.getName(), level);
    }

    public void checkCarpool(Sim sim, int hour) {
        JobLevel job = simJobs.getOrDefault(sim.getName(), JobLevel.UNEMPLOYED);
        if (job == JobLevel.UNEMPLOYED) return;

        // Carpool arrives at 9 AM
        if (hour == 9) {
            System.out.println("[CAREER] Carpool arrived for " + sim.getName());
            // Step 265: Carpool Drift Fix - Immediate trigger
        }
    }

    public int calculatePaycheck(Sim sim) {
        return simJobs.getOrDefault(sim.getName(), JobLevel.UNEMPLOYED).dailyPay;
    }
}
