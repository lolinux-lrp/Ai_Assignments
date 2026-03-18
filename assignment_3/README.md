# Assignment 3

This assignment focuses on pathfinding and navigation algorithms for various environments, including road networks down to grid-based Unmanned Ground Vehicle (UGV) simulations.

## Contents

1. **`1_dijkstra_india.cpp`**: 
   Implements Dijkstra's algorithm (Uniform-Cost Search) to find the shortest navigational path and distance between major cities in India based on a predefined graph network.

2. **`2_ugv_static_obstacles.cpp`**: 
   Simulates a UGV navigating a 70x70 grid with static obstacles. It uses the **A* Search Algorithm** and tests the UGV against different map obstacle densities (low, medium, high) to evaluate the Measures of Effectiveness (path length, nodes expanded, execution time).

3. **`3_ugv_dynamic_obstacles.cpp`**: 
   Simulates a UGV navigating in a dynamic environment where obstacles can appear unexpectedly on the grid. It implements an **A* with Re-planning** strategy, enabling the UGV to detect a new obstacle blocking its trajectory and dynamically recalculate a new optimal detour path to the goal.

## How to Run

You will need a C++ compiler capable of compiling C++11 or later (like `g++` or `clang++`). Follow the steps below for each program:

### 1. Dijkstra on India Map
```bash
g++ 1_dijkstra_india.cpp -o dijkstra
./dijkstra
```

### 2. UGV Static Obstacles (A* Search)
```bash
g++ 2_ugv_static_obstacles.cpp -o ugv_static
./ugv_static
```

### 3. UGV Dynamic Obstacles (A* Re-planning)
```bash
g++ 3_ugv_dynamic_obstacles.cpp -o ugv_dynamic
./ugv_dynamic
```
