package com.simsneo.engine;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/**
 * Step 901: Bridge the Sprite Engine to the JavaFX Canvas
 * Real-time data pipeline from the background Python daemon to the foreground GUI.
 */
public class SpriteBridge {
    private static final String API_URL = "http://localhost:8000/api/metropolis-state";
    private final ObjectMapper mapper = new ObjectMapper();
    private final HttpClient httpClient = HttpClient.newHttpClient();

    public MetropolisState getMetropolisState() {
        try {
            HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(API_URL))
                .GET()
                .build();
            
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() == 200) {
                return mapper.readValue(response.body(), MetropolisState.class);
            }
        } catch (Exception e) {
            System.err.println("[BRIDGE ERROR] Failed to sync with Metropolis Authority: " + e.getMessage());
        }
        return null;
    }

    public List<AgentData> getActiveAgents() {
        MetropolisState state = getMetropolisState();
        if (state != null && state.agents != null) {
            return state.agents;
        }
        return new ArrayList<>();
    }

    public static class MetropolisState {
        public List<AgentData> agents;
        public HardwareState hardware;
        public EconomyState economy;
        public List<JsonNode> chat;
        public List<BuildLabTask> build_lab;
        public WisdomTreeSummary wisdom_tree;
    }

    public static class WisdomTreeSummary {
        public int total_blocks;
        public double efficiency;
        public List<String> latest_components;
    }

    public static class BuildLabTask {
        public String id;
        public String component;
        public String status;
        public String requirement;
    }

    public static class HardwareState {
        public double stability;
        public double heat;
        public double frequency;
        public double ram_load;
        public boolean is_refreshing;
        public Map<String, Double> core_load;
    }

    public static class EconomyState {
        public double treasury_balance;
        public double mint_rate;
    }

    public static class AgentData {
        public String name;
        public String id;
        public String role;
        public List<String> traits;

        public AgentData() {} // For Jackson
    }

    public static class Point {
        public double x, y;
        public Point(double x, double y) { this.x = x; this.y = y; }
    }

    public static class TrajectoryData {
        public Point start;
        public Point end;
        public Point control;
        public String protocol;

        public TrajectoryData(Point start, Point end, Point control, String protocol) {
            this.start = start;
            this.end = end;
            this.control = control;
            this.protocol = protocol;
        }
    }

    public TrajectoryData calculateParabolicArc(Point start, Point end) {
        // Calculate a control point for a quadratic curve to create a parabolic arc
        double midX = (start.x + end.x) / 2;
        double midY = (start.y + end.y) / 2 - 100; // Offset for the arc height
        Point control = new Point(midX, midY);
        return new TrajectoryData(start, end, control, "BUS");
    }
}
