package com.simsneo.engine;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

/**
 * EventDispatcher: Implements a simple observer pattern to broadcast "SystemEvents" 
 * to the engine modules.
 * 
 * [TIMESTAMP] [SimsMerged-v1.3] [Gemini-CLI-Architect]
 */
public class EventDispatcher {

    public enum SystemEvent {
        NODE_FAILURE,
        AGENT_REBORN,
        PURGE_COMMAND,
        HEARTBEAT_PULSE,
        QUANTUM_SYNC
    }

    public interface EventListener {
        void onEvent(SystemEvent event, String metadata);
    }

    private static final List<EventListener> listeners = new ArrayList<>();

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
