package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.TitledPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Step 22.3 - Surgical Injection of Logit Distribution Chart
 */
public class LogitChartPlugin implements GUIExtension {

    private XYChart.Series<Number, Number> series;
    private LineChart<Number, Number> lineChart;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        final NumberAxis xAxis = new NumberAxis();
        final NumberAxis yAxis = new NumberAxis();
        xAxis.setLabel("Token Index");
        yAxis.setLabel("Logit Score");

        lineChart = new LineChart<>(xAxis, yAxis);
        lineChart.setTitle("Emergent Logit Distribution");
        lineChart.setCreateSymbols(false);
        lineChart.setPrefHeight(200);
        lineChart.setAnimated(false); // Speed optimization

        series = new XYChart.Series<>();
        series.setName("Raw Reasoning Strength");
        lineChart.getData().add(series);

        // Styling for retro look
        lineChart.setStyle("-fx-background: #000; -fx-text-fill: #00ffcc;");
        xAxis.lookup(".axis-label").setStyle("-fx-text-fill: #00ffcc;");
        yAxis.lookup(".axis-label").setStyle("-fx-text-fill: #00ffcc;");

        // Step 22.3: Collapsible Panel
        TitledPane titledPane = new TitledPane("LOGIT TELEMETRY", lineChart);
        titledPane.setExpanded(false); // Collapsed by default
        titledPane.setStyle("-fx-text-fill: #00ffcc; -fx-background-color: #111;");

        // Surgical append
        rightPanel.getChildren().add(titledPane);
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                if (json.has("type") && json.getString("type").equals("LOGIT_UPDATE")) {
                    JSONArray data = json.getJSONArray("data");
                    
                    Platform.runLater(() -> {
                        series.getData().clear();
                        for (int i = 0; i < data.length(); i++) {
                            series.getData().add(new XYChart.Data<>(i, data.getDouble(i)));
                        }
                    });
                }
            }
        } catch (Exception e) {
            // Silently ignore malformed logit packets to prevent GUI crash
        }
    }
}
