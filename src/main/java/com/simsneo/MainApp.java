package com.simsneo;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.StackPane;
import javafx.scene.paint.Color;
import javafx.scene.layout.BorderPane;
import com.simsneo.view.HUD;
import com.simsneo.model.Sim;
import javafx.scene.input.KeyEvent;
import javafx.stage.Stage;
import com.simsneo.engine.GameLoop;

public class MainApp extends Application {

    public static final int WINDOW_WIDTH = 1024;
    public static final int WINDOW_HEIGHT = 768;

    @Override
    public void start(Stage primaryStage) {
        BorderPane root = new BorderPane();

        Canvas canvas = new Canvas(WINDOW_WIDTH, WINDOW_HEIGHT - 150);
        GraphicsContext gc = canvas.getGraphicsContext2D();

        HUD hud = new HUD();

        root.setCenter(canvas);
        root.setBottom(hud);

        Scene scene = new Scene(root, WINDOW_WIDTH, WINDOW_HEIGHT);

        // Step 304 & 1201: Keyboard Master Hotkeys and Navigation
        scene.addEventHandler(KeyEvent.KEY_PRESSED, (key) -> {
            switch(key.getCode()) {
                case DIGIT1: GameLoop.instance.setSpeed(1.0); break;
                case DIGIT2: GameLoop.instance.setSpeed(2.0); break;
                case DIGIT3: GameLoop.instance.setSpeed(3.0); break;
                case P: GameLoop.instance.setSpeed(0.0); break; // Pause
                
                // Step 1201: Navigation
                case W: GameLoop.instance.getCamera().pan(0, -20); break;
                case S: GameLoop.instance.getCamera().pan(0, 20); break;
                case A: GameLoop.instance.getCamera().pan(-20, 0); break;
                case D: GameLoop.instance.getCamera().pan(20, 0); break;
            }
        });

        // Step 1203: Drag and Drop Automation
        canvas.setOnMousePressed(e -> {
            Sim target = GameLoop.instance.pickSim(e.getX(), e.getY());
            if (target != null) {
                GameLoop.instance.setSelectedSim(target);
                GameLoop.instance.startDragging();
            }
        });

        canvas.setOnMouseReleased(e -> {
            if (GameLoop.instance.isDragging()) {
                double[] worldCoord = GameLoop.instance.screenToWorld(e.getX(), e.getY());
                GameLoop.instance.dropSim((int)worldCoord[0], (int)worldCoord[1]);
            }
        });

        primaryStage.setTitle("Sims JavaFX Neo - 1700-Step Expansion");
        primaryStage.setScene(scene);
        primaryStage.show();

        GameLoop gameLoop = new GameLoop(gc, hud);
        gameLoop.start();
    }


    public static void main(String[] args) {
        launch(args);
    }
}
