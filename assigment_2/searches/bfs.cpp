#include <iostream>
#include <queue>
#include <vector>
using namespace std;

void bfs(int s, vector<vector<int>> &adj) {
  vector<bool> v(adj.size(), false);
  queue<int> q;
  v[s] = true;
  q.push(s);
  while (!q.empty()) {
    int c = q.front();
    q.pop();
    cout << c << " ";
    for (int n : adj[c]) {
      if (!v[n]) {
        v[n] = true;
        q.push(n);
      }
    }
  }
}

int main() {
  int n, e;
  cout << "Enter the number of vertices and edges: ";
  cin >> n >> e;
  vector<vector<int>> adj(n);
  cout << "Enter the edges: ";
  for (int i = 0; i < e; i++) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }
  bfs(0, adj);
  return 0;
}
