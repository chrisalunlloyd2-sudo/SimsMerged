package com.simsneo.engine;

import com.simsneo.model.Sim;
import com.simsneo.model.Wall;
import com.simsneo.model.Furniture;
import com.simsneo.model.WorldGrid;
import com.simsneo.view.WorldRenderer;
import com.simsneo.view.HUD;
import javafx.animation.AnimationTimer;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import java.util.List;
import java.util.ArrayList;

public class GameLoop extends AnimationTimer {

    public static GameLoop instance;
    private GraphicsContext gc;
    private HUD hud;
    private long lastUpdate = 0;
    private WorldGrid world;
    private WorldRenderer renderer;
    private GameClock clock;
    private CareerSystem careers;
    private EventDispatcher events;

    private int lastProcessedHour = -1;

    public GameLoop(GraphicsContext gc, HUD hud) {
        instance = this;
        this.gc = gc;
        this.hud = hud;
        this.world = new WorldGrid(128, 128); // Expanded for Global Grid
        
        // Step 903 & 1202: Sync agents and nodes
        SpriteBridge bridge = new SpriteBridge();
        List<SpriteBridge.AgentData> agents = bridge.getActiveAgents();
        List<String> remoteNodes = new ArrayList<>(); // In real deployment, fetch from Sprite DB
        
        this.world.generateGlobalTopology(remoteNodes);
        this.renderer = new WorldRenderer(world);
        this.clock = new GameClock();
        this.careers = new CareerSystem();
        this.events = new EventDispatcher();
        
        // Step 903: Map System Processes to Agent Sprites
        for (SpriteBridge.AgentData data : agents) {
            Sim agentSim = new Sim(data.name, 10 + (int)(Math.random() * 10), 10 + (int)(Math.random() * 10));
            this.world.addSim(agentSim);
        }

        if (this.world.getSims().isEmpty()) {
            this.world.addSim(new Sim("SimNeo_01", 5, 5));
        }

        // Step 151: Construction
        this.world.addWall(new Wall(5, 5, true));
        this.world.addWall(new Wall(5, 5, false));

        // Step 201: Objects
        this.world.addObject(new Furniture("Fridge", 5, 5, 1, 1, 0, 1, 600.0, "#ffffff"));
    }

    private long lastGridSync = 0;

    @Override
    public void handle(long now) {
        if (lastUpdate == 0) {
            lastUpdate = now;
            return;
        }
        
        double deltaSeconds = (now - lastUpdate) / 1_000_000_000.0;
        
        // Step 251-300: Time Orchestration
        clock.update(deltaSeconds);
        
        // Step 1401: Total Grid Synchronization (Every 2 seconds for high-fidelity telemetry)
        if (now - lastGridSync > 2_000_000_000L) {
            SpriteBridge bridge = new SpriteBridge();
            SpriteBridge.MetropolisState state = bridge.getMetropolisState();
            if (state != null) {
                hud.updateMetropolisState(state);
            }
            lastGridSync = now;
        }

        // Hourly Triggers
        int currentHour = clock.getHour();
        if (currentHour != lastProcessedHour) {
            for (Sim s : world.getSims()) {
                careers.checkCarpool(s, currentHour);
            }
            events.checkRandomEvents(world, currentHour);
            lastProcessedHour = currentHour;
        }

        // Step 103: Update Agent Nervous System
        for (Sim sim : world.getSims()) {
            sim.updateMotives(deltaSeconds * clock.getSpeed());
        }

        // Step 1201: Smooth Camera Update
        renderer.getCamera().update(0.1);

        // Step 351: Recursive Hardening
        SystemIntegrity.validateSimInteractions(world);

        renderer.render(gc);

        
        // UI Dashboard (Step 301-350)
        hud.update(clock, world.getSims().get(0));

        lastUpdate = now;
    }

    public void setSpeed(double s) {
        clock.setSpeed(s);
    }

    private Sim selectedSim = null;
    private boolean dragging = false;

    public Sim pickSim(double sx, double sy) {
        for (Sim sim : world.getSims()) {
            double ssx = IsoMath.worldToScreenX(sim.getGridX(), sim.getGridY(), renderer.getCamera().getX());
            double ssy = IsoMath.worldToScreenY(sim.getGridX(), sim.getGridY(), renderer.getCamera().getY());
            if (Math.abs(ssx - sx) < 20 && Math.abs(ssy - sy) < 40) {
                return sim;
            }
        }
        return null;
    }

    public void setSelectedSim(Sim sim) { this.selectedSim = sim; }
    public void startDragging() { this.dragging = true; }
    public boolean isDragging() { return dragging; }

    public double[] screenToWorld(double sx, double sy) {
        double x = IsoMath.screenToWorldX(sx, sy, renderer.getCamera().getX(), renderer.getCamera().getY());
        double y = IsoMath.screenToWorldY(sx, sy, renderer.getCamera().getX(), renderer.getCamera().getY());
        return new double[]{x, y};
    }

    public void dropSim(int x, int y) {
        if (selectedSim != null) {
            selectedSim.setGridX(x);
            selectedSim.setGridY(y);
            System.out.println("[GRID] Sim dropped at " + x + ", " + y + ". Initiating remote task.");
            // Step 1203: Remote Task Initiation logic would go here
        }
        this.dragging = false;
    }

    public Camera getCamera() { return renderer.getCamera(); }
}
