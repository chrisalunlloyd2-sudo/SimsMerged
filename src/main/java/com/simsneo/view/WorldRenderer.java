package com.simsneo.view;

import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

public class WorldRenderer extends Canvas {
    public WorldRenderer() {
        super(1024, 768);
    }
    
    public void render() {
        GraphicsContext gc = getGraphicsContext2D();
        gc.setFill(Color.DARKSLATEGRAY);
        gc.fillRect(0, 0, getWidth(), getHeight());
        
        // Isometric Grid Render Simulation
        gc.setStroke(Color.LIGHTGREEN);
        gc.setLineWidth(1.0);
        for(int i = 0; i < 20; i++) {
            gc.strokeLine(0, i * 32, getWidth(), i * 32 + 200);
        }
        
        gc.setFill(Color.CYAN);
        gc.fillText("Darwinistic Engine Active - Systems Online", 20, 30);
    }
}