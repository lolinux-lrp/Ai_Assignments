from csp import CSP, Constraint
from typing import Dict, List, Tuple

class SudokuConstraint(Constraint[Tuple[int, int], int]):
    def __init__(self, variables: List[Tuple[int, int]]) -> None:
        super().__init__(variables)

    def satisfied(self, assignment: Dict[Tuple[int, int], int]) -> bool:
        values = [assignment[var] for var in self.variables if var in assignment]
        return len(values) == len(set(values))

if __name__ == "__main__":
    variables: List[Tuple[int, int]] = [(r, c) for r in range(9) for c in range(9)]
    domains: Dict[Tuple[int, int], List[int]] = {}
    
    # 0 represents an empty cell
    initial_board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    for r in range(9):
        for c in range(9):
            if initial_board[r][c] == 0:
                domains[(r, c)] = list(range(1, 10))
            else:
                domains[(r, c)] = [initial_board[r][c]]

    # Sorting variables so that those with domains of length 1 (pre-filled cells) are assigned first.
    # This massively speeds up the backtracking algorithm for Sudoku.
    variables.sort(key=lambda var: len(domains[var]))

    csp: CSP[Tuple[int, int], int] = CSP(variables, domains)
    
    # Row constraints
    for r in range(9):
        csp.add_constraint(SudokuConstraint([(r, c) for c in range(9)]))
    
    # Column constraints
    for c in range(9):
        csp.add_constraint(SudokuConstraint([(r, c) for r in range(9)]))
    
    # 3x3 Block constraints
    for r_block in range(3):
        for c_block in range(3):
            vars_in_block = []
            for r in range(r_block * 3, r_block * 3 + 3):
                for c in range(c_block * 3, c_block * 3 + 3):
                    vars_in_block.append((r, c))
            csp.add_constraint(SudokuConstraint(vars_in_block))

    solution: Dict[Tuple[int, int], int] = csp.backtracking_search()
    
    if solution is None:
        print("No solution found.")
    else:
        print("Sudoku Solution:")
        for r in range(9):
            row = []
            for c in range(9):
                row.append(str(solution[(r, c)]))
            print(" ".join(row))
