package com.simsneo.engine;

/**
 * Step 251-260: The Game Clock
 * Manages minutes, hours, days, and time compression.
 */
public class GameClock {
    public enum Day { MON, TUE, WED, THU, FRI, SAT, SUN }

    private double speedMultiplier = 1.0; // 1x, 2x, 3x
    private double currentMinute = 0;
    private int currentHour = 8; // Start at 8 AM
    private Day currentDay = Day.MON;

    public void update(double deltaSeconds) {
        // 1 real second = 1 game minute at 1x speed
        currentMinute += deltaSeconds * speedMultiplier * 60.0;
        
        if (currentMinute >= 60.0) {
            currentMinute = 0;
            currentHour++;
        }

        if (currentHour >= 24) {
            currentHour = 0;
            advanceDay();
        }
    }

    private void advanceDay() {
        int next = (currentDay.ordinal() + 1) % Day.values().length;
        currentDay = Day.values()[next];
    }

    public void setSpeed(double multiplier) {
        this.speedMultiplier = multiplier;
    }

    public String getTimeString() {
        return String.format("%s %02d:00", currentDay, currentHour);
    }

    public int getHour() { return currentHour; }
    public Day getDay() { return currentDay; }
    public double getSpeed() { return speedMultiplier; }
}
