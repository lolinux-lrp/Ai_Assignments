#include <iostream>
#include <set>
#include <vector>

using namespace std;

const int TOTAL_M = 3;
const int TOTAL_C = 3;

struct State {
  int m, c, b;
  bool operator<(const State &other) const {
    if (m != other.m)
      return m < other.m;
    if (c != other.c)
      return c < other.c;
    return b < other.b;
  }
  bool operator==(const State &other) const {
    return m == other.m && c == other.c && b == other.b;
  }
};

bool isValid(int m, int c) {
  if (m < 0 || m > TOTAL_M || c < 0 || c > TOTAL_C)
    return false;
  if (m > 0 && m < c)
    return false;
  if (TOTAL_M - m > 0 && TOTAL_M - m < TOTAL_C - c)
    return false;
  return true;
}

vector<pair<int, int>> moves = {{1, 0}, {2, 0}, {0, 1}, {0, 2}, {1, 1}};
set<State> visited;
vector<State> path;

bool dfs(State curr, State goal) {
  path.push_back(curr);
  visited.insert(curr);

  if (curr == goal)
    return true;

  for (auto move : moves) {
    int dm = move.first;
    int dc = move.second;
    State next_state;

    if (curr.b == 1) {
      next_state = {curr.m - dm, curr.c - dc, 0};
    } else {
      next_state = {curr.m + dm, curr.c + dc, 1};
    }

    if (isValid(next_state.m, next_state.c) &&
        visited.find(next_state) == visited.end()) {
      if (dfs(next_state, goal))
        return true;
    }
  }

  path.pop_back();
  // Do not remove from visited to prevent re-evaluating dead-end paths
  return false;
}

int main() {

  State start = {TOTAL_M, TOTAL_C, 1};
  State goal = {0, 0, 0};

  if (dfs(start, goal)) {
    for (size_t i = 0; i < path.size(); ++i) {
      cout << path[i].m << " " << path[i].c << " " << path[i].b << "\n";
    }
  } else {
    cout << "No solution found\n";
  }

  return 0;
}
