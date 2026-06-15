package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import org.json.JSONObject;

/**
 * [TIMESTAMP: 2026-06-14T18:40:00.000Z]
 * [PROJECT_ID: SimsMerged-v1.4.2]
 * [AGENT_ID: viper_cli-architectssj4]
 * DESCRIPTION: Hyper-Expansion Mandate - Telemetry Dashboard.
 * Bridges real-machine hardware telemetry (CPU/IO) to the JavaFX HUD.
 */
public class TelemetryDashboardPlugin implements GUIExtension {

    private ProgressBar cpuBar;
    private ProgressBar ioBar;
    private Label cpuLabel;
    private Label ioLabel;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        VBox container = new VBox(5);
        container.setPadding(new Insets(10, 0, 10, 0));
        container.setStyle("-fx-border-color: #00ffcc; -fx-border-width: 1 0 0 0;");

        Label header = new Label("HARDWARE TELEMETRY");
        header.setTextFill(Color.web("#00ffcc"));
        header.setStyle("-fx-font-weight: bold; -fx-font-size: 10px;");

        cpuLabel = new Label("CPU LOAD: 0%");
        cpuLabel.setTextFill(Color.WHITE);
        cpuLabel.setStyle("-fx-font-size: 9px;");
        cpuBar = new ProgressBar(0);
        cpuBar.setPrefWidth(280);
        cpuBar.setStyle("-fx-accent: #00ffcc;");

        ioLabel = new Label("SSD I/O PRESSURE: 0%");
        ioLabel.setTextFill(Color.WHITE);
        ioLabel.setStyle("-fx-font-size: 9px;");
        ioBar = new ProgressBar(0);
        ioBar.setPrefWidth(280);
        ioBar.setStyle("-fx-accent: #ff3366;");

        container.getChildren().addAll(header, cpuLabel, cpuBar, ioLabel, ioBar);
        rightPanel.getChildren().add(container);
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                if (json.has("type") && json.getString("type").equals("TELEMETRY_UPDATE")) {
                    double cpu = json.getDouble("cpu");
                    double io = json.getDouble("io");

                    Platform.runLater(() -> {
                        cpuBar.setProgress(cpu / 100.0);
                        cpuLabel.setText("CPU LOAD: " + String.format("%.1f", cpu) + "%");
                        
                        ioBar.setProgress(io / 100.0);
                        ioLabel.setText("SSD I/O PRESSURE: " + String.format("%.1f", io) + "%");

                        if (cpu > 80) cpuBar.setStyle("-fx-accent: #ff3366;");
                        else cpuBar.setStyle("-fx-accent: #00ffcc;");
                    });
                }
            }
        } catch (Exception e) {
            // Ignore non-telemetry messages
        }
    }
}
