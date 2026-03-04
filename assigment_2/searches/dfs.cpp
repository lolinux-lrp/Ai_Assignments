#include <iostream>
#include <vector>
using namespace std;

void dfs(int s, vector<vector<int>> &adj, vector<bool> &vis) {
  vis[s] = true;
  cout << s << " ";
  for (int n : adj[s]) {
    if (!vis[n]) {
      dfs(n, adj, vis);
    }
  }
}

int main() {
  int n, e;
  cout << "Enter the number of vertices and edges: ";
  cin >> n >> e;
  vector<vector<int>> adj(n);
  vector<bool> vis(n, false);
  cout << "Enter the edges: ";
  for (int i = 0; i < e; i++) {
    int u, v;
    cin >> u >> v;
    adj[u].push_back(v);
    adj[v].push_back(u);
  }
  dfs(0, adj, vis);
  return 0;
}
