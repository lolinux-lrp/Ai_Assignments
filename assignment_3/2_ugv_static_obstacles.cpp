#include <iostream>
#include <vector>
#include <cmath>
#include <queue>
#include <map>
#include <random>
#include <chrono>

using namespace std;

struct Node {
    int x, y;
    bool operator==(const Node& other) const {
        return x == other.x && y == other.y;
    }
    bool operator<(const Node& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
};

class UGVEnvironment {
public:
    int width, height;
    vector<vector<int>> grid;

    UGVEnvironment(int w, int h, const string& density_level) : width(w), height(h) {
        grid.resize(height, vector<int>(width, 0));
        double density = 0.10;
        if (density_level == "medium") density = 0.25;
        else if (density_level == "high") density = 0.40;

        unsigned seed = chrono::system_clock::now().time_since_epoch().count();
        default_random_engine generator(seed);
        uniform_real_distribution<double> distribution(0.0, 1.0);

        for (int y = 0; y < height; ++y) {
            for (int x = 0; x < width; ++x) {
                if (distribution(generator) < density) {
                    grid[y][x] = 1; // 1 represents obstacle
                }
            }
        }
    }

    vector<pair<Node, double>> getNeighbors(Node n) {
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
};

double heuristic(Node a, Node b) {
    int dx = abs(a.x - b.x);
    int dy = abs(a.y - b.y);
    return (dx + dy) + (1.414 - 2) * min(dx, dy);
}

void aStarSearch(UGVEnvironment& env, Node start, Node goal) {
    auto start_time = chrono::high_resolution_clock::now();
    
    // Priority queue stores {f_score, node}
    priority_queue<pair<double, Node>, vector<pair<double, Node>>, greater<pair<double, Node>>> pq;
    map<Node, double> g_score;
    map<Node, Node> came_from;
    
    pq.push({0 + heuristic(start, goal), start});
    g_score[start] = 0;
    
    int nodes_expanded = 0;
    bool found = false;
    
    while (!pq.empty()) {
        Node current = pq.top().second;
        pq.pop();
        nodes_expanded++;
        
        if (current == goal) {
            found = true;
            break;
        }
        
        for (auto& edge : env.getNeighbors(current)) {
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
    
    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> execution_time = end_time - start_time;
    
    if (found) {
        cout << "Path found!\n";
        cout << "Measures of Effectiveness (MOE):\n";
        cout << "  1. Path Length (Distance) : " << g_score[goal] << " Units (Kms)\n";
        cout << "  2. Nodes Expanded         : " << nodes_expanded << "\n";
        cout << "  3. Execution Time         : " << execution_time.count() << " seconds\n";
    } else {
        cout << "No path found! The environment is too dense.\n";
        cout << "  Nodes Expanded: " << nodes_expanded << "\n";
        cout << "  Execution Time: " << execution_time.count() << " seconds\n";
    }
}

int main() {
    Node start_node = {0, 0};
    Node goal_node = {69, 69};
    
    vector<string> levels = {"low", "medium", "high"};
    cout << "--- UGV Static Obstacle Navigation: 70x70 Grid (8-way movement) ---\n";
    
    for (const string& level : levels) {
        cout << "\n---> Testing Map with " << level << " Obstacle Density:\n";
        UGVEnvironment env(70, 70, level);
        
        // Ensure start and goal are passable
        env.grid[start_node.y][start_node.x] = 0;
        env.grid[goal_node.y][goal_node.x] = 0;
        
        aStarSearch(env, start_node, goal_node);
    }
    
    return 0;
}
