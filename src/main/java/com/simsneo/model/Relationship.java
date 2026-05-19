package com.simsneo.model;

/**
 * Social dynamics between Sims.
 */
public class Relationship {
    private Sim target;
    private int dailyScore;   // -100 to 100
    private int lifetimeScore; // -100 to 100

    public Relationship(Sim target) {
        this.target = target;
        this.dailyScore = 0;
        this.lifetimeScore = 0;
    }

    public void adjustScore(int amount) {
        this.dailyScore = Math.max(-100, Math.min(100, this.dailyScore + amount));
        this.lifetimeScore = Math.max(-100, Math.min(100, this.lifetimeScore + amount));
    }

    public Sim getTarget() { return target; }
    public int getDailyScore() { return dailyScore; }
    public int getLifetimeScore() { return lifetimeScore; }
}
