package com.simsneo.view;

import com.simsneo.engine.GameClock;
import com.simsneo.model.Sim;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.control.Label;
import javafx.scene.control.ProgressBar;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;

/**
 * Step 301-310: The HUD Overlay
 * Implements the "Control Dashboard" (The blue panel).
 */
public class HUD extends HBox {

    private Label timeLabel;
    private Label speedLabel;
    private VBox motiveContainer;
    private Label activeSimName;

    public HUD() {
        this.setPrefHeight(150);
        this.setPadding(new Insets(10));
        this.setSpacing(20);
        this.setAlignment(Pos.CENTER_LEFT);
        this.setStyle("-fx-background-color: #000000; -fx-border-color: #00ffff; -fx-border-width: 2 0 0 0;");
        
        initializeComponents();
    }

    private void initializeComponents() {
        // Family Portrait Placeholder (Step 307)
        VBox portraitBox = new VBox();
        portraitBox.setPrefSize(100, 130);
        portraitBox.setStyle("-fx-background-color: #c0c0c0; -fx-border-color: #000000;");
        activeSimName = new Label("Sim Name");
        activeSimName.setTextFill(Color.BLACK);
        portraitBox.getChildren().add(activeSimName);
        portraitBox.setAlignment(Pos.BOTTOM_CENTER);

        // Time and Speed Controls (Step 302)
        VBox infoBox = new VBox();
        infoBox.setSpacing(5);
        timeLabel = new Label("MON 08:00");
        timeLabel.setFont(Font.font("Consolas", 18));
        timeLabel.setTextFill(Color.WHITE);
        
        speedLabel = new Label("Speed: 1x");
        speedLabel.setTextFill(Color.LIGHTGRAY);
        
        infoBox.getChildren().addAll(timeLabel, speedLabel);

        // Motive Bars (Step 303: Accessibility Lock)
        motiveContainer = new VBox();
        motiveContainer.setSpacing(2);
        addMotiveBar("Hunger");
        addMotiveBar("Energy");
        addMotiveBar("Social");

        this.getChildren().addAll(portraitBox, infoBox, motiveContainer);
        addOmniHUD(); // Step 1204
    }

    private Label lblNodes;
    private Label lblAgents;

    private void addOmniHUD() {
        VBox gridInfo = new VBox(5);
        gridInfo.setPadding(new Insets(5));
        gridInfo.setStyle("-fx-background-color: #000040; -fx-border-color: #ffd700;");
        
        Label lblGrid = new Label("GLOBAL GRID: ONLINE");
        lblGrid.setTextFill(Color.GOLD);
        lblGrid.setFont(Font.font("Arial", 12));
        
        lblNodes = new Label("NODES: Syncing...");
        lblNodes.setTextFill(Color.WHITE);

        lblAgents = new Label("AGENTS: Syncing...");
        lblAgents.setTextFill(Color.WHITE);
        
        gridInfo.getChildren().addAll(lblGrid, lblNodes, lblAgents);
        this.getChildren().add(gridInfo);
    }

    private void addMotiveBar(String name) {
        HBox row = new HBox(5);
        row.setAlignment(Pos.CENTER_LEFT);
        Label lbl = new Label(name);
        lbl.setPrefWidth(60);
        lbl.setTextFill(Color.WHITE);
        ProgressBar pb = new ProgressBar(1.0);
        pb.setPrefWidth(150);
        // Step 303: High-contrast green for high, red for low (logic in update)
        row.getChildren().addAll(lbl, pb);
        motiveContainer.getChildren().add(row);
    }

    public void update(GameClock clock, Sim activeSim) {
        timeLabel.setText(clock.getTimeString());
        speedLabel.setText("Speed: " + clock.getSpeed() + "x");
        activeSimName.setText(activeSim.getName());
        
        // Update motive bars (Step 303)
        updateBar(0, activeSim.getMotive(Sim.Motive.HUNGER) / 100.0);
        updateBar(1, activeSim.getMotive(Sim.Motive.ENERGY) / 100.0);
    }

    public void updateGridStatus(int nodes, int agents) {
        lblNodes.setText("NODES: " + nodes + " ACTIVE");
        lblAgents.setText("AGENTS: " + agents + " DEPLOYED");
    }

    private void updateBar(int index, double progress) {
        HBox row = (HBox) motiveContainer.getChildren().get(index);
        ProgressBar pb = (ProgressBar) row.getChildren().get(1);
        pb.setProgress(progress);
        
        // Step 303: Dynamic Color (Simulated via style)
        if (progress < 0.2) pb.setStyle("-fx-accent: red;");
        else pb.setStyle("-fx-accent: #00ff00;");
    }
}
