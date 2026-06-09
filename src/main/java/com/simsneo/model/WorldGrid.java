package com.simsneo.model;

import java.util.ArrayList;
import java.util.List;

/**
 * Step 55: The WorldGrid
 * A 2D array representing the geometric plane of the city.
 */
public class WorldGrid {
    private final int width;
    private final int height;
    private final Tile[][] grid;

    public WorldGrid(int width, int height) {
        this.width = width;
        this.height = height;
        this.grid = new Tile[width][height];
        initializeGrid();
    }

    private void initializeGrid() {
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                grid[x][y] = new Tile(x, y, Tile.TileType.GRASS);
            }
        }
    }

    /**
     * Step 902 & 1202: Global Grid Topology
     */
    public void generateGlobalTopology(List<String> remoteNodes) {
        // 1. Local Hardware Islands
        for (int x = 10; x < 20; x++) {
            for (int y = 10; y < 20; y++) {
                if (getTile(x, y) != null) grid[x][y] = new Tile(x, y, Tile.TileType.CONCRETE);
            }
        }
        
        // 2. Machine Continents (Remote Nodes)
        int index = 1;
        for (String ip : remoteNodes) {
            int offsetX = (index % 5) * 40;
            int offsetY = (index / 5) * 40;
            for (int x = offsetX; x < offsetX + 10; x++) {
                for (int y = offsetY; y < offsetY + 10; y++) {
                    Tile t = getTile(x, y);
                    if (t != null) grid[x][y] = new Tile(x, y, Tile.TileType.CARPET);
                }
            }
            index++;
        }
    }

    public Tile getTile(int x, int y) {
        if (x >= 0 && x < width && y >= 0 && y < height) {
            return grid[x][y];
        }
        return null;
    }

    /**
     * Step 56: Z-Order Indexing
     * Returns tiles sorted back-to-front for correct isometric rendering.
     */
    public List<Tile> getSortedTiles() {
        List<Tile> sorted = new ArrayList<>();
        for (int x = 0; x < width; x++) {
            for (int y = 0; y < height; y++) {
                sorted.add(grid[x][y]);
            }
        }
        // Depth-sorting: (x + y) determines the order
        sorted.sort((a, b) -> (a.getX() + a.getY()) - (b.getX() + b.getY()));
        return sorted;
    }

    private final List<Wall> walls = new ArrayList<>();
    private final List<GameObject> objects = new ArrayList<>();
    private final List<Sim> sims = new ArrayList<>();

    public void addSim(Sim sim) {
        sims.add(sim);
    }

    public List<Sim> getSims() {
        return sims;
    }

    public int getWidth() {
        return width;
    }

    public int getHeight() {
        return height;
    }

    public void addObject(GameObject obj) {
        objects.add(obj);
    }

    public List<GameObject> getObjects() {
        return objects;
    }

    public void addWall(Wall wall) {
        walls.add(wall);
    }

    public List<Wall> getWalls() {
        return walls;
    }
}
