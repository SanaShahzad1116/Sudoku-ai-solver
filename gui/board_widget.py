import tkinter as tk

# Colors for colorful theme
COLORS = {
    'bg':           '#1a1a2e',
    'grid_bg':      '#16213e',
    'cell_fixed':   '#0f3460',
    'cell_empty':   '#1a1a2e',
    'text_fixed':   '#e94560',
    'text_solving': '#00d4ff',
    'text_correct': '#00ff88',
    'highlight':    '#f5a623',
    'border':       '#e94560',
    'box_border':   '#00d4ff',
}

class BoardWidget(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg'], **kwargs)
        self.cells = {}
        self.fixed_cells = set()
        self.canvas = tk.Canvas(
            self,
            width=450, height=450,
            bg=COLORS['bg'],
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
        self._draw_grid()

    def _draw_grid(self):
        self.canvas.delete('all')
        cell_size = 50

        # Draw cells
        for r in range(9):
            for c in range(9):
                x1 = c * cell_size
                y1 = r * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=COLORS['cell_empty'],
                    outline='#2a2a4a',
                    width=1,
                    tags=f'cell_{r}_{c}'
                )
                # Cell text
                self.canvas.create_text(
                    x1 + cell_size//2,
                    y1 + cell_size//2,
                    text='',
                    font=('Arial', 18, 'bold'),
                    fill=COLORS['text_fixed'],
                    tags=f'text_{r}_{c}'
                )

        # Draw 3x3 box borders (thick)
        for i in range(4):
            x = i * 3 * cell_size
            self.canvas.create_line(x, 0, x, 450, fill=COLORS['box_border'], width=3)
            self.canvas.create_line(0, x, 450, x, fill=COLORS['box_border'], width=3)

    def load_board(self, board):
        self.fixed_cells = set()
        self._draw_grid()
        cell_size = 50
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    self.fixed_cells.add((r, c))
                    x1 = c * cell_size
                    y1 = r * cell_size
                    # Fixed cell background
                    self.canvas.itemconfig(
                        f'cell_{r}_{c}',
                        fill=COLORS['cell_fixed']
                    )
                    self.canvas.itemconfig(
                        f'text_{r}_{c}',
                        text=str(board[r][c]),
                        fill=COLORS['text_fixed']
                    )

    def update_cell(self, r, c, value, color=None):
        cell_size = 50
        if (r, c) in self.fixed_cells:
            return
        fill_color = color or (COLORS['text_solving'] if value != 0 else '')
        bg_color = '#0a2a1a' if value != 0 else COLORS['cell_empty']
        self.canvas.itemconfig(f'cell_{r}_{c}', fill=bg_color)
        self.canvas.itemconfig(
            f'text_{r}_{c}',
            text=str(value) if value != 0 else '',
            fill=fill_color
        )

    def show_solution(self, board):
        for r in range(9):
            for c in range(9):
                if (r, c) not in self.fixed_cells:
                    self.update_cell(r, c, board[r][c], COLORS['text_correct'])

    def flash_solved(self):
        # Flash all cells green when solved
        for r in range(9):
            for c in range(9):
                self.canvas.itemconfig(
                    f'cell_{r}_{c}',
                    fill='#003320'
                )
        self.update()