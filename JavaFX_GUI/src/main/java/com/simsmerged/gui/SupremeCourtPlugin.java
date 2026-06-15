package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import org.json.JSONObject;

/**
 * [TIMESTAMP: 2026-06-14T19:40:00.000Z]
 * [PROJECT_ID: SimsMerged-v1.4.2]
 * [AGENT_ID: viper_cli-architectssj4]
 * DESCRIPTION: Layered Governance - Supreme Court Plugin.
 * Visualizes legal disputes, judge verdicts, and policy shifts.
 */
public class SupremeCourtPlugin implements GUIExtension {

    private ListView<String> caseList;
    private Label statusLabel;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        VBox container = new VBox(5);
        container.setPadding(new Insets(10, 0, 10, 0));
        container.setStyle("-fx-border-color: #ff3366; -fx-border-width: 1 0 0 0;");

        Label header = new Label("METROPOLIS SUPREME COURT");
        header.setTextFill(Color.web("#ff3366"));
        header.setStyle("-fx-font-weight: bold; -fx-font-size: 10px;");

        statusLabel = new Label("LGA STATUS: ACTIVE");
        statusLabel.setTextFill(Color.WHITE);
        statusLabel.setStyle("-fx-font-size: 9px;");

        caseList = new ListView<>();
        caseList.setPrefHeight(100);
        caseList.setStyle("-fx-control-inner-background: #000; -fx-text-fill: #ff3366; -fx-font-family: 'Courier New'; -fx-font-size: 9px;");

        container.getChildren().addAll(header, statusLabel, caseList);
        rightPanel.getChildren().add(container);
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                if (json.has("type") && json.getString("type").equals("GOVERNANCE_CASE")) {
                    String defendant = json.getString("defendant");
                    String verdict = json.getString("verdict");
                    String judge = json.getString("judge");

                    Platform.runLater(() -> {
                        String entry = "[" + judge + "] " + defendant + " -> " + verdict;
                        caseList.getItems().add(0, entry);
                        if (caseList.getItems().size() > 20) caseList.getItems().remove(20);
                        
                        if (verdict.equals("REJECTED")) {
                            statusLabel.setText("LGA STATUS: VIOLATION DETECTED");
                            statusLabel.setTextFill(Color.web("#ff3366"));
                        } else {
                            statusLabel.setText("LGA STATUS: COMPLIANT");
                            statusLabel.setTextFill(Color.web("#00ffcc"));
                        }
                    });
                }
            }
        } catch (Exception e) {
            // Ignore non-governance messages
        }
    }
}
