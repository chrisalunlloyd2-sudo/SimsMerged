package com.simsneo.engine;

import com.simsneo.model.WorldGrid;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

/**
 * EventDispatcher: Implements a simple observer pattern to broadcast "SystemEvents" 
 * to the engine modules and handles random world events.
 * 
 * [TIMESTAMP] [SimsMerged-v1.3] [Gemini-CLI-Architect]
 */
public class EventDispatcher {

    public enum SystemEvent {
        NODE_FAILURE,
        AGENT_REBORN,
        PURGE_COMMAND,
        HEARTBEAT_PULSE,
        QUANTUM_SYNC,
        BURGLAR,
        FIRE,
        TRASH_ACCUMULATION
    }

    public interface EventListener {
        void onEvent(SystemEvent event, String metadata);
    }

    private static final List<EventListener> listeners = new ArrayList<>();
    private final Random rand = new Random();

    public void checkRandomEvents(WorldGrid world, int hour) {
        // Step 141-150: World Events (Birthdays, Burglar, Fire, Trash buildup)
        if (rand.nextDouble() < 0.05) {
            double roll = rand.nextDouble();
            if (roll < 0.3) {
                broadcast(SystemEvent.BURGLAR, "Security breach detected in sector " + rand.nextInt(100));
            } else if (roll < 0.6) {
                broadcast(SystemEvent.FIRE, "Thermal anomaly detected on grid coordinate " + rand.nextInt(128) + "," + rand.nextInt(128));
            } else {
                broadcast(SystemEvent.TRASH_ACCUMULATION, "Data debris requires cleanup.");
            }
        }
    }

    public static void subscribe(EventListener listener) {
        listeners.add(listener);
        log("Subscriber added: " + listener.getClass().getSimpleName());
    }

    public static void unsubscribe(EventListener listener) {
        listeners.remove(listener);
        log("Subscriber removed: " + listener.getClass().getSimpleName());
    }

    public static void broadcast(SystemEvent event, String metadata) {
        log("Broadcasting Event: " + event + " | Context: " + metadata);
        for (EventListener listener : listeners) {
            listener.onEvent(event, metadata);
        }
    }

    private static void log(String message) {
        String timestamp = ZonedDateTime.now().format(DateTimeFormatter.ISO_INSTANT);
        System.out.println("[" + timestamp + "] [SimsMerged-v1.3] [Gemini-CLI-Architect] " + message);
    }
}
