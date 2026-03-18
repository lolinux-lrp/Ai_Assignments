/*
Dynamic Obstacle Environment - Algorithm Design & Simulation

Q: How do you make the UGV navigate and find the optimal path in a dynamic obstacles environment?

Theoretical Answer:
In a real-world scenario where obstacles appear, disappear, or move dynamically, a static 
planning algorithm like standard A* will be inefficient because it has to recalculate the 
entire path from scratch every time an obstacle blocks its route.

Recommended Algorithms:
1. D* Lite (Dynamic A* Lite): 
   This is the industry standard heuristic search algorithm for navigation in unknown or 
   changing terrain. It plans backwards from the goal to the start. 
   When the UGV's sensors detect a new obstacle, D* Lite only updates the heuristic costs 
   of the specific nodes affected by the change, reusing the previously computed map. 
   This makes it extraordinarily efficient compared to recalculating everything.

2. A* with Re-planning:
   In environments where obstacle changes are infrequent, the UGV can rely on standard 
   A* to compute a path. As it moves step-by-step, it scans ahead. If an unexpected 
   obstacle appears on its planned trajectory, it marks the obstacle on its internal grid 
   map and triggers a brand-new A* search from its *current* coordinates to the goal.

Below is a C++ demonstration of the "A* with Re-planning" strategy on a dynamic map.
*/

#include <iostream>
#include <vector>
#include <cmath>
#include <queue>
#include <map>
#include <algorithm>

using namespace std;

struct Node {
    int x, y;
    bool operator==(const Node& other) const { return x == other.x && y == other.y; }
    bool operator!=(const Node& other) const { return !(*this == other); }
    bool operator<(const Node& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
};

double heuristic(Node a, Node b) {
    int dx = abs(a.x - b.x);
    int dy = abs(a.y - b.y);
    return (dx + dy) + (1.414 - 2) * min(dx, dy);
}

vector<pair<Node, double>> getNeighbors(const vector<vector<int>>& grid, Node n) {
    int width = grid[0].size();
    int height = grid.size();
    vector<pair<Node, double>> neighbors;
    int dx[] = {0, 1, 0, -1, 1, 1, -1, -1};
    int dy[] = {1, 0, -1, 0, 1, -1, 1, -1};
    
    for (int i = 0; i < 8; ++i) {
        int nx = n.x + dx[i];
        int ny = n.y + dy[i];
        if (nx >= 0 && nx < width && ny >= 0 && ny < height && grid[ny][nx] == 0) {
            double cost = (dx[i] != 0 && dy[i] != 0) ? 1.414 : 1.0;
            neighbors.push_back({{nx, ny}, cost});
        }
    }
    return neighbors;
}

vector<Node> aStarSearch(const vector<vector<int>>& grid, Node start, Node goal) {
    priority_queue<pair<double, Node>, vector<pair<double, Node>>, greater<pair<double, Node>>> pq;
    map<Node, double> g_score;
    map<Node, Node> came_from;
    
    pq.push({0 + heuristic(start, goal), start});
    g_score[start] = 0;
    
    bool found = false;
    
    while (!pq.empty()) {
        Node current = pq.top().second;
        pq.pop();
        
        if (current == goal) {
            found = true;
            break;
        }
        
        for (auto& edge : getNeighbors(grid, current)) {
            Node neighbor = edge.first;
            double cost = edge.second;
            double tentative_g = g_score[current] + cost;
            
            if (g_score.find(neighbor) == g_score.end() || tentative_g < g_score[neighbor]) {
                g_score[neighbor] = tentative_g;
                double f_score = tentative_g + heuristic(neighbor, goal);
                pq.push({f_score, neighbor});
                came_from[neighbor] = current;
            }
        }
    }
    
    vector<Node> path;
    if (found) {
        Node curr = goal;
        while (curr != start) {
            path.push_back(curr);
            curr = came_from[curr];
        }
        path.push_back(start);
        reverse(path.begin(), path.end());
    }
    return path;
}

int main() {
    int width = 20, height = 20;
    vector<vector<int>> grid(height, vector<int>(width, 0));
    
    Node start = {0, 0};
    Node goal = {19, 19};
    Node current_pos = start;
    
    cout << "--- Dynamic Obstacle UGV Simulation ---\n";
    cout << "Initial Planning from (" << start.x << "," << start.y << ") to (" << goal.x << "," << goal.y << ")...\n";
    
    vector<Node> planned_path = aStarSearch(grid, current_pos, goal);
    cout << "Path plotted successfully. Expects " << planned_path.size() << " steps.\n";
    
    int steps_taken = 0;
    
    while (current_pos != goal) {
        if (planned_path.size() > 1) {
            Node next_step = planned_path[1];
            
            // SIMULATION EVENT: At step 5, an obstacle appears ahead!
            if (steps_taken == 5) {
                if (planned_path.size() > 3) {
                    Node ob = planned_path[3];
                    cout << "\n[SENSOR ALERT] Dynamic obstacle detected ahead at (" << ob.x << ", " << ob.y << ")!\n";
                    grid[ob.y][ob.x] = 1; // Mark obstacle
                    
                    // Check if planned path is blocked
                    bool blocked = false;
                    for (const auto& p : planned_path) {
                        if (grid[p.y][p.x] == 1) {
                            blocked = true;
                            break;
                        }
                    }
                    
                    if (blocked) {
                        cout << "Current trajectory invalidated. Re-planning from current position (" << current_pos.x << "," << current_pos.y << ")...\n";
                        planned_path = aStarSearch(grid, current_pos, goal);
                        
                        if (planned_path.empty()) {
                            cout << "CRITICAL: All routes to the target are blocked. UGV must stop.\n";
                            break;
                        }
                        cout << "New detour path found! Detour will take " << planned_path.size() << " steps.\n";
                        next_step = planned_path[1];
                    }
                }
            }
            
            current_pos = next_step;
            planned_path.erase(planned_path.begin()); // Remove previous node
            steps_taken++;
        } else {
             break; // Unexpected terminal condition
        }
    }
    
    if (current_pos == goal) {
        cout << "\nSuccess! UGV safely reached (" << goal.x << "," << goal.y << ") despite dynamic changes.\n";
        cout << "Total movement steps executed: " << steps_taken << "\n";
    }
    
    return 0;
}
