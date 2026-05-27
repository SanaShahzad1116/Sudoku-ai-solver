import random
import copy

class PuzzleGenerator:
    # Difficulty: number of clues (pre-filled cells)
    DIFFICULTY = {
        'Easy':   46,
        'Medium': 32,
        'Hard':   28,
        'Expert': 24
    }

    def generate(self, difficulty='Easy'):
        board = self._generate_full_board()
        clues = self.DIFFICULTY[difficulty]
        puzzle = self._remove_cells(board, 81 - clues)
        return puzzle, board  # puzzle = with blanks, board = full solution

    def _generate_full_board(self):
        board = [[0]*9 for _ in range(9)]
        self._fill_board(board)
        return board

    def _fill_board(self, board):
        empty = self._find_empty(board)
        if not empty:
            return True
        r, c = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self._is_valid(board, r, c, num):
                board[r][c] = num
                if self._fill_board(board):
                    return True
                board[r][c] = 0
        return False

    def _remove_cells(self, board, count):
        puzzle = copy.deepcopy(board)
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        removed = 0
        for (r, c) in cells:
            if removed >= count:
                break
            backup = puzzle[r][c]
            puzzle[r][c] = 0
            # Check unique solution
            test = copy.deepcopy(puzzle)
            if self._count_solutions(test) == 1:
                removed += 1
            else:
                puzzle[r][c] = backup
        return puzzle

    def _count_solutions(self, board, limit=2):
        empty = self._find_empty(board)
        if not empty:
            return 1
        r, c = empty
        count = 0
        for num in range(1, 10):
            if self._is_valid(board, r, c, num):
                board[r][c] = num
                count += self._count_solutions(board, limit)
                board[r][c] = 0
                if count >= limit:
                    return count
        return count

    def _find_empty(self, board):
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def _is_valid(self, board, r, c, num):
        # Row check
        if num in board[r]:
            return False
        # Column check
        if num in [board[row][c] for row in range(9)]:
            return False
        # Box check
        box_r, box_c = 3 * (r // 3), 3 * (c // 3)
        for row in range(box_r, box_r + 3):
            for col in range(box_c, box_c + 3):
                if board[row][col] == num:
                    return False
        return True