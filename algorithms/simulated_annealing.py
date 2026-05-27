import random
import math
import copy
from performance.tracker import PerformanceTracker

class SimulatedAnnealingSolver:
    def __init__(self):
        self.tracker = PerformanceTracker()
        self.steps = []

    def solve(self, board):
        self.steps = []
        self.tracker.start()

        current = self._fill_boxes(board)
        current_cost = self._cost(current)

        temp = 1.0
        cooling = 0.9995
        min_temp = 0.001
        max_iter = 100000

        best = copy.deepcopy(current)
        best_cost = current_cost

        for i in range(max_iter):
            if current_cost == 0:
                break

            temp *= cooling
            if temp < min_temp:
                break

            neighbor, r, c1, c2 = self._get_neighbor(current, board)
            neighbor_cost = self._cost(neighbor)
            self.tracker.add_state()

            delta = neighbor_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / temp):
                current = neighbor
                current_cost = neighbor_cost
                self.steps.append((r, c1, current[r][c1]))
                self.steps.append((r, c2, current[r][c2]))

                if current_cost < best_cost:
                    best = copy.deepcopy(current)
                    best_cost = current_cost

        self.tracker.stop()

        if best_cost == 0:
            return best
        # Return best attempt even if not perfect
        return best

    def _fill_boxes(self, board):
        grid = copy.deepcopy(board)
        for box_r in range(3):
            for box_c in range(3):
                missing = list(range(1, 10))
                cells = []
                for r in range(box_r*3, box_r*3+3):
                    for c in range(box_c*3, box_c*3+3):
                        if grid[r][c] != 0:
                            if grid[r][c] in missing:
                                missing.remove(grid[r][c])
                        else:
                            cells.append((r, c))
                random.shuffle(missing)
                for i, (r, c) in enumerate(cells):
                    grid[r][c] = missing[i] if i < len(missing) else random.randint(1,9)
        return grid

    def _cost(self, grid):
        cost = 0
        for i in range(9):
            cost += (9 - len(set(grid[i])))           # row duplicates
            cost += (9 - len(set(grid[r][i] for r in range(9))))  # col duplicates
        return cost

    def _get_neighbor(self, grid, fixed):
        new_grid = copy.deepcopy(grid)
        # Pick random box, swap two non-fixed cells
        for _ in range(100):
            box_r = random.randint(0, 2)
            box_c = random.randint(0, 2)
            cells = []
            for r in range(box_r*3, box_r*3+3):
                for c in range(box_c*3, box_c*3+3):
                    if fixed[r][c] == 0:
                        cells.append((r, c))
            if len(cells) >= 2:
                (r1, c1), (r2, c2) = random.sample(cells, 2)
                new_grid[r1][c1], new_grid[r2][c2] = new_grid[r2][c2], new_grid[r1][c1]
                return new_grid, r1, c1, c2
        return new_grid, 0, 0, 1

    def get_tracker(self):
        return self.tracker

    def get_steps(self):
        return self.steps