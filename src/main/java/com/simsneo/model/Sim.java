package com.simsneo.model;

import java.util.HashMap;
import java.util.Map;

/**
 * Steps 101-110: The Sim Class (Agent DNA)
 * Implements OpenClaw Motives and Personality Traits.
 */
public class Sim {
    public enum Motive {
        HUNGER, COMFORT, HYGIENE, BLADDER, ENERGY, FUN, SOCIAL, ROOM
    }

    public enum Trait {
        NEAT, OUTGOING, ACTIVE, PLAYFUL, NICE
    }

    private String name;
    private int gridX, gridY;
    private double screenX, screenY;
    
    private Map<Motive, Double> motives = new HashMap<>();
    private Map<Trait, Integer> personality = new HashMap<>();
    private Map<String, Relationship> relationships = new HashMap<>();
    private Job job;
    private double wallet = 100.0;
    private double stability = 1.0;
    private String emotionalState = "STABLE";
    
    private SimState state = SimState.IDLE;

    public enum SimState {
        IDLE, MOVING, INTERACTING, ROUTING, WORKING, BINDING
    }

    public Sim(String name, int x, int y) {
        this.name = name;
        this.gridX = x;
        this.gridY = y;
        initializeMotives();
        initializePersonality();
    }

    public void setJob(Job job) { this.job = job; }
    public Job getJob() { return job; }
    public double getWallet() { return wallet; }
    public void addMoney(double amount) { this.wallet += amount; }

    public void addRelationship(Sim other) {
        relationships.put(other.getName(), new Relationship(other));
    }

    public Relationship getRelationship(String name) {
        return relationships.get(name);
    }

    private void initializeMotives() {
        for (Motive m : Motive.values()) {
            motives.put(m, 100.0); // Start at full strength
        }
    }

    private void initializePersonality() {
        // Default balanced personality (1-10 scale)
        for (Trait t : Trait.values()) {
            personality.put(t, 5);
        }
    }

    /**
     * Step 103: MotiveDecay Logic
     * Depletes stats over time.
     */
    public void updateMotives(double deltaSeconds) {
        // Different motives decay at different rates
        decay(Motive.HUNGER, 0.5 * deltaSeconds);
        decay(Motive.ENERGY, 0.3 * deltaSeconds);
        decay(Motive.HYGIENE, 0.2 * deltaSeconds);
        decay(Motive.BLADDER, 0.4 * deltaSeconds);
        // ... more decay logic based on personality
    }

    private void decay(Motive m, double amount) {
        double current = motives.get(m);
        motives.put(m, Math.max(0, current - amount));
    }

    public String getName() { return name; }
    public int getGridX() { return gridX; }
    public void setGridX(int x) { this.gridX = x; }
    public int getGridY() { return gridY; }
    public void setGridY(int y) { this.gridY = y; }
    public double getMotive(Motive m) { return motives.getOrDefault(m, 0.0); }
    public SimState getState() { return state; }
    public void setState(SimState state) { this.state = state; }
    public double getStability() { return stability; }
    public void setStability(double stability) { this.stability = stability; }
    public String getEmotionalState() { return emotionalState; }
    public void setEmotionalState(String emotionalState) { this.emotionalState = emotionalState; }
}
