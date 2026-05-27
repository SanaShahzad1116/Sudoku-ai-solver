import tkinter as tk
from tkinter import ttk

from gui.board_widget import BoardWidget
from gui.control_panel import ControlPanel
from gui.dashboard import Dashboard

from puzzle.generator import PuzzleGenerator

from algorithms.backtracking import BacktrackingSolver
from algorithms.ac3_mrv import AC3MRVSolver
from algorithms.forward_checking import ForwardCheckingSolver
from algorithms.simulated_annealing import SimulatedAnnealingSolver


class SudokuApp:

    def __init__(self, root):

        self.root = root

        self.generator = PuzzleGenerator()

        self.current_board = None

        # =========================
        # TITLE
        # =========================

        title = tk.Label(
            root,
            text="AI Powered Sudoku Solver",
            font=("Arial", 32, "bold"),
            bg="#121212",
            fg="#00ffee"
        )

        title.pack(pady=20)

        # STATUS
        self.status = tk.Label(
            root,
            text="Ready",
            font=("Arial", 14, "bold"),
            bg="#121212",
            fg="#00ff99"
        )

        self.status.pack()

        # CONTROLS
        self.controls = ControlPanel(
            root,
            self.generate_puzzle,
            self.solve_puzzle,
            self.run_benchmark
        )

        self.controls.pack(
            pady=20
        )

        # BOARD
        self.board = SudokuBoard(root)

        self.board.pack(
            pady=10
        )

        # DASHBOARD
        self.dashboard = Dashboard(root)

        self.dashboard.pack(
            fill="both",
            expand=True,
            pady=20
        )

    def generate_puzzle(self, difficulty):

        puzzle, solution = self.generator.generate(
            difficulty
        )

        self.current_board = puzzle

        self.board.draw_board(
            puzzle
        )

        self.dashboard.clear()

        self.status.config(
            text=f"{difficulty} puzzle generated"
        )

    def solve_puzzle(self, algorithm):

        if not self.current_board:

            messagebox.showerror(
                "Error",
                "Generate puzzle first"
            )

            return

        solver = self.get_solver(algorithm)

        self.status.config(
            text=f"Running {algorithm}..."
        )

        self.root.update()

        solution = solver.solve(
            [row[:] for row in self.current_board]
        )

        if solution:

            self.board.animate_steps(
                solver.get_steps(),
                delay=10
            )

            result = solver.get_tracker().get_results(
                algorithm
            )

            self.dashboard.add_result(
                result
            )

            self.status.config(
                text=f"{algorithm} completed"
            )

    def run_benchmark(self):

        if not self.current_board:
            return

        self.dashboard.clear()

        algorithms = [
            ("Backtracking", BacktrackingSolver),
            ("AC3 + MRV", AC3MRVSolver),
            ("Forward Checking", ForwardCheckingSolver),
            ("Simulated Annealing", SimulatedAnnealingSolver)
        ]

        for name, SolverClass in algorithms:

            solver = SolverClass()

            solver.solve(
                [row[:] for row in self.current_board]
            )

            result = solver.get_tracker().get_results(
                name
            )

            self.dashboard.add_result(
                result
            )

        self.status.config(
            text="Benchmark Complete"
        )

    def get_solver(self, algorithm):

        if algorithm == "Backtracking":
            return BacktrackingSolver()

        elif algorithm == "AC3 + MRV":
            return AC3MRVSolver()

        elif algorithm == "Forward Checking":
            return ForwardCheckingSolver()

        else:
            return SimulatedAnnealingSolver()



# class SudokuApp(tk.Tk):
#     def __init__(self):
#         super().__init__()

#         self.title("AI Sudoku Solver | CCP Project")
#         self.geometry("1250x750")
#         self.configure(bg="#0f172a")  # dark navy background

#         self._setup_style()

#         self.generator = PuzzleGenerator()

#         # LEFT PANEL (Controls)
#         self.control_frame = tk.Frame(self, bg="#111827", padx=10, pady=10)
#         self.control_frame.grid(row=0, column=0, sticky="ns")

#         # CENTER (Board)
#         self.board_frame = tk.Frame(self, bg="#0f172a")
#         self.board_frame.grid(row=0, column=1, padx=20, pady=20)

#         # RIGHT (Dashboard)
#         self.dashboard_frame = tk.Frame(self, bg="#111827", padx=10, pady=10)
#         self.dashboard_frame.grid(row=0, column=2, sticky="ns")

#         self.board_widget = BoardWidget(self.board_frame)
#         self.board_widget.pack()

#         self.dashboard = Dashboard(self.dashboard_frame)
#         self.dashboard.pack()

#         self.control = ControlPanel(
#             self.control_frame,
#             self.run_solver,
#             self.compare_all,
#             self.race_mode
#         )
#         self.control.pack()

#         self.load_new_puzzle()

#     # 🎨 MODERN STYLE SYSTEM
#     def _setup_style(self):
#         style = ttk.Style(self)
#         style.theme_use("clam")

#         style.configure("TButton",
#                         font=("Segoe UI", 10, "bold"),
#                         padding=6)

#         style.configure("TLabel",
#                         background="#111827",
#                         foreground="white",
#                         font=("Segoe UI", 10))

#         style.configure("TCombobox",
#                         padding=5)

#     # -------------------------
#     def load_new_puzzle(self, difficulty="Easy"):
#         self.current_puzzle, _ = self.generator.generate(difficulty)
#         self.board_widget.set_board(self.current_puzzle)

#     # -------------------------
#     def run_solver(self, algo, difficulty):
#         self.load_new_puzzle(difficulty)

#         solvers = {
#             "Backtracking": BacktrackingSolver(),
#             "AC3_MRV": AC3MRVSolver(),
#             "ForwardChecking": ForwardCheckingSolver(),
#             "SimulatedAnnealing": SimulatedAnnealingSolver()
#         }

#         solver = solvers[algo]
#         solver.solve(self.current_puzzle)

#         self.board_widget.animate_steps(solver.get_steps())

#     # -------------------------
#     def compare_all(self, difficulty):
#         self.load_new_puzzle(difficulty)

#         solvers = {
#             "Backtracking": BacktrackingSolver(),
#             "AC3_MRV": AC3MRVSolver(),
#             "ForwardChecking": ForwardCheckingSolver(),
#             "SimulatedAnnealing": SimulatedAnnealingSolver()
#         }

#         results = []

#         for name, solver in solvers.items():
#             solver.solve(self.current_puzzle)
#             results.append(solver.get_tracker().get_results(name))

#         self.dashboard.update(results)

#     # -------------------------
#     def race_mode(self, difficulty):
#         self.compare_all(difficulty)


# if __name__ == "__main__":
#     app = SudokuApp()
#     app.mainloop()