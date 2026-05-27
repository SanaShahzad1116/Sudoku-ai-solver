# CSP Formulation for Sudoku
# Variables: each cell (row, col)
# Domain: 1-9 for empty cells, fixed value for pre-filled
# Constraints: row, column, box uniqueness

class SudokuCSP:
    def __init__(self, board):
        # board is 9x9 list, 0 means empty
        self.board = [row[:] for row in board]
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = self._init_domains()
        self.constraints = self._init_constraints()

    def _init_domains(self):
        domains = {}
        for (r, c) in self.variables:
            if self.board[r][c] != 0:
                domains[(r, c)] = [self.board[r][c]]
            else:
                domains[(r, c)] = list(range(1, 10))
        return domains

    def _init_constraints(self):
        constraints = {}
        for var in self.variables:
            constraints[var] = self._get_peers(var)
        return constraints

    def _get_peers(self, var):
        r, c = var
        peers = set()
        # Same row
        for col in range(9):
            if col != c:
                peers.add((r, col))
        # Same column
        for row in range(9):
            if row != r:
                peers.add((row, c))
        # Same 3x3 box
        box_r, box_c = 3 * (r // 3), 3 * (c // 3)
        for row in range(box_r, box_r + 3):
            for col in range(box_c, box_c + 3):
                if (row, col) != var:
                    peers.add((row, col))
        return peers

    def is_consistent(self, var, value, assignment):
        for peer in self.constraints[var]:
            if assignment.get(peer) == value:
                return False
        return True

    def get_unassigned_variables(self, assignment):
        return [v for v in self.variables if v not in assignment]

    def is_complete(self, assignment):
        return len(assignment) == 81

    def get_peers(self, var):
        return self.constraints[var]