package com.simsneo.model;

/**
 * Career and Employment logic.
 */
public class Job {
    private String title;
    private double hourlyWage;
    private int shiftStart; // 0-23
    private int shiftDuration;

    public Job(String title, double hourlyWage, int shiftStart, int shiftDuration) {
        this.title = title;
        this.hourlyWage = hourlyWage;
        this.shiftStart = shiftStart;
        this.shiftDuration = shiftDuration;
    }

    public String getTitle() { return title; }
    public double getHourlyWage() { return hourlyWage; }
    public int getShiftStart() { return shiftStart; }
    public int getShiftDuration() { return shiftDuration; }
}
