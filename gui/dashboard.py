

# import tkinter as tk
# from tkinter import ttk

# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure


# class Dashboard(tk.Frame):

#     def __init__(self, parent):

#         super().__init__(
#             parent,
#             bg="#121212"
#         )

#         self.results = []

#         # TITLE
#         title = tk.Label(
#             self,
#             text="AI Performance Dashboard",
#             font=("Arial", 22, "bold"),
#             bg="#121212",
#             fg="#00ffee"
#         )

#         title.pack(pady=15)

#         # =========================
#         # MAIN CONTENT FRAME
#         # =========================

#         content = tk.Frame(
#             self,
#             bg="#121212"
#         )

#         content.pack(
#             fill="both",
#             expand=True
#         )

#         # =========================
#         # TABLE SECTION
#         # =========================

#         table_frame = tk.Frame(
#             content,
#             bg="#121212"
#         )

#         table_frame.pack(
#             side="left",
#             padx=20,
#             pady=10
#         )

#         columns = (
#             "Algorithm",
#             "Time (s)",
#             "States",
#             "Backtracks"
#         )

#         self.table = ttk.Treeview(
#             table_frame,
#             columns=columns,
#             show="headings",
#             height=8
#         )

#         for col in columns:

#             self.table.heading(
#                 col,
#                 text=col
#             )

#             self.table.column(
#                 col,
#                 width=140,
#                 anchor="center"
#             )

#         self.table.pack()

#         # =========================
#         # BAR CHART
#         # =========================

#         chart_frame = tk.Frame(
#             content,
#             bg="#121212"
#         )

#         chart_frame.pack(
#             side="left",
#             padx=20
#         )

#         self.figure1 = Figure(
#             figsize=(5.5, 3.5),
#             dpi=100
#         )

#         self.ax1 = self.figure1.add_subplot(111)

#         self.canvas1 = FigureCanvasTkAgg(
#             self.figure1,
#             master=chart_frame
#         )

#         self.canvas1.get_tk_widget().pack()

#         # =========================
#         # LINE CHART
#         # =========================

#         self.figure2 = Figure(
#             figsize=(5.5, 3.5),
#             dpi=100
#         )

#         self.ax2 = self.figure2.add_subplot(111)

#         self.canvas2 = FigureCanvasTkAgg(
#             self.figure2,
#             master=chart_frame
#         )

#         self.canvas2.get_tk_widget().pack(
#             pady=20
#         )

#     def add_result(self, result):

#         self.results.append(result)

#         self.table.insert(
#             "",
#             "end",
#             values=(
#                 result["algorithm"],
#                 result["time"],
#                 result["states"],
#                 result["backtracks"]
#             )
#         )

#         self.update_charts()

#     def update_charts(self):

#         algorithms = [
#             r["algorithm"]
#             for r in self.results
#         ]

#         times = [
#             r["time"]
#             for r in self.results
#         ]

#         # BAR CHART
#         self.ax1.clear()

#         bars = self.ax1.bar(
#             algorithms,
#             times
#         )

#         self.ax1.set_title(
#             "Execution Time Comparison"
#         )

#         self.ax1.set_ylabel(
#             "Seconds"
#         )

#         for bar, value in zip(bars, times):

#             self.ax1.text(
#                 bar.get_x() + bar.get_width()/2,
#                 bar.get_height(),
#                 f"{value:.4f}",
#                 ha='center',
#                 va='bottom'
#             )

#         self.canvas1.draw()

#         # LINE CHART
#         self.ax2.clear()

#         self.ax2.plot(
#             algorithms,
#             times,
#             marker='o'
#         )

#         self.ax2.set_title(
#             "Performance Trend"
#         )

#         self.ax2.set_ylabel(
#             "Execution Time"
#         )

#         self.canvas2.draw()

#     def clear(self):

#         self.results.clear()

#         for row in self.table.get_children():
#             self.table.delete(row)

#         self.ax1.clear()
#         self.ax2.clear()

#         self.canvas1.draw()
#         self.canvas2.draw()



import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

class Dashboard(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.table = ttk.Treeview(self, columns=("Algo", "Time", "States", "Backtracks"), show="headings")

        for col in ("Algo", "Time", "States", "Backtracks"):
            self.table.heading(col, text=col)

        self.table.pack(fill="both", expand=True)

        tk.Button(self, text="Show Graph", command=self.plot_graph).pack(pady=5)

        self.data = []

    def update(self, results):
        self.data = results
        for row in self.table.get_children():
            self.table.delete(row)

        for r in results:
            self.table.insert("", "end", values=(
                r["algorithm"],
                r["time"],
                r["states"],
                r["backtracks"]
            ))

    def plot_graph(self):
        if not self.data:
            return

        algos = [d["algorithm"] for d in self.data]
        times = [d["time"] for d in self.data]
        states = [d["states"] for d in self.data]

        plt.figure()

        plt.subplot(1, 2, 1)
        plt.bar(algos, times)
        plt.title("Time Comparison")

        plt.subplot(1, 2, 2)
        plt.bar(algos, states)
        plt.title("States Explored")

        plt.tight_layout()
        plt.show()