# import random
# import math
# import copy
# from performance.tracker import PerformanceTracker

# class SimulatedAnnealingSolver:
#     def __init__(self):
#         self.tracker = PerformanceTracker()
#         self.steps   = []

#     def solve(self, board):
#         self.steps = []
#         self.tracker.start()

#         current      = self._fill_boxes(board)
#         current_cost = self._cost(current)

#         temp        = 2.0
#         cooling     = 0.9997
#         min_temp    = 0.001
#         max_iter    = 150000

#         best      = copy.deepcopy(current)
#         best_cost = current_cost

#         for i in range(max_iter):
#             if current_cost == 0:
#                 break
#             if temp < min_temp:
#                 break

#             temp *= cooling

#             neighbor, r, c1, c2 = self._get_neighbor(current, board)
#             neighbor_cost        = self._cost(neighbor)

#             # count every iteration as a state
#             self.tracker.add_state()

#             delta = neighbor_cost - current_cost

#             # if delta < 0 or random.random() < math.exp(
#             #         max(-500, -delta / temp)):
#             #     current      = neighbor
#             #     current_cost = neighbor_cost
#             if delta < 0 or random.random() < math.exp(-delta / temp):
#                 current = neighbor
#                 current_cost = neighbor_cost
#             else:
#                 self.tracker.add_backtrack()  # ✅ rejection count karo

#                 # Only record step every 50 iterations (keep animation light)
#                 if i % 50 == 0:
#                     self.steps.append((r, c1, current[r][c1]))
#                     self.steps.append((r, c2, current[r][c2]))

#                 if current_cost < best_cost:
#                     best      = copy.deepcopy(current)
#                     best_cost = current_cost

#             # Count as backtrack when cost gets worse and we reject
#                 else:
#                     self.tracker.add_backtrack()
 
#         self.tracker.stop()
#         return best   # always return best found

#     # ── helpers ───────────────────────────────────────────
#     def _fill_boxes(self, board):
#         grid = copy.deepcopy(board)
#         for box_r in range(3):
#             for box_c in range(3):
#                 missing = list(range(1, 10))
#                 cells   = []
#                 for r in range(box_r*3, box_r*3+3):
#                     for c in range(box_c*3, box_c*3+3):
#                         if grid[r][c] != 0:
#                             if grid[r][c] in missing:
#                                 missing.remove(grid[r][c])
#                         else:
#                             cells.append((r, c))
#                 random.shuffle(missing)
#                 for idx, (r, c) in enumerate(cells):
#                     grid[r][c] = missing[idx] if idx < len(missing) \
#                                  else random.randint(1, 9)
#         return grid

#     def _cost(self, grid):
#         cost = 0
#         for i in range(9):
#             cost += 9 - len(set(grid[i]))
#             cost += 9 - len(set(grid[r][i] for r in range(9)))
#         return cost

#     def _get_neighbor(self, grid, fixed):
#         new_grid = copy.deepcopy(grid)
#         for _ in range(200):
#             box_r = random.randint(0, 2)
#             box_c = random.randint(0, 2)
#             cells = [
#                 (r, c)
#                 for r in range(box_r*3, box_r*3+3)
#                 for c in range(box_c*3, box_c*3+3)
#                 if fixed[r][c] == 0
#             ]
#             if len(cells) >= 2:
#                 (r1, c1), (r2, c2) = random.sample(cells, 2)
#                 new_grid[r1][c1], new_grid[r2][c2] = \
#                     new_grid[r2][c2], new_grid[r1][c1]
#                 return new_grid, r1, c1, c2
#         return new_grid, 0, 0, 1

#     def get_tracker(self):
#         return self.tracker

#     def get_steps(self):
#         return self.steps



import random
import math
import copy
from performance.tracker import PerformanceTracker


