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


import tkinter as tk
import time

class BoardWidget(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#0f172a")

        self.cells = {}
        self._build_grid()

    def _build_grid(self):
        for r in range(9):
            for c in range(9):

                bg_color = "#1e293b" if (r//3 + c//3) % 2 == 0 else "#334155"

                frame = tk.Frame(
                    self,
                    width=55,
                    height=55,
                    bg=bg_color,
                    highlightbackground="#64748b",
                    highlightthickness=1
                )
                frame.grid(row=r, column=c)

                label = tk.Label(
                    frame,
                    text="",
                    font=("Segoe UI", 14, "bold"),
                    bg=bg_color,
                    fg="#f8fafc"
                )
                label.pack(expand=True)

                self.cells[(r, c)] = label

    def set_board(self, board):
        for r in range(9):
            for c in range(9):
                val = board[r][c]
                self.cells[(r, c)].config(text=str(val) if val != 0 else "")

    def animate_steps(self, steps):
        for (r, c, val) in steps:
            self.cells[(r, c)].config(
                text="" if val == 0 else str(val),
                fg="#22c55e" if val != 0 else "#f87171"
            )
            self.update()
            time.sleep(0.01)