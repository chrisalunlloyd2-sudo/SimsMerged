package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import org.json.JSONObject;
import org.json.JSONArray;

/**
 * [TIMESTAMP: 2026-06-12T07:20:00.000Z]
 * [PROJECT_ID: SimsMerged-v1.4.2]
 * [AGENT_ID: viper_cli-architectssj4]
 * DESCRIPTION: Phase 16 - Step 46: Issue Tracker Board (GUI Panel)
 * Integrates GitHub-style issues into the game loop.
 */
public class IssueTrackerPlugin implements GUIExtension {

    private ListView<String> issueList;
    private VBox container;
    private App app;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        this.app = app;
        
        container = new VBox(5);
        container.setPadding(new Insets(5));
        container.setStyle("-fx-border-color: #00ffcc; -fx-border-width: 1 0 0 0; -fx-padding: 10 0 0 0;");

        Label title = new Label("ISSUE TRACKER BOARD");
        title.setTextFill(Color.web("#00ffcc"));
        title.setStyle("-fx-font-size: 11px; -fx-font-weight: bold; -fx-font-family: 'Courier New';");

        issueList = new ListView<>();
        issueList.setPrefHeight(120);
        issueList.setStyle("-fx-control-inner-background: #000; -fx-text-fill: #ffcc00; -fx-font-family: 'Courier New'; -fx-font-size: 10px;");
        
        // Context menu to assign issues
        ContextMenu contextMenu = new ContextMenu();
        MenuItem assignItem = new MenuItem("Assign to Nearest Agent");
        assignItem.setOnAction(e -> {
            String selected = issueList.getSelectionModel().getSelectedItem();
            if (selected != null && app.getWebSocket() != null) {
                app.getWebSocket().sendText("/assign_issue " + selected, true);
                app.getChatList().getItems().add("[God Hand] Assigning: " + selected);
            }
        });
        contextMenu.getItems().add(assignItem);
        issueList.setContextMenu(contextMenu);

        Button btnFetch = new Button("SYNC GITHUB ISSUES");
        btnFetch.setStyle("-fx-background-color: #1a3a4a; -fx-text-fill: #00ffcc; -fx-font-size: 10px;");
        btnFetch.setMaxWidth(Double.MAX_VALUE);
        btnFetch.setOnAction(e -> {
            if (app.getWebSocket() != null) {
                app.getWebSocket().sendText("/sync_issues", true);
                app.getChatList().getItems().add("[System] Requesting issue sync from GitHub...");
            }
        });

        container.getChildren().addAll(title, issueList, btnFetch);
        rightPanel.getChildren().add(container);

        // Initial Data
        issueList.getItems().addAll("#402: Fix Memory Leak", "#403: Implement Pathfinding", "#404: Texture Recovery");
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                if (json.has("type") && json.getString("type").equals("ISSUE_SYNC")) {
                    Platform.runLater(() -> {
                        issueList.getItems().clear();
                        JSONArray issues = json.getJSONArray("issues");
                        for (int i = 0; i < issues.length(); i++) {
                            issueList.getItems().add(issues.getString(i));
                        }
                    });
                } else if (json.has("type") && json.getString("type").equals("ISSUE_CLAIMED")) {
                    String issueId = json.getString("issue_id");
                    String agentId = json.getString("agent_id");
                    Platform.runLater(() -> {
                        app.getChatList().getItems().add("[Data Syphon] Agent " + agentId + " claimed " + issueId);
                        issueList.getItems().removeIf(s -> s.contains(issueId));
                    });
                }
            }
        } catch (Exception e) {
            // Not a JSON or wrong format
        }
    }
}
