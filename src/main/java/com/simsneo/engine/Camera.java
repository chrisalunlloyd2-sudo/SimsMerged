package com.simsneo.engine;

/**
 * Step 57: The Camera Class
 * Manages viewport offsets for panning and focal points.
 */
public class Camera {
    private double x, y;
    private double targetX, targetY;

    public Camera(double x, double y) {
        this.x = x;
        this.y = y;
        this.targetX = x;
        this.targetY = y;
    }

    public void pan(double dx, double dy) {
        this.targetX += dx;
        this.targetY += dy;
    }

    public void update(double lerp) {
        x += (targetX - x) * lerp;
        y += (targetY - y) * lerp;
    }

    public double getX() { return x; }
    public void setX(double x) { this.x = x; this.targetX = x; }
    public double getY() { return y; }
    public void setY(double y) { this.y = y; this.targetY = y; }
}
