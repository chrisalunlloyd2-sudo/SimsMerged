package com.simsmerged.gui;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.stage.Stage;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.WebSocket;
import java.util.concurrent.CompletionStage;
import java.util.List;
import java.util.ArrayList;
import org.json.JSONObject;
import org.json.JSONArray;

public class App extends Application {

    private ListView<String> chatList;
    private Canvas canvas;
    private GraphicsContext gc;
    private WebSocket webSocket;
    private int[][] worldMatrix;
    private int[][] thermalMatrix;
    private int worldSize = 0;
    private java.util.Map<String, Agent> agentMap = new java.util.concurrent.ConcurrentHashMap<>();
    private java.util.List<GUIExtension> extensions = new java.util.concurrent.CopyOnWriteArrayList<>();
    
    // Chronos State (Phase 13)
    private int gameHour = 12;
    private Color ambientColor = Color.web("#050505");
    private Color gridColor = Color.web("rgba(0, 255, 204, 0.15)");

    public static class Agent {
        public String id;
        public String address;
        public double x, y;
        public String status;
        public double balance;
        public java.util.Map<String, Integer> inventory = new java.util.HashMap<>();

        public Agent(String id, double x, double y) {
            this.id = id;
            this.address = "0x" + Integer.toHexString(id.hashCode()) + "00000000000000000";
            this.x = x;
            this.y = y;
            this.status = "ACTIVE";
            this.balance = 0.0;
        }
    }

    public WebSocket getWebSocket() { return webSocket; }
    public ListView<String> getChatList() { return chatList; }
    public java.util.Map<String, Agent> getAgentMap() { return agentMap; }

