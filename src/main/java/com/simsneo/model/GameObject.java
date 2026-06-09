package com.simsneo.model;

import javafx.scene.canvas.GraphicsContext;

/**
 * Step 202: The GameObject Interface
 * Defines logic for interactable items in the world.
 */
public interface GameObject {
    String getName();
    int getGridX();
    int getGridY();
    int getWidth();  // Width in tiles
    int getHeight(); // Height in tiles
    
    // Interaction Slots (Step 203)
    // Relative coordinates where a Sim stands to use the object
    int getSlotX();
    int getSlotY();

    double getPrice();
    double getDepreciationRate();
    
    void render(GraphicsContext gc, double x, double y);
}
