package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.control.TitledPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import org.json.JSONObject;

/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Step 24.2 - Surgical Injection of Consensus Progress Tracker
 */
public class ConsensusPlugin implements GUIExtension {

    private VBox progressBox;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        progressBox = new VBox(5);
        progressBox.setPadding(new javafx.geometry.Insets(5));
        progressBox.setStyle("-fx-background-color: #000;");

        TitledPane titledPane = new TitledPane("SWARM CONSENSUS", progressBox);
        titledPane.setExpanded(true);
        titledPane.setStyle("-fx-text-fill: #ffff33; -fx-background-color: #111;");

        rightPanel.getChildren().add(titledPane);
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                if (json.has("type") && json.getString("type").equals("CONSENSUS_UPDATE")) {
                    String pid = json.getString("proposal_id");
                    String stage = json.getString("stage");
                    int count = json.getInt("vote_count");
                    int quorum = json.getInt("quorum");

                    Platform.runLater(() -> {
                        updateProgressUI(pid, stage, count, quorum);
                    });
                }
            }
        } catch (Exception e) {}
    }

    private void updateProgressUI(String pid, String stage, int count, int quorum) {
        // Find existing progress bar for this proposal or create new
        Label lbl = new Label(pid + " [" + stage + "]");
        lbl.setTextFill(Color.web("#ffff33"));
        lbl.setStyle("-fx-font-size: 9px;");

        ProgressBar pb = new ProgressBar((double)count / quorum);
        pb.setMaxWidth(Double.MAX_VALUE);
        pb.setStyle("-fx-accent: #ffff33;");

        // Simple clear and redraw for the simulation
        progressBox.getChildren().clear();
        progressBox.getChildren().addAll(lbl, pb);
    }
}
