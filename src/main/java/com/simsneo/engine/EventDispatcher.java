package com.simsneo.engine;

import com.simsneo.model.WorldGrid;
import java.util.Random;

/**
 * Step 271-280: World Events Dispatcher
 */
public class EventDispatcher {
    private Random rand = new Random();

    public void checkRandomEvents(WorldGrid world, int hour) {
        // 5% chance of event every hour
        if (rand.nextDouble() < 0.05) {
            triggerEvent("BURGLAR", "A suspicious figure was seen near the grid.");
        }
    }

    private void triggerEvent(String type, String message) {
        System.out.println("[EVENT][" + type + "] " + message);
    }
}
