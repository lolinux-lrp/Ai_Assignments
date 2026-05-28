import math
import random

class TicTacToe:
    """
    Tic-Tac-Toe Environment.
    State is a tuple of 9 elements: 1 for 'X', -1 for 'O', 0 for empty.
    'X' is the maximizing player, 'O' is the minimizing player.
    """
    def __init__(self, state=None, turn=1):
        if state is None:
            self.state = (0,) * 9
        else:
            self.state = state
        self.turn = turn

    def get_legal_moves(self):
        return [i for i, v in enumerate(self.state) if v == 0]

    def make_move(self, move):
        new_state = list(self.state)
        new_state[move] = self.turn
        return TicTacToe(tuple(new_state), -self.turn)

    def check_winner(self):
        """Returns 1 if 'X' wins, -1 if 'O' wins, 0 for draw, None if game is ongoing."""
        winning_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # cols
            (0, 4, 8), (2, 4, 6)             # diagonals
        ]
        for a, b, c in winning_lines:
            if self.state[a] != 0 and self.state[a] == self.state[b] == self.state[c]:
                return self.state[a]
        if 0 not in self.state:
            return 0 # Draw
        return None # Ongoing

    def evaluate(self):
        """Heuristic evaluation for non-terminal states."""
        winner = self.check_winner()
        if winner is not None:
            return winner * 1000 # Terminal state value
            
        score = 0
        winning_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        
        for a, b, c in winning_lines:
            line = [self.state[a], self.state[b], self.state[c]]
            x_count = line.count(1)
            o_count = line.count(-1)
            if x_count > 0 and o_count == 0:
                score += 10**x_count
            elif o_count > 0 and x_count == 0:
                score -= 10**o_count
                
        return score

    def display(self):
        symbols = {1: 'X', -1: 'O', 0: ' '}
        for i in range(3):
            print(f" {symbols[self.state[i*3]]} | {symbols[self.state[i*3+1]]} | {symbols[self.state[i*3+2]]} ")
            if i < 2:
                print("---+---+---")
        print()


def minimax(env, depth):
    """
    Minimax search algorithm.
    Returns the optimal value and best move for the current player.
    """
    winner = env.check_winner()
    if winner is not None or depth == 0:
        return winner, None

    maximizing = env.turn == 1
    best_move = None
    
    if maximizing:
        max_eval = -math.inf
        for move in env.get_legal_moves():
            new_env = env.make_move(move)
            eval_val, _ = minimax(new_env, depth - 1)
            # If no legal moves returned from deep search, eval_val might be None?
            # Wait, depth = 0 returns (eval, None). So eval_val is scalar.
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = move
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in env.get_legal_moves():
            new_env = env.make_move(move)
            eval_val, _ = minimax(new_env, depth - 1)
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = move
        return min_eval, best_move


def alpha_beta_search(env, depth, alpha=-math.inf, beta=math.inf):
    """
    Alpha-Beta search algorithm.
    Returns optimal value and best move using alpha-beta pruning.
    """
    winner = env.check_winner()
    if winner is not None or depth == 0:
        return winner, None

    maximizing = env.turn == 1
    best_move = None

    if maximizing:
        max_eval = -math.inf
        for move in env.get_legal_moves():
            new_env = env.make_move(move)
            eval_val, _ = alpha_beta_search(new_env, depth - 1, alpha, beta)
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = move
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break # Beta cut-off
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in env.get_legal_moves():
            new_env = env.make_move(move)
            eval_val, _ = alpha_beta_search(new_env, depth - 1, alpha, beta)
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = move
            beta = min(beta, eval_val)
            if beta <= alpha:
                break # Alpha cut-off
        return min_eval, best_move


