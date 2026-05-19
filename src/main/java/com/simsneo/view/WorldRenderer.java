package com.simsneo.view;

import com.simsneo.engine.IsoMath;
import com.simsneo.engine.Camera;
import com.simsneo.model.Tile;
import com.simsneo.model.WorldGrid;
import com.simsneo.model.GameObject;
import com.simsneo.model.Wall;
import com.simsneo.model.Sim;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import java.util.List;

/**
 * Step 51-100: The Isometric Rendering Engine
 */
public class WorldRenderer {

    private final WorldGrid world;
    private Camera camera;

    public WorldRenderer(WorldGrid world) {
        this.world = world;
        this.camera = new Camera(512, 100);
    }

    /**
     * Step 355: Optimized Z-Order Buffer
     * Ensures perfect isometric layering for 50+ objects.
     */
    public void render(GraphicsContext gc) {
        gc.setFill(Color.web("#000000"));
        gc.fillRect(0, 0, 1024, 768);

        // 1. Collect all renderable entities
        List<Tile> sortedTiles = world.getSortedTiles();
        
        // 2. Render Plane
        for (Tile tile : sortedTiles) {
            double sx = IsoMath.worldToScreenX(tile.getX(), tile.getY(), camera.getX());
            double sy = IsoMath.worldToScreenY(tile.getX(), tile.getY(), camera.getY());
            drawTile(gc, sx, sy, tile.getType().hexColor);

            // Step 355: Stable Depth sorting for dynamic objects
            // Objects at same coordinate as tile are drawn immediately after tile
            for (GameObject obj : world.getObjects()) {
                if (obj.getGridX() == tile.getX() && obj.getGridY() == tile.getY()) {
                    obj.render(gc, sx, sy);
                }
            }
            
            for (Sim sim : world.getSims()) {
                if (sim.getGridX() == tile.getX() && sim.getGridY() == tile.getY()) {
                    drawSim(gc, sx, sy, sim);
                }
            }

            for (Wall wall : world.getWalls()) {
                if (wall.getStartX() == tile.getX() && wall.getStartY() == tile.getY()) {
                    drawWall(gc, sx, sy, wall);
                }
            }
        }
    }

    /**
     * Step 151: Isometric Wall Rendering
     */
    private void drawWall(GraphicsContext gc, double x, double y, Wall wall) {
        double wallHeight = 50.0;
        gc.setFill(Color.web(wall.getWallpaperHex()));
        
        if (wall.isHorizontal()) {
            // Draw Right-facing wall
            double[] wx = {x, x + IsoMath.TILE_WIDTH / 2.0, x + IsoMath.TILE_WIDTH / 2.0, x};
            double[] wy = {y, y - IsoMath.TILE_HEIGHT / 2.0, y - IsoMath.TILE_HEIGHT / 2.0 - wallHeight, y - wallHeight};
            gc.fillPolygon(wx, wy, 4);
            gc.setStroke(Color.BLACK);
            gc.strokePolygon(wx, wy, 4);
        } else {
            // Draw Left-facing wall
            double[] wx = {x, x - IsoMath.TILE_WIDTH / 2.0, x - IsoMath.TILE_WIDTH / 2.0, x};
            double[] wy = {y, y - IsoMath.TILE_HEIGHT / 2.0, y - IsoMath.TILE_HEIGHT / 2.0 - wallHeight, y - wallHeight};
            gc.fillPolygon(wx, wy, 4);
            gc.setStroke(Color.BLACK);
            gc.strokePolygon(wx, wy, 4);
        }
    }

    /**
     * Step 110: Sim Sprite Rendering
     */
    private void drawSim(GraphicsContext gc, double x, double y, Sim sim) {
        // Simple retro cube for Sim body
        gc.setFill(Color.web("#ff0000"));
        gc.fillOval(x - 10, y - 25, 20, 40);
        
        // Plumbob (Visual Ping)
        if (sim.getName().contains("Security")) {
            gc.setFill(Color.GOLD); // High-trust DePIN color
        } else {
            gc.setFill(Color.web("#00ff00"));
        }
        double[] px = {x, x+5, x, x-5};
        double[] py = {y-45, y-40, y-35, y-40};
        gc.fillPolygon(px, py, 4);

        gc.setFill(Color.WHITE);
        gc.setFont(Font.font("Arial", 10));
        gc.fillText(sim.getName(), x - 20, y - 50);

        // Step 904: Data Traffic Visual Effects
        if (sim.getName().contains("Sprite")) {
            gc.setStroke(Color.CYAN);
            gc.setLineWidth(1);
            gc.strokeLine(x, y - 20, x + (Math.random() * 20 - 10), y - 60 - (Math.random() * 20));
        }
    }

    /**
     * Step 58: Brute-Force Pixel Gap prevention
     */
    private void drawTile(GraphicsContext gc, double x, double y, String colorHex) {
        gc.setFill(Color.web(colorHex));
        
        // Build the diamond path
        double[] xPoints = {
            x, 
            x + IsoMath.TILE_WIDTH / 2.0, 
            x, 
            x - IsoMath.TILE_WIDTH / 2.0
        };
        double[] yPoints = {
            y - IsoMath.TILE_HEIGHT / 2.0, 
            y, 
            y + IsoMath.TILE_HEIGHT / 2.0, 
            y
        };

        gc.fillPolygon(xPoints, yPoints, 4);
        
        // Step 58: Stroke to prevent gaps
        gc.setStroke(Color.web(colorHex).darker());
        gc.setLineWidth(0.5);
        gc.strokePolygon(xPoints, yPoints, 4);
    }
    
    public Camera getCamera() {
        return camera;
    }
}
