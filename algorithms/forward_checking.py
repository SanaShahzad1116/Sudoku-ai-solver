# import copy
# from csp.formulation import SudokuCSP
# from performance.tracker import PerformanceTracker

# class ForwardCheckingSolver:
#     def __init__(self):
#         self.tracker = PerformanceTracker()
#         self.steps   = []

#     def solve(self, board):
#         self.steps = []
#         self.tracker.start()

#         # Simple domain — sirf board se
#         domains = {}
#         for r in range(9):
#             for c in range(9):
#                 if board[r][c] != 0:
#                     domains[(r, c)] = {board[r][c]}
#                 else:
#                     domains[(r, c)] = set(range(1, 10))

#         # Peers compute karo
#         peers = {}
#         for r in range(9):
#             for c in range(9):
#                 p = set()
#                 for col in range(9):
#                     if col != c:
#                         p.add((r, col))
#                 for row in range(9):
#                     if row != r:
#                         p.add((row, c))
#                 br, bc = 3*(r//3), 3*(c//3)
#                 for row in range(br, br+3):
#                     for col in range(bc, bc+3):
#                         if (row, col) != (r, c):
#                             p.add((row, col))
#                 peers[(r, c)] = p

#         # Initial forward check — fixed cells propagate karo
#         for r in range(9):
#             for c in range(9):
#                 if board[r][c] != 0:
#                     val = board[r][c]
#                     for peer in peers[(r, c)]:
#                         domains[peer].discard(val)

#         assignment = {}
#         for r in range(9):
#             for c in range(9):
#                 if board[r][c] != 0:
#                     assignment[(r, c)] = board[r][c]

#         result = self._solve(assignment, domains, peers, board)
#         self.tracker.stop()

#         if result:
#             solution = [[0]*9 for _ in range(9)]
#             for (r, c), v in result.items():
#                 solution[r][c] = v
#             return solution
#         return None

#     def _solve(self, assignment, domains, peers, fixed):
#         if len(assignment) == 81:
#             return assignment

#         # MRV — sabse kam options wala cell
#         unassigned = [
#             v for v in domains
#             if v not in assignment
#         ]
#         if not unassigned:
#             return None

#         var = min(unassigned, key=lambda v: len(domains[v]))
#         self.tracker.add_state()

#         for value in list(domains[var]):
#             # Consistency check
#             conflict = False
#             for peer in peers[var]:
#                 if assignment.get(peer) == value:
#                     conflict = True
#                     break

#             if conflict:
#                 continue

#             assignment[var] = value
#             self.steps.append((var[0], var[1], value))

#             # Forward checking — peers ki domain prune karo
#             pruned = {}
#             failure = False

#             for peer in peers[var]:
#                 if peer not in assignment:
#                     if value in domains[peer]:
#                         domains[peer].discard(value)
#                         pruned[peer] = value
#                         if len(domains[peer]) == 0:
#                             failure = True
#                             break

#             if not failure:
#                 result = self._solve(assignment, domains, peers, fixed)
#                 if result:
#                     return result

#             # Undo
#             del assignment[var]
#             self.steps.append((var[0], var[1], 0))
#             self.tracker.add_backtrack()

#             # Domain restore karo
#             for peer, val in pruned.items():
#                 domains[peer].add(val)

#         return None

#     def get_tracker(self):
#         return self.tracker

#     def get_steps(self):
#         return self.steps
    

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