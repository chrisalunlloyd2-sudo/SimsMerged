package com.simsneo.model;

import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import com.simsneo.engine.IsoMath;

/**
 * Step 201: The Furniture Object
 */
public class Furniture implements GameObject {
    private String name;
    private int x, y;
    private int width, height;
    private int slotOffsetX, slotOffsetY;
    private double price;
    private double depreciationRate;
    private Color color;

    public Furniture(String name, int x, int y, int w, int h, int sx, int sy, double price, String hexColor) {
        this.name = name;
        this.x = x;
        this.y = y;
        this.width = w;
        this.height = h;
        this.slotOffsetX = sx;
        this.slotOffsetY = sy;
        this.price = price;
        this.depreciationRate = 0.05; // 5% per day
        this.color = Color.web(hexColor);
    }

    @Override public String getName() { return name; }
    @Override public int getGridX() { return x; }
    @Override public int getGridY() { return y; }
    @Override public int getWidth() { return width; }
    @Override public int getHeight() { return height; }
    @Override public int getSlotX() { return x + slotOffsetX; }
    @Override public int getSlotY() { return y + slotOffsetY; }
    @Override public double getPrice() { return price; }
    @Override public double getDepreciationRate() { return depreciationRate; }

    @Override
    public void render(GraphicsContext gc, double x, double y) {
        // Step 201: Render as a 3D isometric cube
        double h = 30.0;
        gc.setFill(color);
        
        // Base diamond
        double[] bx = {x, x + IsoMath.TILE_WIDTH/2.0, x, x - IsoMath.TILE_WIDTH/2.0};
        double[] by = {y - IsoMath.TILE_HEIGHT/2.0, y, y + IsoMath.TILE_HEIGHT/2.0, y};
        
        // Lift to 3D
        double[] tx = {x, x + IsoMath.TILE_WIDTH/2.0, x, x - IsoMath.TILE_WIDTH/2.0};
        double[] ty = {y - IsoMath.TILE_HEIGHT/2.0 - h, y - h, y + IsoMath.TILE_HEIGHT/2.0 - h, y - h};
        
        gc.fillPolygon(tx, ty, 4);
        gc.setStroke(Color.BLACK);
        gc.strokePolygon(tx, ty, 4);
        
        // Sides
        gc.setFill(color.darker());
        double[] sx = {tx[3], tx[2], tx[2], tx[3]};
        double[] sy = {ty[3], ty[2], y + IsoMath.TILE_HEIGHT/2.0, y};
        gc.fillPolygon(sx, sy, 4);
        gc.strokePolygon(sx, sy, 4);
    }
}
