package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.NumberAxis;
import javafx.scene.chart.XYChart;
import javafx.scene.control.TitledPane;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import org.json.JSONObject;

/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Step 8.3 - Surgical Injection of Metropolis Economy Dashboard
 */
public class EconomyDashboardPlugin implements GUIExtension {

    private XYChart.Series<Number, Number> woodSeries;
    private XYChart.Series<Number, Number> stoneSeries;
    private int tick = 0;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        final NumberAxis xAxis = new NumberAxis();
        final NumberAxis yAxis = new NumberAxis();
        xAxis.setLabel("Epoch Ticks");
        yAxis.setLabel("Resource Count");

        LineChart<Number, Number> economyChart = new LineChart<>(xAxis, yAxis);
        economyChart.setTitle("METROPOLIS ECONOMY");
        economyChart.setCreateSymbols(true);
        economyChart.setPrefHeight(200);

        woodSeries = new XYChart.Series<>();
        woodSeries.setName("Wood");
        stoneSeries = new XYChart.Series<>();
        stoneSeries.setName("Stone");

        economyChart.getData().add(woodSeries);
        economyChart.getData().add(stoneSeries);

        TitledPane titledPane = new TitledPane("ECONOMY DASHBOARD", economyChart);
        titledPane.setExpanded(false);
        titledPane.setStyle("-fx-text-fill: #00ffcc; -fx-background-color: #111;");

        rightPanel.getChildren().add(titledPane);
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                // Listen for aggregate reports from the Aggregator Agent
                if (json.has("type") && json.getString("type").equals("ECONOMY_SUMMARY")) {
                    int wood = json.getInt("total_wood");
                    int stone = json.getInt("total_stone");
                    
                    Platform.runLater(() -> {
                        tick++;
                        woodSeries.getData().add(new XYChart.Data<>(tick, wood));
                        stoneSeries.getData().add(new XYChart.Data<>(tick, stone));
                        if (woodSeries.getData().size() > 20) {
                            woodSeries.getData().remove(0);
                            stoneSeries.getData().remove(0);
                        }
                    });
                }
            }
        } catch (Exception e) {}
    }
}