class SimulatedAnnealingSolver:
    """
    Local Search — Simulated Annealing.

    Starts from a complete (but inconsistent) assignment,
    iteratively reduces constraint violations via probabilistic
    neighbour acceptance. Not guaranteed to find a solution.

    States    = accepted moves (actual transitions)
    Backtracks = rejected moves (cost-increasing moves refused)
    """

    def __init__(self):
        self.tracker = PerformanceTracker()
        self.steps = []

    def solve(self, board):
        self.steps = []
        self.tracker.start()

        current = self._fill_boxes(board)
        current_cost = self._cost(current)

        temp = 2.0
        cooling = 0.9997
        min_temp = 0.001
        max_iter = 150000

        best = copy.deepcopy(current)
        best_cost = current_cost
        step_counter = 0

        for i in range(max_iter):
            # Stop early if perfect solution found
            if current_cost == 0:
                break
            if temp < min_temp:
                break

            temp *= cooling

            neighbor, r1, c1, r2, c2 = self._get_neighbor(current, board)
            neighbor_cost = self._cost(neighbor)
            delta = neighbor_cost - current_cost

            # Accept or reject
            if delta < 0:
                # Always accept improvement
                current = neighbor
                current_cost = neighbor_cost
                self.tracker.add_state()

                step_counter += 1
                if step_counter % 100 == 0:
                    self.steps.append((r1, c1, current[r1][c1]))
                    self.steps.append((r2, c2, current[r2][c2]))

            else:
                # Accept worse solution probabilistically
                try:
                    prob = math.exp(-delta / temp)
                except OverflowError:
                    prob = 0.0

                if random.random() < prob:
                    current = neighbor
                    current_cost = neighbor_cost
                    self.tracker.add_state()

                    step_counter += 1
                    if step_counter % 100 == 0:
                        self.steps.append((r1, c1, current[r1][c1]))
                        self.steps.append((r2, c2, current[r2][c2]))
                else:
                    # Rejected move — equivalent to backtrack in SA
                    self.tracker.add_backtrack()

            # Track best solution seen
            if current_cost < best_cost:
                best = copy.deepcopy(current)
                best_cost = current_cost

        self.tracker.stop()

        # Return perfect solution if found, else best attempt
        if best_cost == 0:
            return best
        return best

    def _fill_boxes(self, board):
        """
        Fill each 3x3 box with digits 1-9 (no intra-box duplicates).
        This gives a complete assignment where only row/col constraints
        may be violated — SA then works to fix those.
        """
        grid = copy.deepcopy(board)
        for box_r in range(3):
            for box_c in range(3):
                missing = list(range(1, 10))
                cells = []
                for r in range(box_r * 3, box_r * 3 + 3):
                    for c in range(box_c * 3, box_c * 3 + 3):
                        if grid[r][c] != 0:
                            if grid[r][c] in missing:
                                missing.remove(grid[r][c])
                        else:
                            cells.append((r, c))
                random.shuffle(missing)
                for idx, (r, c) in enumerate(cells):
                    if idx < len(missing):
                        grid[r][c] = missing[idx]
                    else:
                        # Fallback — should not happen with valid puzzle
                        grid[r][c] = random.randint(1, 9)
        return grid

    def _cost(self, grid):
        """
        Count total duplicates in rows and columns.
        Cost = 0 means valid solution.
        """
        cost = 0
        for i in range(9):
            cost += 9 - len(set(grid[i]))
            cost += 9 - len(set(grid[r][i] for r in range(9)))
        return cost

    def _get_neighbor(self, grid, fixed):
        """
        Swap two non-fixed cells within the same 3x3 box.
        Preserves intra-box validity, changes row/col conflicts.
        Returns (new_grid, r1, c1, r2, c2).
        """
        new_grid = copy.deepcopy(grid)
        for _ in range(200):
            box_r = random.randint(0, 2)
            box_c = random.randint(0, 2)
            cells = [
                (r, c)
                for r in range(box_r * 3, box_r * 3 + 3)
                for c in range(box_c * 3, box_c * 3 + 3)
                if fixed[r][c] == 0
            ]
            if len(cells) >= 2:
                (r1, c1), (r2, c2) = random.sample(cells, 2)
                new_grid[r1][c1], new_grid[r2][c2] = (
                    new_grid[r2][c2], new_grid[r1][c1]
                )
                return new_grid, r1, c1, r2, c2

        # Fallback — no valid swap found
        return new_grid, 0, 0, 0, 1

    def get_tracker(self):
        return self.tracker

    def get_steps(self):
        return self.steps