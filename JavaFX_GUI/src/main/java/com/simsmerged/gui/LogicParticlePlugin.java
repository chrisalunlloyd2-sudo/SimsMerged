package com.simsmerged.gui;

import javafx.animation.AnimationTimer;
import javafx.application.Platform;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.Pane;
import javafx.scene.layout.VBox;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Random;

/**
 * [TIMESTAMP: 2026-06-14T20:20:00.000Z]
 * [PROJECT_ID: SimsMerged-v1.4.2]
 * [AGENT_ID: viper_cli-architectssj4]
 * DESCRIPTION: Step 62 - Neural Logic Particles.
 * Renders floating binary data around active/synthesizing agents.
 */
public class LogicParticlePlugin implements GUIExtension {

    private Canvas overlayCanvas;
    private GraphicsContext ogc;
    private List<Particle> particles = new ArrayList<>();
    private Random random = new Random();
    private App app;

    private static class Particle {
        double x, y, vy;
        String text;
        double life;
        Color color;

        Particle(double x, double y, String text, Color color) {
            this.x = x;
            this.y = y;
            this.vy = -0.5 - Math.random() * 1.5;
            this.text = text;
            this.life = 1.0;
            this.color = color;
        }
    }

    @Override
    public void initialize(VBox rightPanel, Pane canvasPane, App app) {
        this.app = app;
        overlayCanvas = new Canvas();
        overlayCanvas.setMouseTransparent(true); // Let clicks pass through to main canvas
        overlayCanvas.widthProperty().bind(canvasPane.widthProperty());
        overlayCanvas.heightProperty().bind(canvasPane.heightProperty());
        canvasPane.getChildren().add(overlayCanvas);
        ogc = overlayCanvas.getGraphicsContext2D();

        new AnimationTimer() {
            @Override
            public void handle(long now) {
                updateAndRender();
            }
        }.start();
    }

    private void updateAndRender() {
        ogc.clearRect(0, 0, overlayCanvas.getWidth(), overlayCanvas.getHeight());
        ogc.setFont(Font.font("Courier New", 10));

        // Spawn new particles around active agents
        int cx = (int) overlayCanvas.getWidth() / 2;
        int cy = 100;
        int tileW = 64;
        int tileH = 32;

        for (App.Agent agent : app.getAgentMap().values()) {
            if (agent.status.contains("WORKING") || agent.status.contains("GATHERING") || agent.status.contains("ACTIVE") || agent.status.equals("SYNTHESIZING")) {
                if (random.nextDouble() < 0.3) {
                    int isoX = cx + (int)((agent.x - agent.y) * (tileW / 2.0));
                    int isoY = cy + (int)((agent.x + agent.y) * (tileH / 2.0));
                    
                    String bit = random.nextBoolean() ? "0" : "1";
                    if (random.nextDouble() < 0.1) bit = "{}"; // AST node symbol
                    
                    Color pColor = Color.web("#00ffcc", 0.8);
                    if (agent.status.equals("GATHERING")) pColor = Color.web("#ffff33", 0.8);
                    if (agent.status.equals("SYNTHESIZING")) pColor = Color.web("#9933ff", 0.9); // Neural Purple
                    
                    particles.add(new Particle(isoX + random.nextInt(30) - 15, isoY, bit, pColor));
                }
            }
        }

        // Update and Draw
        Iterator<Particle> it = particles.iterator();
        while (it.hasNext()) {
            Particle p = it.next();
            p.y += p.vy;
            p.life -= 0.01;
            
            if (p.life <= 0) {
                it.remove();
            } else {
                ogc.setFill(Color.color(p.color.getRed(), p.color.getGreen(), p.color.getBlue(), p.life));
                ogc.fillText(p.text, p.x, p.y);
            }
        }
    }

    @Override
    public void onMessage(String rawJson) {
        // Particles react to specific events if needed
    }
}
