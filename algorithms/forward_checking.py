import copy
from csp.formulation import SudokuCSP
from performance.tracker import PerformanceTracker

class ForwardCheckingSolver:
    def __init__(self):
        self.tracker = PerformanceTracker()
        self.steps = []

    def solve(self, board):
        self.steps = []
        self.tracker.start()
        csp = SudokuCSP(board)
        domains = copy.deepcopy(csp.domains)

        assignment = {}
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    assignment[(r, c)] = board[r][c]

        result = self._forward_check(csp, assignment, domains)
        self.tracker.stop()

        if result:
            solution = [[0]*9 for _ in range(9)]
            for (r, c), v in result.items():
                solution[r][c] = v
            return solution
        return None

    def _forward_check(self, csp, assignment, domains):
        if csp.is_complete(assignment):
            return assignment

        unassigned = csp.get_unassigned_variables(assignment)
        var = min(unassigned, key=lambda v: len(domains[v]))
        self.tracker.add_state()

        for value in list(domains[var]):
            if csp.is_consistent(var, value, assignment):
                assignment[var] = value
                self.steps.append((var[0], var[1], value))

            # Pruning — track karo kya hataya
                pruned = {}
                failure = False
                for peer in csp.get_peers(var):
                    if peer not in assignment:
                        if value in domains[peer]:
                            domains[peer].remove(value)
                            pruned[peer] = value
                            if len(domains[peer]) == 0:
                                failure = True
                                break

                if not failure:
                    result = self._forward_check(
                        csp, assignment, domains)
                    if result:
                        return result

            # Undo assignment
                del assignment[var]
                self.steps.append((var[0], var[1], 0))
                self.tracker.add_backtrack()

            # Domain restore — deepcopy nahi, sirf wapas daalo
                for peer, val in pruned.items():
                    domains[peer].append(val)

        return None

    def get_tracker(self):
        return self.tracker

    def get_steps(self):
        return self.steps