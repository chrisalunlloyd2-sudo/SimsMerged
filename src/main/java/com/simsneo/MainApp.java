package com.simsneo;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.BorderPane;
import javafx.stage.Stage;
import com.simsneo.engine.GameLoop;
import com.simsneo.view.WorldRenderer;

public class MainApp extends Application {
    @Override
    public void start(Stage primaryStage) {
        BorderPane root = new BorderPane();
        WorldRenderer renderer = new WorldRenderer();
        root.setCenter(renderer);
        
        Scene scene = new Scene(root, 1024, 768);
        primaryStage.setTitle("Final Boss Automation - Sims Neo");
        primaryStage.setScene(scene);
        primaryStage.show();
        
        GameLoop loop = new GameLoop(renderer);
        loop.start();
    }
    public static void main(String[] args) {
        launch(args);
    }
}