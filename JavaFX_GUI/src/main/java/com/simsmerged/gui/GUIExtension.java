package com.simsmerged.gui;

import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;

/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Step 21.2 - Plugin Registry Interface for Surgical UI Integration
 */
public interface GUIExtension {
    /**
     * Called when the plugin is registered. 
     * Allows the plugin to inject nodes into the rightPanel or canvas.
     */
    void initialize(VBox rightPanel, Pane canvasPane, App app);

    /**
     * Called when a WebSocket message is received.
     * Allows the plugin to react to backend events without modifying App.java.
     */
    void onMessage(String rawJson);
}