    @Override
    public void start(Stage primaryStage) {
        loadWorldMap();

        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #050505;");

        // --- ISOMETRIC CANVAS ---
        canvas = new Canvas(800, 600);
        gc = canvas.getGraphicsContext2D();
        Pane canvasPane = new Pane(canvas);
        root.setCenter(canvasPane);
        
        canvasPane.widthProperty().addListener((obs, oldVal, newVal) -> {
            canvas.setWidth(newVal.doubleValue());
            drawGrid();
        });
        canvasPane.heightProperty().addListener((obs, oldVal, newVal) -> {
            canvas.setHeight(newVal.doubleValue());
            drawGrid();
        });

        // --- UI PANEL ---
        VBox rightPanel = new VBox(10);
        rightPanel.setPadding(new Insets(10));
        rightPanel.setPrefWidth(300);
        rightPanel.setStyle("-fx-background-color: rgba(10, 15, 20, 0.9); -fx-border-color: #1a3a4a; -fx-border-width: 0 0 0 2;");

        // --- CHAPTER 7: MSN HEADER & STATUS ---
        HBox msnHeader = new HBox(10);
        msnHeader.setAlignment(javafx.geometry.Pos.CENTER_LEFT);
        
        Label msnLogo = new Label("(u)"); 
        msnLogo.setTextFill(Color.web("#00ffcc"));
        msnLogo.setStyle("-fx-font-size: 20px; -fx-font-weight: bold;");
        
        VBox statusBox = new VBox(2);
        Label title = new Label("METROPOLIS AUTHORITY");
        title.setTextFill(Color.web("#00ffcc"));
        title.setStyle("-fx-font-weight: bold; -fx-font-family: 'Courier New';");
        
        ComboBox<String> statusDropdown = new ComboBox<>();
        statusDropdown.getItems().addAll("Online", "Busy", "Be Right Back", "Appear Offline");
        statusDropdown.setValue("Online");
        statusDropdown.setStyle("-fx-background-color: #111; -fx-text-fill: #00ffcc; -fx-font-size: 9px;");
        
        statusBox.getChildren().addAll(title, statusDropdown);
        msnHeader.getChildren().addAll(msnLogo, statusBox);

        chatList = new ListView<>();
        chatList.setPrefHeight(400);
        chatList.setStyle("-fx-control-inner-background: #000000; -fx-text-fill: #00ffcc; -fx-font-family: 'Courier New';");

        TextField chatInput = new TextField();
        chatInput.setPromptText("Type /fund L3_PIONEER 10...");
        chatInput.setStyle("-fx-background-color: #111; -fx-text-fill: #00ffcc; -fx-border-color: #1a3a4a;");
        chatInput.setOnAction(e -> {
            String txt = chatInput.getText();
            if (!txt.isEmpty() && webSocket != null) {
                webSocket.sendText(txt, true);
                chatList.getItems().add("You: " + txt);
                chatInput.clear();
            }
        });

        Button btnSpawn = new Button("SPAWN AGENT");
        btnSpawn.setStyle("-fx-background-color: transparent; -fx-border-color: #1a3a4a; -fx-text-fill: #00ffcc;");
        btnSpawn.setOnAction(e -> chatList.getItems().add("[System] Agent spawn sequence initiated..."));

        // --- PHASE 6: GOD HAND CONTROLS ---
        Label fundingLabel = new Label("DEPIN FUNDING INJECTOR");
        fundingLabel.setTextFill(Color.web("#00ffcc"));
        fundingLabel.setStyle("-fx-font-size: 10px;");
        
        Slider depinSlider = new Slider(0, 100, 10);
        depinSlider.setShowTickLabels(true);
        depinSlider.setShowTickMarks(true);
        
        Button btnFund = new Button("INJECT FUNDS");
        btnFund.setStyle("-fx-background-color: #004444; -fx-text-fill: #00ffcc; -fx-border-color: #1a3a4a;");
        btnFund.setOnAction(e -> {
            String selected = "L3_PIONEER_01"; 
            double val = depinSlider.getValue();
            String cmd = "/fund " + selected + " " + String.format("%.1f", val);
            if (webSocket != null) {
                webSocket.sendText(cmd, true);
                chatList.getItems().add("God Hand: " + cmd);
            }
        });

        Button btnNudge = new Button("NUDGE");
        btnNudge.setStyle("-fx-background-color: #440022; -fx-text-fill: #ff3366; -fx-border-color: #ff3366;");
        btnNudge.setOnAction(e -> {
            if (webSocket != null) {
                webSocket.sendText("/nudge", true);
                shakeWindow(primaryStage);
            }
        });

        Label taskLabel = new Label("TASK ASSIGNMENT DAG");
        taskLabel.setTextFill(Color.web("#00ffcc"));
        taskLabel.setStyle("-fx-font-size: 10px;");

        ListView<String> taskList = new ListView<>();
        taskList.setPrefHeight(150);
        taskList.getItems().addAll("Gather Wood (Bounty: 5.0)", "Gather Stone (Bounty: 5.0)", "Build Delivery Hub (LOCKED)");
        taskList.setStyle("-fx-control-inner-background: #000; -fx-text-fill: #00ffcc;");
        taskList.setOnMouseClicked(e -> {
            String selected = taskList.getSelectionModel().getSelectedItem();
            if (selected != null && !selected.contains("LOCKED")) {
                String task = selected.split(" ")[1]; 
                String cmd = "/assign L3_PIONEER_01 " + task;
                if (webSocket != null) {
                    webSocket.sendText(cmd, true);
                    chatList.getItems().add("God Hand: " + cmd);
                }
            }
        });

        rightPanel.getChildren().addAll(msnHeader, new Separator(), chatList, chatInput, btnSpawn, new Separator(), fundingLabel, depinSlider, btnFund, btnNudge, new Separator(), taskLabel, taskList);
        root.setRight(rightPanel);

        canvas.setOnMouseClicked(e -> {
            int cx = (int) canvas.getWidth() / 2;
            int cy = 100;
            int tileW = 64;
            int tileH = 32;

            for (Agent a : agentMap.values()) {
                int isoX = cx + (int)((a.x - a.y) * (tileW / 2.0));
                int isoY = cy + (int)((a.x + a.y) * (tileH / 2.0));
                if (Math.abs(e.getX() - isoX) < 20 && Math.abs(e.getY() - isoY) < 20) {
                    updateDossier(a);
                    break;
                }
            }
        });

        Scene scene = new Scene(root, 1100, 600);
        primaryStage.setTitle("SimsMerged - JavaFX God Hand");
        primaryStage.setScene(scene);
        primaryStage.show();

        new javafx.animation.AnimationTimer() {
            @Override
            public void handle(long now) {
                drawGrid();
            }
        }.start();

        connectWebSocket();

        // Step 21.2: Register Plugins (The only place we will edit App.java from now on)
        registerExtension(new ContextClearingPlugin(), rightPanel, canvasPane);
        registerExtension(new LogitChartPlugin(), rightPanel, canvasPane);
        registerExtension(new ConsensusPlugin(), rightPanel, canvasPane);
        registerExtension(new WeatherPlugin(), rightPanel, canvasPane);
        registerExtension(new MailboxPlugin(), rightPanel, canvasPane);
        registerExtension(new EconomyDashboardPlugin(), rightPanel, canvasPane);
        registerExtension(new IssueTrackerPlugin(), rightPanel, canvasPane);
        registerExtension(new TelemetryDashboardPlugin(), rightPanel, canvasPane);
        registerExtension(new SupremeCourtPlugin(), rightPanel, canvasPane);
        registerExtension(new LogicParticlePlugin(), rightPanel, canvasPane);
        registerExtension(new GeneticMatrixPlugin(), rightPanel, canvasPane);
    }

