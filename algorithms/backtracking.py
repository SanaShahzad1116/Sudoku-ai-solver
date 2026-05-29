# import copy
# from csp.formulation import SudokuCSP
# from performance.tracker import PerformanceTracker

# class BacktrackingSolver:
#     def __init__(self):
#         self.tracker = PerformanceTracker()
#         self.steps = []  # For animation: list of (r, c, value)

#     def solve(self, board):
#         self.steps = []
#         self.tracker.start()
#         csp = SudokuCSP(board)
#         assignment = {}

#         # Add pre-filled cells to assignment
#         for r in range(9):
#             for c in range(9):
#                 if board[r][c] != 0:
#                     assignment[(r, c)] = board[r][c]

#         result = self._backtrack(csp, assignment)
#         self.tracker.stop()

#         if result:
#             solution = [[0]*9 for _ in range(9)]
#             for (r, c), v in result.items():
#                 solution[r][c] = v
#             return solution
#         return None

#     def _backtrack(self, csp, assignment):
#         if csp.is_complete(assignment):
#             return assignment

#         # Pick next unassigned variable (simple order)
#         unassigned = csp.get_unassigned_variables(assignment)
#         var = unassigned[0]
#         self.tracker.add_state()

#         for value in csp.domains[var]:
#             if csp.is_consistent(var, value, assignment):
#                 assignment[var] = value
#                 self.steps.append((var[0], var[1], value))

#                 result = self._backtrack(csp, assignment)
#                 if result:
#                     return result

#                 # Backtrack
#                 del assignment[var]
#                 self.steps.append((var[0], var[1], 0))  # 0 = undo
#                 self.tracker.add_backtrack()

#         return None

#     def get_tracker(self):
#         return self.tracker

#     def get_steps(self):
#         return self.steps


import copy
from csp.formulation import SudokuCSP
from performance.tracker import PerformanceTracker


class BacktrackingSolver:
    """
    Uninformed Search — pure depth-first backtracking.
    No heuristics, no look-ahead.
    Baseline for comparison against informed strategies.
    """

    def __init__(self):
        self.tracker = PerformanceTracker()
        self.steps = []

    def solve(self, board):
        self.steps = []
        self.tracker.start()

        csp = SudokuCSP(board)
        assignment = {}

        # Pre-fill fixed cells
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    assignment[(r, c)] = board[r][c]

        result = self._backtrack(csp, assignment)
        self.tracker.stop()

        if result:
            solution = [[0] * 9 for _ in range(9)]
            for (r, c), v in result.items():
                solution[r][c] = v
            return solution
        return None

    def _backtrack(self, csp, assignment):
        # Base case — all 81 cells assigned
        if csp.is_complete(assignment):
            return assignment

        # Select next variable — simple left-to-right order (uninformed)
        unassigned = csp.get_unassigned_variables(assignment)
        var = unassigned[0]

        # Count this variable selection as one state explored
        self.tracker.add_state()

        # Try each value in domain
        for value in csp.domains[var]:
            if csp.is_consistent(var, value, assignment):
                # Assign
                assignment[var] = value
                self.steps.append((var[0], var[1], value))

                # Recurse
                result = self._backtrack(csp, assignment)
                if result:
                    return result

                # Undo — backtrack
                del assignment[var]
                self.steps.append((var[0], var[1], 0))
                self.tracker.add_backtrack()

        # No value worked — signal failure
        return None

    def get_tracker(self):
        return self.tracker

    def get_steps(self):
        return self.steps