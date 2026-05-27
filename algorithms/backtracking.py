import copy
from csp.formulation import SudokuCSP
from performance.tracker import PerformanceTracker

class BacktrackingSolver:
    def __init__(self):
        self.tracker = PerformanceTracker()
        self.steps = []  # For animation: list of (r, c, value)

    def solve(self, board):
        self.steps = []
        self.tracker.start()
        csp = SudokuCSP(board)
        assignment = {}

        # Add pre-filled cells to assignment
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    assignment[(r, c)] = board[r][c]

        result = self._backtrack(csp, assignment)
        self.tracker.stop()

        if result:
            solution = [[0]*9 for _ in range(9)]
            for (r, c), v in result.items():
                solution[r][c] = v
            return solution
        return None

    def _backtrack(self, csp, assignment):
        if csp.is_complete(assignment):
            return assignment

        # Pick next unassigned variable (simple order)
        unassigned = csp.get_unassigned_variables(assignment)
        var = unassigned[0]
        self.tracker.add_state()

        for value in csp.domains[var]:
            if csp.is_consistent(var, value, assignment):
                assignment[var] = value
                self.steps.append((var[0], var[1], value))

                result = self._backtrack(csp, assignment)
                if result:
                    return result

                # Backtrack
                del assignment[var]
                self.steps.append((var[0], var[1], 0))  # 0 = undo
                self.tracker.add_backtrack()

        return None

    def get_tracker(self):
        return self.tracker

    def get_steps(self):
        return self.steps