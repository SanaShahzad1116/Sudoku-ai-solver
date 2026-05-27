import copy
from collections import deque
from csp.formulation import SudokuCSP
from performance.tracker import PerformanceTracker

class AC3MRVSolver:
    def __init__(self):
        self.tracker = PerformanceTracker()
        self.steps = []

    def solve(self, board):
        self.steps = []
        self.tracker.start()
        csp = SudokuCSP(board)
        domains = copy.deepcopy(csp.domains)

        # Run AC3 first
        if not self._ac3(csp, domains):
            self.tracker.stop()
            return None

        assignment = {}
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    assignment[(r, c)] = board[r][c]

        result = self._backtrack_mrv(csp, assignment, domains)
        self.tracker.stop()

        if result:
            solution = [[0]*9 for _ in range(9)]
            for (r, c), v in result.items():
                solution[r][c] = v
            return solution
        return None

    def _ac3(self, csp, domains):
        queue = deque()
        for var in csp.variables:
            for peer in csp.get_peers(var):
                queue.append((var, peer))

        while queue:
            (xi, xj) = queue.popleft()
            if self._revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False
                for xk in csp.get_peers(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def _revise(self, domains, xi, xj):
        revised = False
        for val in domains[xi][:]:
            if all(val == v for v in domains[xj]):
                domains[xi].remove(val)
                revised = True
        return revised

    def _backtrack_mrv(self, csp, assignment, domains):
        if csp.is_complete(assignment):
            return assignment

        var = self._select_mrv(csp, assignment, domains)
        self.tracker.add_state()

        for value in self._order_values(var, domains):
            if csp.is_consistent(var, value, assignment):
                assignment[var] = value
                self.steps.append((var[0], var[1], value))

                new_domains = copy.deepcopy(domains)
                new_domains[var] = [value]

                result = self._backtrack_mrv(csp, assignment, new_domains)
                if result:
                    return result

                del assignment[var]
                self.steps.append((var[0], var[1], 0))
                self.tracker.add_backtrack()

        return None

    def _select_mrv(self, csp, assignment, domains):
        # Minimum Remaining Values heuristic
        unassigned = csp.get_unassigned_variables(assignment)
        return min(unassigned, key=lambda v: len(domains[v]))

    def _order_values(self, var, domains):
        return domains[var]

    def get_tracker(self):
        return self.tracker

    def get_steps(self):
        return self.steps