    private void registerExtension(GUIExtension ext, VBox rightPanel, Pane canvasPane) {
        extensions.add(ext);
        ext.initialize(rightPanel, canvasPane, this);
    }

    private void loadWorldMap() {
        try {
            String path = "C:\\Users\\viper\\Desktop\\SimsMerged\\backend\\world_map.json";
            File file = new File(path);
            if (file.exists()) {
                String content = new String(Files.readAllBytes(Paths.get(path)));
                JSONObject obj = new JSONObject(content);
                worldSize = obj.getInt("size");
                JSONArray matrix = obj.getJSONArray("matrix");
                worldMatrix = new int[worldSize][worldSize];
                for (int i = 0; i < worldSize; i++) {
                    JSONArray row = matrix.getJSONArray(i);
                    for (int j = 0; j < worldSize; j++) {
                        worldMatrix[i][j] = row.getInt(j);
                    }
                }
            }
            
            // Step 13.3: Load Thermal Map
            String tPath = "C:\\Users\\viper\\Desktop\\SimsMerged\\backend\\thermal_map.json";
            File tFile = new File(tPath);
            if (tFile.exists()) {
                String tContent = new String(Files.readAllBytes(Paths.get(tPath)));
                JSONObject tObj = new JSONObject(tContent);
                JSONArray tMatrix = tObj.getJSONArray("matrix");
                thermalMatrix = new int[worldSize][worldSize];
                for (int i = 0; i < worldSize; i++) {
                    JSONArray tRow = tMatrix.getJSONArray(i);
                    for (int j = 0; j < worldSize; j++) {
                        thermalMatrix[i][j] = tRow.getInt(j);
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Failed to load map data: " + e.getMessage());
        }
    }

    private void drawGrid() {
        gc.setFill(ambientColor);
        gc.fillRect(0, 0, canvas.getWidth(), canvas.getHeight());

        int tileW = 64;
        int tileH = 32;
        int cx = (int) canvas.getWidth() / 2;
        int cy = 100;

        int renderRange = 30;

        if (worldMatrix == null) {
            gc.setStroke(gridColor);
            for (int x = 0; x < 20; x++) {
                for (int y = 0; y < 20; y++) {
                    drawTile(cx, cy, x, y, tileW, tileH, null, null);
                }
            }
            return;
        }

        for (int x = 0; x < Math.min(worldSize, renderRange); x++) {
            for (int y = 0; y < Math.min(worldSize, renderRange); y++) {
                Color tileColor;
                switch (worldMatrix[x][y]) {
                    case 0: tileColor = Color.web("#2d5a27"); break; // Grass
                    case 1: tileColor = Color.web("#1a3a4a"); break; // Water
                    case 2: tileColor = Color.web("#4a4a4a"); break; // Stone
                    default: tileColor = Color.web("#111"); break;
                }
                
                // Step 13.3: Calculate Thermal Overlay
                Color thermalOverlay = null;
                if (thermalMatrix != null) {
                    int temp = thermalMatrix[x][y];
                    if (temp > 50) thermalOverlay = Color.web("rgba(255, 0, 0, 0.4)"); // Hot
                    else if (temp < 10) thermalOverlay = Color.web("rgba(0, 0, 255, 0.3)"); // Cold
                }
                
                drawTile(cx, cy, x, y, tileW, tileH, tileColor, thermalOverlay);
            }
        }
        drawAgents(cx, cy, tileW, tileH);
    }

    private void drawAgents(int cx, int cy, int tileW, int tileH) {
        for (Agent agent : agentMap.values()) {
            int isoX = cx + (int)((agent.x - agent.y) * (tileW / 2.0));
            int isoY = cy + (int)((agent.x + agent.y) * (tileH / 2.0));

            Color agentColor = Color.web("#33ff66");
            if (agent.status.equals("SUSPENDED") || agent.status.equals("TRADING")) {
                agentColor = Color.web("#ff3366");
            } else if (agent.status.equals("GATHERING")) {
                agentColor = Color.web("#00ffcc");
            } else if (agent.status.equals("DELIVERING")) {
                agentColor = Color.web("#ffff33");
            }

            gc.setFill(agentColor);
            gc.fillOval(isoX - 5, isoY + 5, 10, 10);
            
            gc.setFill(Color.web("rgba(0,0,0,0.7)"));
            gc.fillRect(isoX - 30, isoY - 30, 60, 15);
            gc.setStroke(agentColor);
            gc.setLineWidth(0.5);
            gc.strokeRect(isoX - 30, isoY - 30, 60, 15);

            gc.setFill(agentColor);
            gc.setLineWidth(1.0);
            gc.setFont(javafx.scene.text.Font.font("Courier New", 9));
            gc.fillText(agent.status, isoX - 25, isoY - 18);

            gc.setFill(Color.WHITE);
            gc.fillText(agent.id, isoX - 10, isoY);
        }
    }

    private void drawTile(int cx, int cy, int x, int y, int tileW, int tileH, Color fill, Color overlay) {
        int isoX = cx + (x - y) * (tileW / 2);
        int isoY = cy + (x + y) * (tileH / 2);
        double[] xs = new double[]{isoX, isoX + tileW/2.0, isoX, isoX - tileW/2.0};
        double[] ys = new double[]{isoY, isoY + tileH/2.0, isoY + tileH, isoY + tileH/2.0};
        
        if (fill != null) {
            gc.setFill(fill);
            gc.fillPolygon(xs, ys, 4);
        }
        
        if (overlay != null) {
            gc.setFill(overlay);
            gc.fillPolygon(xs, ys, 4);
        }
        
        gc.setStroke(gridColor);
        gc.strokePolygon(xs, ys, 4);
    }

    private void updateDossier(Agent a) {
        Platform.runLater(() -> {
            StringBuilder sb = new StringBuilder();
            sb.append("ID: ").append(a.id).append("\n");
            sb.append("ADDR: ").append(a.address).append("\n");
            sb.append("Status: ").append(a.status).append("\n");
            sb.append("Inventory:\n");
            for (String item : a.inventory.keySet()) {
                sb.append(" - ").append(item).append(": ").append(a.inventory.get(item)).append("\n");
            }
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle("Agent Dossier");
            alert.setHeaderText(null);
            alert.setContentText(sb.toString());
            alert.show();
        });
    }

    private void shakeWindow(Stage stage) {
        javafx.animation.Timeline timeline = new javafx.animation.Timeline();
        javafx.scene.Node root = stage.getScene().getRoot();

        for (int i = 0; i < 10; i++) {
            double offset = (i % 2 == 0) ? 10 : -10;
            timeline.getKeyFrames().add(new javafx.animation.KeyFrame(
                javafx.util.Duration.millis(i * 50),
                new javafx.animation.KeyValue(root.translateXProperty(), offset)
            ));
        }
        timeline.getKeyFrames().add(new javafx.animation.KeyFrame(
            javafx.util.Duration.millis(500),
            new javafx.animation.KeyValue(root.translateXProperty(), 0)
        ));
        timeline.play();
    }

    private void connectWebSocket() {
        try {
            HttpClient client = HttpClient.newHttpClient();
            client.newWebSocketBuilder()
                  .buildAsync(URI.create("ws://127.0.0.1:8000/ws/chat/GodHandUI"), new WebSocket.Listener() {
                      @Override
                      public void onOpen(WebSocket webSocket) {
                          Platform.runLater(() -> chatList.getItems().add("[System] Connected to PulseCore."));
                          App.this.webSocket = webSocket;
                          WebSocket.Listener.super.onOpen(webSocket);
                      }
                      @Override
                      public CompletionStage<?> onText(WebSocket webSocket, CharSequence data, boolean last) {
                          Platform.runLater(() -> {
                              String raw = data.toString();
                              try {
                                  if (raw.startsWith("{")) {
                                      JSONObject json = new JSONObject(raw);
                                      if (json.has("type") && json.getString("type").equals("AGENT_UPDATE")) {
                                          String id = json.getString("agent_id");
                                          double nx = json.getDouble("x");
                                          double ny = json.getDouble("y");
                                          String stat = json.optString("status", "ACTIVE");
                                          Agent a = agentMap.computeIfAbsent(id, k -> new Agent(id, nx, ny));
                                          a.x = nx;
                                          a.y = ny;
                                          a.status = stat;
                                          if (json.has("inventory")) {
                                              JSONObject inv = json.getJSONObject("inventory");
                                              a.inventory.clear();
                                              for (String key : inv.keySet()) {
                                                  a.inventory.put(key, inv.getInt(key));
                                              }
                                          }
                                      } else if (json.has("type") && json.getString("type").equals("CHRONO_UPDATE")) {
                                          gameHour = json.getInt("hour");
                                          if (gameHour >= 6 && gameHour < 18) {
                                              ambientColor = Color.web("#050505");
                                              gridColor = Color.web("rgba(0, 255, 204, 0.15)");
                                          } else {
                                              ambientColor = Color.web("#0a001a");
                                              gridColor = Color.web("rgba(153, 51, 255, 0.2)");
                                          }
                                      } else if (json.has("type") && json.getString("type").equals("EVOLUTION_VOTE")) {
                                          chatList.getItems().add("--- COUNCIL CONVENED ---");
                                          chatList.getItems().add("Mod: " + json.getString("module"));
                                          chatList.getItems().add(">>> STATUS: " + json.getString("status"));
                                      } else if (raw.contains("/nudge")) {
                                          shakeWindow((Stage) canvas.getScene().getWindow());
                                      }
                                  } else {
                                      chatList.getItems().add(raw);
                                      if (raw.contains("/nudge")) shakeWindow((Stage) canvas.getScene().getWindow());
                                  }

                                  // Step 21.2: Notify Extensions
                                  for (GUIExtension ext : extensions) {
                                      ext.onMessage(raw);
                                  }
                              } catch (Exception e) {
                                  chatList.getItems().add(raw);
                              }
                              chatList.scrollTo(chatList.getItems().size() - 1);
                          });
                          return WebSocket.Listener.super.onText(webSocket, data, last);
                      }
                      @Override
                      public void onError(WebSocket webSocket, Throwable error) {
                          Platform.runLater(() -> chatList.getItems().add("[Error] Connection failed. Backend offline?"));
                      }
                  });
        } catch (Exception e) {
            chatList.getItems().add("[Error] " + e.getMessage());
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}
