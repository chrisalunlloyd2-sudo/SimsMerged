package com.simsneo.engine;

import com.simsneo.model.WorldGrid;
import java.util.*;

/**
 * Step 107: Pathfinding DNA (A-Star Algorithm)
 */
public class Pathfinding {

    public static class Node {
        public int x, y;
        public double g, h;
        public Node parent;

        public Node(int x, int y) {
            this.x = x;
            this.y = y;
        }

        public double f() { return g + h; }
    }

    public static List<int[]> findPath(WorldGrid world, int startX, int startY, int endX, int endY) {
        PriorityQueue<Node> openSet = new PriorityQueue<>(Comparator.comparingDouble(Node::f));
        Set<String> closedSet = new HashSet<>();

        Node startNode = new Node(startX, startY);
        Node endNode = new Node(endX, endY);
        openSet.add(startNode);

        while (!openSet.isEmpty()) {
            Node current = openSet.poll();
            String posKey = current.x + "," + current.y;

            if (current.x == endX && current.y == endY) {
                return reconstructPath(current);
            }

            closedSet.add(posKey);

            int[][] neighbors = {{0,1}, {0,-1}, {1,0}, {-1,1}}; // 4-way movement for simplicity
            for (int[] offset : neighbors) {
                int nx = current.x + offset[0];
                int ny = current.y + offset[1];

                if (nx < 0 || nx >= world.getWidth() || ny < 0 || ny >= world.getHeight()) continue;
                if (closedSet.contains(nx + "," + ny)) continue;

                Node neighbor = new Node(nx, ny);
                neighbor.g = current.g + 1;
                neighbor.h = Math.abs(nx - endX) + Math.abs(ny - endY);
                neighbor.parent = current;

                openSet.add(neighbor);
            }
        }
        return null;
    }

    private static List<int[]> reconstructPath(Node node) {
        List<int[]> path = new ArrayList<>();
        while (node != null) {
            path.add(0, new int[]{node.x, node.y});
            node = node.parent;
        }
        return path;
    }
}
