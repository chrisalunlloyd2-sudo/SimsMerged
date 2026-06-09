package com.simsneo.engine;

/**
 * Steps 51-60: The Isometric Mathematical Foundation
 * Provides the 2:1 projection logic for the grid.
 */
public class IsoMath {

    public static final int TILE_WIDTH = 64;
    public static final int TILE_HEIGHT = 32;

    /**
     * Step 52: World to Screen Transformation
     * Formula: x_iso = (x - y) * (tileWidth / 2)
     *          y_iso = (x + y) * (tileHeight / 4)
     */
    public static double worldToScreenX(int mapX, int mapY, double offsetX) {
        return offsetX + (mapX - mapY) * (TILE_WIDTH / 2.0);
    }

    public static double worldToScreenY(int mapX, int mapY, double offsetY) {
        return offsetY + (mapX + mapY) * (TILE_HEIGHT / 4.0);
    }

    /**
     * Step 53: Inverse Transformation (Screen to World)
     * Used for mouse picking.
     */
    public static int screenToWorldX(double screenX, double screenY, double offsetX, double offsetY) {
        double relX = screenX - offsetX;
        double relY = screenY - offsetY;
        return (int) Math.floor((relX / (TILE_WIDTH / 2.0) + relY / (TILE_HEIGHT / 4.0)) / 2.0);
    }

    public static int screenToWorldY(double screenX, double screenY, double offsetX, double offsetY) {
        double relX = screenX - offsetX;
        double relY = screenY - offsetY;
        return (int) Math.floor((relY / (TILE_HEIGHT / 4.0) - relX / (TILE_WIDTH / 2.0)) / 2.0);
    }
}
