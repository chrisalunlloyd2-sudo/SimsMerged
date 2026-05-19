package com.simsneo.engine;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.File;
import java.util.ArrayList;
import java.util.List;

/**
 * Step 901: Bridge the Sprite Engine to the JavaFX Canvas
 * Real-time data pipeline from the background Python daemon to the foreground GUI.
 */
public class SpriteBridge {
    private static final String PYTHON_EXE = "C:\\Users\\viper\\python\\python.exe";
    private static final String SPRITE_DB_PATH = "C:\\Users\\viper\\sprite_core\\context_fence\\db\\sprite.db";
    private final ObjectMapper mapper = new ObjectMapper();

    public List<AgentData> getActiveAgents() {
        List<AgentData> agents = new ArrayList<>();
        try {
            // Simplified: Query the SQLite database via a small Python helper or direct JDBC
            // For Step 901, we'll use a process call to get JSON status
            ProcessBuilder pb = new ProcessBuilder(PYTHON_EXE, "-c", 
                "import sqlite3, json, os; " +
                "conn = sqlite3.connect('" + SPRITE_DB_PATH.replace("\\", "/") + "'); " +
                "cursor = conn.cursor(); " +
                "cursor.execute('SELECT name, hardware_anchor, traits, hardware_uuid, trust_score FROM agent_profiles'); " +
                "rows = cursor.fetchall(); " +
                "print(json.dumps([{'name': r[0], 'anchor': r[1], 'traits': json.loads(r[2]), 'uuid': r[3], 'trust': r[4]} for r in rows])); " +
                "conn.close()");
            
            Process p = pb.start();
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String jsonOutput = in.readLine();
            
            if (jsonOutput != null && !jsonOutput.isEmpty()) {
                JsonNode root = mapper.readTree(jsonOutput);
                for (JsonNode node : root) {
                    agents.add(new AgentData(
                        node.get("name").asText(),
                        node.get("anchor").asText(),
                        node.get("traits"),
                        node.get("uuid").asText(),
                        node.get("trust").asDouble()
                    ));
                }
            }
        } catch (Exception e) {
            System.err.println("[BRIDGE ERROR] Failed to sync with Sprite Engine: " + e.getMessage());
        }
        return agents;
    }

    public GridStatus getGridStatus() {
        try {
            ProcessBuilder pb = new ProcessBuilder(PYTHON_EXE, "-c", 
                "import sqlite3, json, os, time; " +
                "conn = sqlite3.connect('" + SPRITE_DB_PATH.replace("\\", "/") + "'); " +
                "cursor = conn.cursor(); " +
                "cursor.execute('SELECT COUNT(*) FROM agent_profiles'); " +
                "agent_count = cursor.fetchone()[0]; " +
                "print(json.dumps({'nodes': 3, 'agents': agent_count})); " + // Simulated node count for now
                "conn.close()");
            
            Process p = pb.start();
            BufferedReader in = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String jsonOutput = in.readLine();
            
            if (jsonOutput != null && !jsonOutput.isEmpty()) {
                JsonNode root = mapper.readTree(jsonOutput);
                return new GridStatus(root.get("nodes").asInt(), root.get("agents").asInt());
            }
        } catch (Exception e) {
            System.err.println("[BRIDGE ERROR] Grid Status sync failed: " + e.getMessage());
        }
        return new GridStatus(1, 0);
    }

    public static class GridStatus {
        public int nodes;
        public int agents;
        public GridStatus(int n, int a) { this.nodes = n; this.agents = a; }
    }

    public static class AgentData {
        public String name;
        public String anchor;
        public JsonNode traits;
        public String uuid;
        public double trust;

        public AgentData(String name, String anchor, JsonNode traits, String uuid, double trust) {
            this.name = name;
            this.anchor = anchor;
            this.traits = traits;
            this.uuid = uuid;
            this.trust = trust;
        }
    }
}
