# import tkinter as tk

# class SudokuBoard(tk.Frame):
#     def __init__(self, parent):
#         super().__init__(parent, bg="#222")

#         self.cells = []

#         for r in range(9):
#             row = []

#             for c in range(9):

#                 frame = tk.Frame(
#                     self,
#                     bg="black",
#                     highlightbackground="white",
#                     highlightthickness=1
#                 )

#                 frame.grid(
#                     row=r,
#                     column=c,
#                     padx=(2 if c % 3 == 0 else 1),
#                     pady=(2 if r % 3 == 0 else 1)
#                 )

#                 cell = tk.Label(
#                     frame,
#                     text="",
#                     width=3,
#                     height=1,
#                     font=("Arial", 20, "bold"),
#                     bg="#121212",
#                     fg="#00ffcc"
#                 )

#                 cell.pack()
#                 row.append(cell)

#             self.cells.append(row)

#     def draw_board(self, board):

#         for r in range(9):
#             for c in range(9):

#                 value = board[r][c]

#                 if value == 0:
#                     self.cells[r][c].config(
#                         text="",
#                         fg="white"
#                     )
#                 else:
#                     self.cells[r][c].config(
#                         text=str(value),
#                         fg="#00ff99"
#                     )

#     def animate_steps(self, steps, delay=20):

#         def animate(index):

#             if index >= len(steps):
#                 return

#             r, c, value = steps[index]

#             if value == 0:
#                 self.cells[r][c].config(
#                     text="",
#                     fg="red"
#                 )
#             else:
#                 self.cells[r][c].config(
#                     text=str(value),
#                     fg="yellow"
#                 )

#             self.after(delay, lambda: animate(index + 1))

#         animate(0)


# # import tkinter as tk
# # import time

# # class BoardWidget(tk.Frame):
# #     def __init__(self, master):
# #         super().__init__(master, bg="#0f172a")

# #         self.cells = {}
# #         self._build_grid()

# #     def _build_grid(self):
# #         for r in range(9):
# #             for c in range(9):

# #                 bg_color = "#1e293b" if (r//3 + c//3) % 2 == 0 else "#334155"

# #                 frame = tk.Frame(
# #                     self,
# #                     width=55,
# #                     height=55,
# #                     bg=bg_color,
# #                     highlightbackground="#64748b",
# #                     highlightthickness=1
# #                 )
# #                 frame.grid(row=r, column=c)

# #                 label = tk.Label(
# #                     frame,
# #                     text="",
# #                     font=("Segoe UI", 14, "bold"),
# #                     bg=bg_color,
# #                     fg="#f8fafc"
# #                 )
# #                 label.pack(expand=True)

# #                 self.cells[(r, c)] = label

# #     def set_board(self, board):
# #         for r in range(9):
# #             for c in range(9):
# #                 val = board[r][c]
# #                 self.cells[(r, c)].config(text=str(val) if val != 0 else "")

# #     def animate_steps(self, steps):
# #         for (r, c, val) in steps:
# #             self.cells[(r, c)].config(
# #                 text="" if val == 0 else str(val),
# #                 fg="#22c55e" if val != 0 else "#f87171"
# #             )
# #             self.update()
# #             time.sleep(0.01)





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