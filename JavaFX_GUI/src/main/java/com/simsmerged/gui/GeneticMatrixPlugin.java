package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import org.json.JSONArray;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

/**
 * [TIMESTAMP: 2026-06-14T20:40:00.000Z]
 * [PROJECT_ID: SimsMerged-v1.4.2]
 * [AGENT_ID: viper_cli-architectssj4]
 * DESCRIPTION: Step 63 - Genetic Matrix View.
 * Visualizes agent technical traits and skills.
 */
public class GeneticMatrixPlugin implements GUIExtension {

    private GridPane matrixGrid;
    private VBox container;
    private Map<String, VBox> agentSkillContainers = new HashMap<>();

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        container = new VBox(5);
        container.setPadding(new Insets(10, 0, 10, 0));
        container.setStyle("-fx-border-color: #9933ff; -fx-border-width: 1 0 0 0;");

        Label header = new Label("GENETIC SKILL-MATRIX");
        header.setTextFill(Color.web("#9933ff"));
        header.setStyle("-fx-font-weight: bold; -fx-font-size: 10px;");

        matrixGrid = new GridPane();
        matrixGrid.setHgap(5);
        matrixGrid.setVgap(5);
        
        ScrollPane scroll = new ScrollPane(matrixGrid);
        scroll.setPrefHeight(120);
        scroll.setStyle("-fx-background: #000; -fx-border-color: transparent;");
        scroll.setFitToWidth(true);

        container.getChildren().addAll(header, scroll);
        rightPanel.getChildren().add(container);
        
        // Initial build from app.getAgentMap() if possible
        Platform.runLater(this::refreshMatrix);
    }

    private void refreshMatrix() {
        matrixGrid.getChildren().clear();
        agentSkillContainers.clear();
        
        // This is a simplified view: List of agents and their active traits
        int row = 0;
        // matrixGrid is a simple list for now as we don't have many agents
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                if (json.has("type") && json.getString("type").equals("COUNCIL_2_0_EVENT")) {
                    String event = json.getString("event");
                    JSONObject data = json.getJSONObject("data");

                    if (event.equals("GENETIC_HANDSHAKE") || event.equals("INVENTION_REVIEW") || event.equals("TRAIT_UNLOCKED")) {
                        // For simplicity, we refresh when these happen, but normally we'd need the full agent state
                        // The backend 'AGENT_UPDATE' should ideally include traits now
                    }
                } else if (json.has("type") && json.getString("type").equals("AGENT_UPDATE")) {
                    if (json.has("traits")) {
                        updateAgentTraits(json.getString("agent_id"), json.getJSONArray("traits"));
                    }
                }
            }
        } catch (Exception e) {
            // Ignore
        }
    }

    private void updateAgentTraits(String agentId, JSONArray traits) {
        Platform.runLater(() -> {
            VBox box = agentSkillContainers.get(agentId);
            if (box == null) {
                box = new VBox(2);
                box.setPadding(new Insets(2));
                box.setStyle("-fx-background-color: #111; -fx-border-color: #333;");
                
                Label name = new Label(agentId.toUpperCase());
                name.setTextFill(Color.WHITE);
                name.setStyle("-fx-font-size: 8px; -fx-font-weight: bold;");
                box.getChildren().add(name);
                
                agentSkillContainers.put(agentId, box);
                int count = matrixGrid.getChildren().size();
                matrixGrid.add(box, count % 3, count / 3);
            }
            
            // Clear old traits (except name)
            box.getChildren().remove(1, box.getChildren().size());
            
            for (int i = 0; i < traits.length(); i++) {
                Label tLabel = new Label("• " + traits.getString(i));
                tLabel.setTextFill(Color.web("#9933ff"));
                tLabel.setStyle("-fx-font-size: 7px;");
                box.getChildren().add(tLabel);
            }
        });
    }
}
