package com.simsneo.model;

/**
 * Step 152: The Wall Data Model
 * Represents a structural boundary between tiles.
 */
public class Wall {
    private int startX, startY;
    private int endX, endY;
    private boolean horizontal; // Horizontal or Vertical orientation
    private String wallpaperHex = "#d3d3d3"; // Default light gray

    public Wall(int x, int y, boolean horizontal) {
        this.startX = x;
        this.startY = y;
        this.horizontal = horizontal;
        if (horizontal) {
            this.endX = x + 1;
            this.endY = y;
        } else {
            this.endX = x;
            this.endY = y + 1;
        }
    }

    public int getStartX() { return startX; }
    public int getStartY() { return startY; }
    public boolean isHorizontal() { return horizontal; }
    public String getWallpaperHex() { return wallpaperHex; }
    public void setWallpaperHex(String hex) { this.wallpaperHex = hex; }
}
