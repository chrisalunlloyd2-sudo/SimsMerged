package com.simsmerged.gui;

import javafx.application.Platform;
import javafx.scene.control.Label;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import org.json.JSONArray;
import org.json.JSONObject;

/**
 * TIMESTAMP: 2026-06-09
 * PROJECT_ID: SimsMerged-v1.4.2
 * DESCRIPTION: Step 25.3 - Surgical Injection of Weather NOTAM Overlay
 */
public class WeatherPlugin implements GUIExtension {

    private Label weatherLabel;
    private VBox weatherBox;

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        weatherBox = new VBox(2);
        weatherBox.setPadding(new javafx.geometry.Insets(5));
        weatherBox.setStyle("-fx-background-color: rgba(0,0,0,0.6); -fx-border-color: #ff3366; -fx-border-width: 1;");
        
        Label header = new Label("ATC WEATHER NOTAMS");
        header.setTextFill(Color.web("#ff3366"));
        header.setStyle("-fx-font-size: 10px; -fx-font-weight: bold;");
        
        weatherLabel = new Label("SKY CLEAR");
        weatherLabel.setTextFill(Color.web("#33ff66"));
        weatherLabel.setStyle("-fx-font-size: 9px;");

        weatherBox.getChildren().addAll(header, weatherLabel);
        
        // Inject into the top left of the canvas area
        weatherBox.setLayoutX(10);
        weatherBox.setLayoutY(10);
        canvasPane.getChildren().add(weatherBox);
    }

    @Override
    public void onMessage(String rawJson) {
        try {
            if (rawJson.startsWith("{")) {
                JSONObject json = new JSONObject(rawJson);
                if (json.has("type") && json.getString("type").equals("WEATHER_UPDATE")) {
                    JSONArray notams = json.getJSONArray("notams");
                    
                    Platform.runLater(() -> {
                        if (notams.length() == 0) {
                            weatherLabel.setText("SKY CLEAR");
                            weatherLabel.setTextFill(Color.web("#33ff66"));
                            weatherBox.setStyle("-fx-background-color: rgba(0,0,0,0.6); -fx-border-color: #33ff66;");
                        } else {
                            StringBuilder sb = new StringBuilder();
                            for (int i = 0; i < notams.length(); i++) {
                                JSONObject n = notams.getJSONObject(i);
                                sb.append("! ").append(n.getString("code")).append("\n");
                            }
                            weatherLabel.setText(sb.toString().trim());
                            weatherLabel.setTextFill(Color.web("#ff3366"));
                            weatherBox.setStyle("-fx-background-color: rgba(0,0,0,0.8); -fx-border-color: #ff3366;");
                        }
                    });
                }
            }
        } catch (Exception e) {
            // Silently ignore
        }
    }
}
