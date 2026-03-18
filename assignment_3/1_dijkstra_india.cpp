#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <queue>
#include <limits>
#include <algorithm>

using namespace std;

typedef pair<double, string> pds;

class Graph {
public:
    unordered_map<string, unordered_map<string, double>> adjList;

    void addEdge(string u, string v, double weight) {
        adjList[u][v] = weight;
        adjList[v][u] = weight; // Bidirectional
    }

    void dijkstra(string start, string goal = "") {
        unordered_map<string, double> distances;
        unordered_map<string, string> came_from;
        priority_queue<pds, vector<pds>, greater<pds>> pq;

        for (const auto& pair : adjList) {
            distances[pair.first] = numeric_limits<double>::infinity();
        }

        distances[start] = 0;
        pq.push({0, start});

        while (!pq.empty()) {
            double current_dist = pq.top().first;
            string current_node = pq.top().second;
            pq.pop();

            if (goal != "" && current_node == goal) {
                break;
            }

            if (current_dist > distances[current_node]) {
                continue;
            }

            for (const auto& neighbor : adjList[current_node]) {
                string next_node = neighbor.first;
                double weight = neighbor.second;
                double new_dist = current_dist + weight;

                if (distances.find(next_node) == distances.end() || new_dist < distances[next_node]) {
                    distances[next_node] = new_dist;
                    came_from[next_node] = current_node;
                    pq.push({new_dist, next_node});
                }
            }
        }

        if (goal != "") {
            cout << "Shortest Path from " << start << " to " << goal << ":\n";
            if (distances.find(goal) == distances.end() || distances[goal] == numeric_limits<double>::infinity()) {
                cout << "No path found.\n";
                return;
            }
            vector<string> path;
            string curr = goal;
            while (curr != start) {
                path.push_back(curr);
                curr = came_from[curr];
            }
            path.push_back(start);
            reverse(path.begin(), path.end());
            
            for (size_t i = 0; i < path.size(); ++i) {
                cout << path[i] << (i == path.size() - 1 ? "" : " -> ");
            }
            cout << "\nTotal Distance: " << distances[goal] << " km\n";
        } else {
            cout << "\nDistances from " << start << " to all other connected cities:\n";
            vector<pair<double, string>> sorted_dists;
            for (auto const& [key, val] : distances) {
                if (val != numeric_limits<double>::infinity()) {
                    sorted_dists.push_back({val, key});
                }
            }
            sort(sorted_dists.begin(), sorted_dists.end());
            for (auto const& p : sorted_dists) {
                cout << " - " << p.second << " : " << p.first << " km\n";
            }
        }
    }
};

int main() {
    Graph g;
    g.addEdge("Delhi", "Jaipur", 280);
    g.addEdge("Delhi", "Agra", 240);
    g.addEdge("Delhi", "Chandigarh", 250);
    g.addEdge("Jaipur", "Ahmedabad", 660);
    g.addEdge("Jaipur", "Indore", 600);
    g.addEdge("Agra", "Kanpur", 280);
    g.addEdge("Agra", "Gwalior", 120);
    g.addEdge("Chandigarh", "Amritsar", 230);
    g.addEdge("Chandigarh", "Shimla", 110);
    g.addEdge("Ahmedabad", "Mumbai", 520);
    g.addEdge("Ahmedabad", "Surat", 260);
    g.addEdge("Indore", "Bhopal", 190);
    g.addEdge("Indore", "Nagpur", 480);
    g.addEdge("Kanpur", "Lucknow", 90);
    g.addEdge("Kanpur", "Varanasi", 330);
    g.addEdge("Gwalior", "Bhopal", 430);
    g.addEdge("Amritsar", "Jammu", 210);
    g.addEdge("Mumbai", "Pune", 150);
    g.addEdge("Mumbai", "Goa", 590);
    g.addEdge("Surat", "Mumbai", 280);
    g.addEdge("Pune", "Bangalore", 840);
    g.addEdge("Pune", "Hyderabad", 560);
    g.addEdge("Nagpur", "Hyderabad", 500);
    g.addEdge("Bhopal", "Nagpur", 350);
    g.addEdge("Varanasi", "Patna", 250);
    g.addEdge("Patna", "Kolkata", 580);
    g.addEdge("Kolkata", "Bhubaneswar", 440);
    g.addEdge("Bhubaneswar", "Visakhapatnam", 440);
    g.addEdge("Visakhapatnam", "Vijayawada", 350);
    g.addEdge("Vijayawada", "Chennai", 450);
    g.addEdge("Vijayawada", "Hyderabad", 270);
    g.addEdge("Hyderabad", "Bangalore", 570);
    g.addEdge("Bangalore", "Chennai", 350);
    g.addEdge("Bangalore", "Kochi", 550);
    g.addEdge("Chennai", "Madurai", 460);
    g.addEdge("Madurai", "Kochi", 270);
    g.addEdge("Madurai", "Kanyakumari", 240);
    g.addEdge("Kochi", "Thiruvananthapuram", 200);
    g.addEdge("Thiruvananthapuram", "Kanyakumari", 90);
    g.addEdge("Jammu", "Srinagar", 260);
    g.addEdge("Goa", "Mangalore", 360);
    g.addEdge("Mangalore", "Bangalore", 350);

    string start_city = "Delhi";
    string target_city = "Bangalore";

    cout << "--- Dijkstra's Algorithm (Uniform-Cost Search) ---\n";
    g.dijkstra(start_city, target_city);
    g.dijkstra(start_city);

    return 0;
}
