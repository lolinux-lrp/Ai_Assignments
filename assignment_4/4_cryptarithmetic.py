from csp import CSP, Constraint
from typing import Dict, List

class CryptarithmeticConstraint(Constraint[str, int]):
    def __init__(self, letters: List[str]) -> None:
        super().__init__(letters)
        self.letters = letters

    def satisfied(self, assignment: Dict[str, int]) -> bool:
        assigned_letters = [var for var in self.letters if var in assignment and len(var) == 1]
        values = [assignment[var] for var in assigned_letters]
        if len(values) != len(set(values)):
            return False

        if len(assignment) == len(self.letters):
            t = assignment['T']
            w = assignment['W']
            o = assignment['O']
            f = assignment['F']
            u = assignment['U']
            r = assignment['R']
            
            x1 = assignment['X1']
            x2 = assignment['X2']
            x3 = assignment['X3']
            
            if t == 0 or f == 0:
                return False

            if o + o != r + 10 * x1: return False
            if w + w + x1 != u + 10 * x2: return False
            if t + t + x2 != o + 10 * x3: return False
            if x3 != f: return False
            return True
            
        return True

if __name__ == "__main__":
    letters: List[str] = ['T', 'W', 'O', 'F', 'U', 'R']
    carries = ['X1', 'X2', 'X3']
    variables: List[str] = letters + carries
    
    domains: Dict[str, List[int]] = {}
    for letter in letters:
        domains[letter] = list(range(10)) 
    
    for carry in carries:
        domains[carry] = [0, 1]

    csp: CSP[str, int] = CSP(variables, domains)
    csp.add_constraint(CryptarithmeticConstraint(variables))

    solution: Dict[str, int] = csp.backtracking_search()
    
    if solution is None:
        print("No solution found.")
    else:
        print("Cryptarithmetic Solution for TWO + TWO = FOUR:")
        for letter in letters:
            print(f"{letter} = {solution[letter]}")
        print("\nEquation Check:")
        t_w_o = str(solution['T']) + str(solution['W']) + str(solution['O'])
        f_o_u_r = str(solution['F']) + str(solution['O']) + str(solution['U']) + str(solution['R'])
        print(f"  {t_w_o}")
        print(f"+ {t_w_o}")
        print("------")
        print(f" {f_o_u_r}")
