# import copy
# from csp.formulation import SudokuCSP
# from performance.tracker import PerformanceTracker

# class ForwardCheckingSolver:
#     def __init__(self):
#         self.tracker = PerformanceTracker()
#         self.steps = []

#     def solve(self, board):
#         self.steps = []
#         self.tracker.start()
#         csp = SudokuCSP(board)
#         domains = copy.deepcopy(csp.domains)

#         assignment = {}
#         for r in range(9):
#             for c in range(9):
#                 if board[r][c] != 0:
#                     assignment[(r, c)] = board[r][c]

#         result = self._forward_check(csp, assignment, domains)
#         self.tracker.stop()

#         if result:
#             solution = [[0]*9 for _ in range(9)]
#             for (r, c), v in result.items():
#                 solution[r][c] = v
#             return solution
#         return None

#     def _forward_check(self, csp, assignment, domains):
#         if csp.is_complete(assignment):
#             return assignment

#         unassigned = csp.get_unassigned_variables(assignment)
#         var = min(unassigned, key=lambda v: len(domains[v]))
#         self.tracker.add_state()

#         for value in list(domains[var]):
#             if csp.is_consistent(var, value, assignment):
#                 assignment[var] = value
#                 self.steps.append((var[0], var[1], value))

#             # Pruning — track karo kya hataya
#                 pruned = {}
#                 failure = False
#                 for peer in csp.get_peers(var):
#                     if peer not in assignment:
#                         if value in domains[peer]:
#                             domains[peer].remove(value)
#                             pruned[peer] = value
#                             if len(domains[peer]) == 0:
#                                 failure = True
#                                 break

#                 if not failure:
#                     result = self._forward_check(
#                         csp, assignment, domains)
#                     if result:
#                         return result

#             # Undo assignment
#                 del assignment[var]
#                 self.steps.append((var[0], var[1], 0))
#                 self.tracker.add_backtrack()

#             # Domain restore — deepcopy nahi, sirf wapas daalo
#                 for peer, val in pruned.items():
#                     domains[peer].append(val)

#         return None

#     def get_tracker(self):
#         return self.tracker

#     def get_steps(self):
#         return self.steps


import copy
from csp.formulation import SudokuCSP
from performance.tracker import PerformanceTracker


class ForwardCheckingSolver:
    """
    Constraint Propagation — Forward Checking with MRV.

    After each assignment, immediately prunes the assigned value
    from all unassigned peer domains (one level of propagation).
    Detects dead-ends earlier than pure backtracking but does not
    propagate transitively like AC-3.
    """

    def __init__(self):
        self.tracker = PerformanceTracker()
        self.steps = []

    def solve(self, board):
        self.steps = []
        self.tracker.start()

        # Build domains as sets
        domains = {}
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    domains[(r, c)] = {board[r][c]}
                else:
                    domains[(r, c)] = set(range(1, 10))

        # Build peer graph once — reused at every recursion level
        peers = self._build_peers()

        # Initial pruning — propagate fixed cells immediately
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    val = board[r][c]
                    for peer in peers[(r, c)]:
                        domains[peer].discard(val)

        # Build initial assignment from fixed cells
        assignment = {}
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    assignment[(r, c)] = board[r][c]

        result = self._solve(assignment, domains, peers)
        self.tracker.stop()

        if result:
            solution = [[0] * 9 for _ in range(9)]
            for (r, c), v in result.items():
                solution[r][c] = v
            return solution
        return None

    def _build_peers(self):
        """Pre-compute peer sets for all 81 cells."""
        peers = {}
        for r in range(9):
            for c in range(9):
                p = set()
                # Row peers
                for col in range(9):
                    if col != c:
                        p.add((r, col))
                # Column peers
                for row in range(9):
                    if row != r:
                        p.add((row, c))
                # Box peers
                br, bc = 3 * (r // 3), 3 * (c // 3)
                for row in range(br, br + 3):
                    for col in range(bc, bc + 3):
                        if (row, col) != (r, c):
                            p.add((row, col))
                peers[(r, c)] = p
        return peers

    def _solve(self, assignment, domains, peers):
        # Base case
        if len(assignment) == 81:
            return assignment

        # MRV — most constrained unassigned variable
        unassigned = [
            v for v in domains
            if v not in assignment
        ]
        if not unassigned:
            return None

        var = min(unassigned, key=lambda v: len(domains[v]))
        self.tracker.add_state()

        for value in list(domains[var]):
            # Consistency check against current assignment
            conflict = any(
                assignment.get(peer) == value
                for peer in peers[var]
            )
            if conflict:
                continue

            # Assign
            assignment[var] = value
            self.steps.append((var[0], var[1], value))

            # Forward checking — prune peers, record what changed
            pruned = {}
            failure = False
            for peer in peers[var]:
                if peer not in assignment:
                    if value in domains[peer]:
                        domains[peer].discard(value)
                        pruned[peer] = value
                        if len(domains[peer]) == 0:
                            failure = True
                            break

            if not failure:
                result = self._solve(assignment, domains, peers)
                if result:
                    return result

            # Undo
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