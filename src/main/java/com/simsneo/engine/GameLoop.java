package com.simsneo.engine;

import javafx.animation.AnimationTimer;
import com.simsneo.view.WorldRenderer;

public class GameLoop extends AnimationTimer {
    private WorldRenderer renderer;
    private long lastUpdate = 0;

    public GameLoop(WorldRenderer renderer) {
        this.renderer = renderer;
    }

    @Override
    public void handle(long now) {
        if (now - lastUpdate >= 16_000_000) { // ~60 FPS
            renderer.render();
            lastUpdate = now;
        }
    }
}