def heuristic_alpha_beta(env, depth, alpha=-math.inf, beta=math.inf):
    """
    Heuristic Alpha-Beta search algorithm.
    Uses an evaluation function for non-terminal states when depth limit is reached.
    """
    if depth == 0 or env.check_winner() is not None:
        return env.evaluate(), None

    maximizing = env.turn == 1
    best_move = None

    if maximizing:
        max_eval = -math.inf
        for move in env.get_legal_moves():
            new_env = env.make_move(move)
            eval_val, _ = heuristic_alpha_beta(new_env, depth - 1, alpha, beta)
            if eval_val > max_eval:
                max_eval = eval_val
                best_move = move
            alpha = max(alpha, eval_val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in env.get_legal_moves():
            new_env = env.make_move(move)
            eval_val, _ = heuristic_alpha_beta(new_env, depth - 1, alpha, beta)
            if eval_val < min_eval:
                min_eval = eval_val
                best_move = move
            beta = min(beta, eval_val)
            if beta <= alpha:
                break
        return min_eval, best_move


class MCTSNode:
    """Node for Monte-Carlo Tree Search."""
    def __init__(self, env, parent=None, move=None):
        self.env = env
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0.0
        self.visits = 0
        self.untried_moves = env.get_legal_moves()

    def ucb1(self, c=1.414):
        if self.visits == 0:
            return math.inf
        exploitation = self.wins / self.visits
        exploration = c * math.sqrt(math.log(self.parent.visits) / self.visits)
        return exploitation + exploration

def mcts(root_env, iterations=1000):
    """
    Monte-Carlo Tree Search algorithm.
    Returns the best move found after the given number of iterations.
    """
    root = MCTSNode(root_env)
    
    for _ in range(iterations):
        node = root
        
        # 1. Selection
        while node.untried_moves == [] and node.children != []:
            node = max(node.children, key=lambda c: c.ucb1())
            
        # 2. Expansion
        if node.untried_moves != []:
            move = random.choice(node.untried_moves)
            node.untried_moves.remove(move)
            new_env = node.env.make_move(move)
            child = MCTSNode(new_env, parent=node, move=move)
            node.children.append(child)
            node = child
            
        # 3. Simulation
        sim_env = node.env
        while sim_env.check_winner() is None:
            sim_move = random.choice(sim_env.get_legal_moves())
            sim_env = sim_env.make_move(sim_move)
            
        winner = sim_env.check_winner()
        
        # 4. Backpropagation
        while node is not None:
            node.visits += 1
            if node.parent is not None:
                # If the parent made the move that led to this node,
                # the parent's turn is -node.env.turn.
                # A win for the parent means winner == -node.env.turn.
                if winner == -node.env.turn:
                    node.wins += 1
                elif winner == 0:
                    node.wins += 0.5 # Draw
            node = node.parent
            
    if not root.children:
        return None
    best_child = max(root.children, key=lambda c: c.visits)
    return best_child.move

def test_algorithms():
    print("=== Testing Search Algorithms ===")
    
    # State where X can win in one move:
    # X | X |  
    # O | O |  
    #   |   |  
    state = (
        1, 1, 0,
       -1,-1, 0,
        0, 0, 0
    )
    env = TicTacToe(state=state, turn=1)
    print("Initial State (X to move):")
    env.display()
    
    val, move = minimax(env, depth=9)
    print(f"Minimax optimal move: {move} (expected 2)")
    
    val, move = alpha_beta_search(env, depth=9)
    print(f"Alpha-Beta optimal move: {move} (expected 2)")
    
    val, move = heuristic_alpha_beta(env, depth=2)
    print(f"Heuristic Alpha-Beta optimal move: {move} (expected 2)")
    
    move = mcts(env, iterations=1000)
    print(f"MCTS best move: {move} (expected 2)")
    
    print("\nState where X must block O:")
    # X |   |  
    # O | O |  
    # X |   |  
    state = (
        1, 0, 0,
       -1,-1, 0,
        1, 0, 0
    )
    env = TicTacToe(state=state, turn=1)
    env.display()
    
    val, move = minimax(env, depth=9)
    print(f"Minimax blocking move: {move} (expected 5)")

if __name__ == "__main__":
    test_algorithms()
