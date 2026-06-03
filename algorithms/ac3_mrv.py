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

        # Build working domains as sets for fast operations
        domains = {}
        for var in csp.variables:
            if board[var[0]][var[1]] != 0:
                domains[var] = {board[var[0]][var[1]]}
            else:
                domains[var] = set(range(1, 10))

        # Phase 1 — AC-3 preprocessing
        if not self._ac3(csp, domains):
            self.tracker.stop()
            return None

        # Build initial assignment from fixed cells + any
        # domains reduced to singleton by AC-3
        assignment = {}
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    assignment[(r, c)] = board[r][c]

        # Also assign cells whose domain AC-3 reduced to size 1
        changed = True
        while changed:
            changed = False
            for var in csp.variables:
                if var not in assignment and len(domains[var]) == 1:
                    val = next(iter(domains[var]))
                    assignment[var] = val
                    self.steps.append((var[0], var[1], val))
                    changed = True

        # Phase 2 — MRV backtracking
        result = self._backtrack_mrv(csp, assignment, domains)
        self.tracker.stop()

        if result:
            solution = [[0] * 9 for _ in range(9)]
            for (r, c), v in result.items():
                solution[r][c] = v
            return solution
        return None

    # ── AC-3 ──────────────────────────────────────────────────────────────
    def _ac3(self, csp, domains):
        queue = deque()
        for var in csp.variables:
            for peer in csp.get_peers(var):
                queue.append((var, peer))

        while queue:
            xi, xj = queue.popleft()
            if self._revise(domains, xi, xj):
                if len(domains[xi]) == 0:
                    return False
                # Propagate — re-check all neighbours of xi
                for xk in csp.get_peers(xi):
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def _revise(self, domains, xi, xj):
   
        revised = False
        for val in list(domains[xi]):
            # Support exists if xj has at least one value != val
            has_support = any(w != val for w in domains[xj])
            if not has_support:
                domains[xi].discard(val)
                revised = True
        return revised

    # ── MRV Backtracking ──────────────────────────────────────────────────
    def _backtrack_mrv(self, csp, assignment, domains):
        if csp.is_complete(assignment):
            return assignment

        # MRV — pick variable with fewest remaining values
        unassigned = [v for v in csp.variables if v not in assignment]
        if not unassigned:
            return None

        var = min(unassigned, key=lambda v: len(domains[v]))
        self.tracker.add_state()

        for value in list(domains[var]):
            if csp.is_consistent(var, value, assignment):
                assignment[var] = value
                self.steps.append((var[0], var[1], value))

                # Forward checking — prune peers, track what was removed
                pruned = {}
                failure = False
                for peer in csp.get_peers(var):
                    if peer not in assignment:
                        if value in domains[peer]:
                            domains[peer].discard(value)
                            pruned[peer] = value
                            if len(domains[peer]) == 0:
                                failure = True
                                break

                if not failure:
                    result = self._backtrack_mrv(csp, assignment, domains)
                    if result:
                        return result

                # Undo assignment
                del assignment[var]
                self.steps.append((var[0], var[1], 0))
                self.tracker.add_backtrack()

                # Restore pruned domains
                for peer, val in pruned.items():
                    domains[peer].add(val)

        return None

    def get_tracker(self):
        return self.tracker

    def get_steps(self):
        return self.steps