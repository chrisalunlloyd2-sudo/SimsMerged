package com.simsneo.model;

import javafx.scene.paint.Color;

/**
 * Step 54: The Tile Object
 */
public class Tile {
    public enum TileType {
        GRASS("#008000"),
        CONCRETE("#808080"),
        CARPET("#a52a2a"),
        WATER("#0000ff");

        public final String hexColor;
        TileType(String hexColor) { this.hexColor = hexColor; }
    }

    private int x, y;
    private TileType type;

    public Tile(int x, int y, TileType type) {
        this.x = x;
        this.y = y;
        this.type = type;
    }

    public int getX() { return x; }
    public int getY() { return y; }
    public TileType getType() { return type; }
    public void setType(TileType type) { this.type = type; }
}
