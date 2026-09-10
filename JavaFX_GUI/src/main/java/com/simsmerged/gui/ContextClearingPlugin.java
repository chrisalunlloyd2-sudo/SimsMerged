package com.simsmerged.gui;

import javafx.scene.control.Button;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.application.Platform;

/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Step 22.2 - Surgical Injection of Context Clearing Button
 */
public class ContextClearingPlugin implements GUIExtension {

    private App mainApp;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        this.mainApp = app;
        
        // Create the button with consistent styling
        Button btnClear = new Button("CLEAR CONTEXT");
        btnClear.setStyle("-fx-background-color: #444400; -fx-text-fill: #ffff33; -fx-border-color: #ffff33;");
        btnClear.setMaxWidth(Double.MAX_VALUE);
        
        btnClear.setOnAction(e -> {
            if (app.getWebSocket() != null) {
                app.getWebSocket().sendText("/clear_context", true);
                app.getChatList().getItems().add("[God Hand] Context clearing command sent.");
            }
        });

        // Surgical append-only injection
        rightPanel.getChildren().add(btnClear);
    }

    @Override
    public void onMessage(String rawJson) {
        // This plugin is command-only, doesn't need to process incoming logs
    }
}
