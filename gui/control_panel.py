
# import tkinter as tk
# from tkinter import ttk


# class ControlPanel(tk.Frame):

#     def __init__(
#         self,
#         parent,
#         generate_callback,
#         solve_callback,
#         benchmark_callback
#     ):

#         super().__init__(
#             parent,
#             bg="#1f1f1f",
#             padx=20,
#             pady=15
#         )

#         style = ttk.Style()
#         style.theme_use("clam")

#         # Difficulty
#         tk.Label(
#             self,
#             text="Difficulty",
#             font=("Arial", 12, "bold"),
#             bg="#1f1f1f",
#             fg="white"
#         ).grid(row=0, column=0, padx=10)

#         self.difficulty = ttk.Combobox(
#             self,
#             values=["Easy", "Medium", "Hard", "Expert"],
#             state="readonly",
#             width=15
#         )

#         self.difficulty.current(0)

#         self.difficulty.grid(
#             row=0,
#             column=1,
#             padx=10
#         )

#         # Algorithm
#         tk.Label(
#             self,
#             text="Algorithm",
#             font=("Arial", 12, "bold"),
#             bg="#1f1f1f",
#             fg="white"
#         ).grid(row=0, column=2, padx=10)

#         self.algorithm = ttk.Combobox(
#             self,
#             values=[
#                 "Backtracking",
#                 "AC3 + MRV",
#                 "Forward Checking",
#                 "Simulated Annealing"
#             ],
#             state="readonly",
#             width=20
#         )

#         self.algorithm.current(0)

#         self.algorithm.grid(
#             row=0,
#             column=3,
#             padx=10
#         )

#         # Buttons
#         generate_btn = tk.Button(
#             self,
#             text="Generate Puzzle",
#             font=("Arial", 11, "bold"),
#             bg="#00c896",
#             fg="white",
#             width=16,
#             command=lambda:
#                 generate_callback(
#                     self.difficulty.get()
#                 )
#         )

#         generate_btn.grid(
#             row=0,
#             column=4,
#             padx=10
#         )

#         solve_btn = tk.Button(
#             self,
#             text="Solve",
#             font=("Arial", 11, "bold"),
#             bg="#ff8800",
#             fg="white",
#             width=12,
#             command=lambda:
#                 solve_callback(
#                     self.algorithm.get()
#                 )
#         )

#         solve_btn.grid(
#             row=0,
#             column=5,
#             padx=10
#         )

#         benchmark_btn = tk.Button(
#             self,
#             text="Run Benchmark",
#             font=("Arial", 11, "bold"),
#             bg="#0066ff",
#             fg="white",
#             width=16,
#             command=benchmark_callback
#         )

#         benchmark_btn.grid(
#             row=0,
#             column=6,
#             padx=10
#         )


import tkinter as tk
from tkinter import ttk

class ControlPanel(tk.Frame):
    def __init__(self, master, run_callback, compare_callback, race_callback):
        super().__init__(master, bg="#111827")

        self.run_callback = run_callback
        self.compare_callback = compare_callback
        self.race_callback = race_callback

        self.algorithm = tk.StringVar(value="Backtracking")
        self.difficulty = tk.StringVar(value="Easy")

        self._build()

    def _build(self):
        title = tk.Label(
            self,
            text="SUDOKU AI ENGINE",
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#111827"
        )
        title.pack(pady=10)

        ttk.Label(self, text="Difficulty").pack()
        ttk.Combobox(self, textvariable=self.difficulty,
                     values=["Easy", "Medium", "Hard", "Expert"]).pack(pady=5)

        ttk.Label(self, text="Algorithm").pack()
        ttk.Combobox(self, textvariable=self.algorithm,
                     values=["Backtracking", "AC3_MRV",
                             "ForwardChecking", "SimulatedAnnealing"]).pack(pady=5)

        tk.Button(self, text="▶ Solve",
                  bg="#22c55e", fg="black",
                  command=self.run).pack(pady=8, fill="x")

        tk.Button(self, text="📊 Compare",
                  bg="#3b82f6", fg="white",
                  command=self.compare).pack(pady=8, fill="x")

        tk.Button(self, text="⚔ AI Race",
                  bg="#f59e0b", fg="black",
                  command=self.race).pack(pady=8, fill="x")

    def run(self):
        self.run_callback(self.algorithm.get(), self.difficulty.get())

    def compare(self):
        self.compare_callback(self.difficulty.get())

    def race(self):
        self.race_callback(self.difficulty.get())