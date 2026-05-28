

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



# # import tkinter as tk
# # from tkinter import ttk
# # import matplotlib.pyplot as plt

# # class Dashboard(tk.Frame):
# #     def __init__(self, master):
# #         super().__init__(master)

# #         self.table = ttk.Treeview(self, columns=("Algo", "Time", "States", "Backtracks"), show="headings")

# #         for col in ("Algo", "Time", "States", "Backtracks"):
# #             self.table.heading(col, text=col)

# #         self.table.pack(fill="both", expand=True)

# #         tk.Button(self, text="Show Graph", command=self.plot_graph).pack(pady=5)

# #         self.data = []

# #     def update(self, results):
# #         self.data = results
# #         for row in self.table.get_children():
# #             self.table.delete(row)

# #         for r in results:
# #             self.table.insert("", "end", values=(
# #                 r["algorithm"],
# #                 r["time"],
# #                 r["states"],
# #                 r["backtracks"]
# #             ))

# #     def plot_graph(self):
# #         if not self.data:
# #             return

# #         algos = [d["algorithm"] for d in self.data]
# #         times = [d["time"] for d in self.data]
# #         states = [d["states"] for d in self.data]

# #         plt.figure()

# #         plt.subplot(1, 2, 1)
# #         plt.bar(algos, times)
# #         plt.title("Time Comparison")

# #         plt.subplot(1, 2, 2)
# #         plt.bar(algos, states)
# #         plt.title("States Explored")

# #         plt.tight_layout()
# #         plt.show()

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

COLORS = {
    'bg':     '#1a1a2e',
    'grid':   '#16213e',
    'accent': '#00d4ff',
    'text':   '#ffffff',
}

ALGO_COLORS = ['#e94560', '#00d4ff', '#f5a623', '#00b894']
ALGOS  = ['Backtracking', 'AC3+MRV', 'Forward Checking', 'Simulated Annealing']
LEVELS = ['Easy', 'Medium', 'Hard', 'Expert']


class Dashboard(tk.Toplevel):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.title('📊 Performance Comparison Dashboard')
        self.configure(bg=COLORS['bg'])

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w  = min(1200, sw - 40)
        h  = min(800,  sh - 40)
        self.geometry(f'{w}x{h}+{(sw-w)//2}+{(sh-h)//2}')
        self.resizable(True, True)

        self.results = results
        self._build_ui()

    # ── helper: safe float ────────────────────────────
    def _val(self, algo, level, metric):
        r = self.results.get((algo, level), {})
        v = r.get(metric, None)
        try:
            return float(v)
        except (TypeError, ValueError):
            return 0.0

    def _build_ui(self):
        tk.Label(
            self,
            text='📊 Algorithm Performance Comparison',
            font=('Arial', 18, 'bold'),
            bg=COLORS['bg'], fg=COLORS['accent']
        ).pack(pady=10)

        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook',
                        background=COLORS['bg'], borderwidth=0)
        style.configure('TNotebook.Tab',
                        background='#16213e', foreground='white',
                        padding=[12, 5], font=('Arial', 10, 'bold'))
        style.map('TNotebook.Tab',
                  background=[('selected', '#0f3460')],
                  foreground=[('selected', '#00d4ff')])

        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=10, pady=5)

        # ── Tab 1: Data Table ─────────────────────────
        t1 = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(t1, text='📋 Data Table')
        self._build_table(t1)

        # ── Tab 2: Bar - Time ─────────────────────────
        t2 = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(t2, text='⏱ Time (Bar)')
        self._build_bar(t2, 'time', 'Solve Time (seconds)', 'Time Comparison')

        # ── Tab 3: Bar - States ───────────────────────
        t3 = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(t3, text='🔍 States (Bar)')
        self._build_bar(t3, 'states', 'States Explored', 'States Explored')

        # ── Tab 4: Bar - Backtracks ───────────────────
        t4 = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(t4, text='↩ Backtracks (Bar)')
        self._build_bar(t4, 'backtracks', 'Backtracks', 'Backtracks Comparison')

        # ── Tab 5: Line - All metrics trend ──────────
        t5 = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(t5, text='📈 Trend (Line)')
        self._build_line(t5)

        # ── Tab 6: Winner Analysis ────────────────────
        t6 = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(t6, text='🏆 Winner Analysis')
        self._build_winner(t6)

    # ══════════════════════════════════════════════════
    #  TABLE
    # ══════════════════════════════════════════════════
    def _build_table(self, parent):
        tk.Label(parent,
                 text='Performance Metrics — All Algorithms × All Difficulty Levels',
                 font=('Arial', 13, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['accent']).pack(pady=8)

        frame = tk.Frame(parent, bg=COLORS['bg'])
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        vsb = tk.Scrollbar(frame, orient='vertical')
        hsb = tk.Scrollbar(frame, orient='horizontal')
        vsb.pack(side='right',  fill='y')
        hsb.pack(side='bottom', fill='x')

        s = ttk.Style()
        s.configure('Custom.Treeview',
                    background='#16213e', foreground='white',
                    rowheight=28, fieldbackground='#16213e',
                    font=('Courier', 10))
        s.configure('Custom.Treeview.Heading',
                    background='#0f3460', foreground='#00d4ff',
                    font=('Arial', 11, 'bold'))

        cols = ('Algorithm', 'Difficulty', 'Time (s)',
                'States', 'Backtracks', 'Status')
        tv = ttk.Treeview(frame, columns=cols, show='headings',
                          style='Custom.Treeview',
                          yscrollcommand=vsb.set,
                          xscrollcommand=hsb.set)
        vsb.config(command=tv.yview)
        hsb.config(command=tv.xview)

        widths = [170, 120, 120, 140, 140, 110]
        for col, w in zip(cols, widths):
            tv.heading(col, text=col)
            tv.column(col,  width=w, anchor='center')

        row_bgs = ['#1e2a3a', '#16213e']
        i = 0
        for algo in ALGOS:
            for level in LEVELS:
                r      = self.results.get((algo, level), {})
                time_s = r.get('time',       'N/A')
                states = r.get('states',     'N/A')
                backs  = r.get('backtracks', 'N/A')
                status = r.get('status',     'N/A')
                tag    = f'row{i % 2}'
                tv.insert('', 'end',
                          values=(algo, level, time_s,
                                  states, backs, status),
                          tags=(tag,))
                tv.tag_configure(tag, background=row_bgs[i % 2])
                i += 1

        tv.pack(fill='both', expand=True)

    # ══════════════════════════════════════════════════
    #  BAR CHART  (used for Time / States / Backtracks)
    # ══════════════════════════════════════════════════
    def _build_bar(self, parent, metric, ylabel, title):
        fig, ax = plt.subplots(figsize=(9, 4.8))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#16213e')

        x      = np.arange(len(LEVELS))
        width  = 0.18
        offset = -(width * (len(ALGOS) - 1) / 2)

        for idx, algo in enumerate(ALGOS):
            vals = [self._val(algo, lv, metric) for lv in LEVELS]

            bars = ax.bar(x + offset, vals, width,
                          label=algo,
                          color=ALGO_COLORS[idx],
                          alpha=0.85,
                          edgecolor='white',
                          linewidth=0.5)
            offset += width

            for bar, v in zip(bars, vals):
                if v > 0:
                    label_txt = (f'{v:.3f}' if metric == 'time'
                                 else str(int(v)))
                    ax.text(bar.get_x() + bar.get_width() / 2,
                            bar.get_height() * 1.01,
                            label_txt,
                            ha='center', va='bottom',
                            color='white', fontsize=7,
                            fontweight='bold')

        ax.set_xticks(x)
        ax.set_xticklabels(LEVELS, color='white', fontsize=11)
        ax.set_ylabel(ylabel,  color='white', fontsize=11)
        ax.set_title(title,    color='#00d4ff',
                     fontsize=14, fontweight='bold')
        ax.legend(facecolor='#0f3460', edgecolor='#00d4ff',
                  labelcolor='white', fontsize=9)
        ax.tick_params(colors='white')
        ax.spines[:].set_color('#2a2a4a')
        ax.yaxis.grid(True, color='#2a2a4a',
                      linestyle='--', alpha=0.5)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True,
                                    padx=10, pady=10)

    # ══════════════════════════════════════════════════
    #  LINE CHART  — trend across difficulty levels
    # ══════════════════════════════════════════════════
    def _build_line(self, parent):
        tk.Label(parent,
                 text='Performance Trend Across Difficulty Levels',
                 font=('Arial', 13, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['accent']).pack(pady=6)

        tk.Label(parent,
                 text='Shows how each algorithm degrades as difficulty increases  '
                      '(lower = better for all metrics)',
                 font=('Arial', 9),
                 bg=COLORS['bg'], fg='#aaaaaa').pack()

        # 3 sub-plots: Time / States / Backtracks
        fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
        fig.patch.set_facecolor('#1a1a2e')

        metrics = [
            ('time',       'Solve Time (s)',    'Time Trend'),
            ('states',     'States Explored',   'States Trend'),
            ('backtracks', 'Backtracks',        'Backtracks Trend'),
        ]

        markers = ['o', 's', '^', 'D']   # circle, square, triangle, diamond

        for ax, (metric, ylabel, title) in zip(axes, metrics):
            ax.set_facecolor('#16213e')

            for idx, algo in enumerate(ALGOS):
                vals = [self._val(algo, lv, metric) for lv in LEVELS]

                ax.plot(LEVELS, vals,
                        color=ALGO_COLORS[idx],
                        marker=markers[idx],
                        linewidth=2.2,
                        markersize=7,
                        label=algo,
                        alpha=0.9)

                # Value annotation on each point
                for lv, v in zip(LEVELS, vals):
                    if v > 0:
                        ax.annotate(
                            f'{v:.2f}' if metric == 'time' else str(int(v)),
                            xy=(lv, v),
                            xytext=(0, 8),
                            textcoords='offset points',
                            ha='center', fontsize=6,
                            color=ALGO_COLORS[idx],
                            fontweight='bold'
                        )

            ax.set_title(title, color='#00d4ff',
                         fontsize=11, fontweight='bold')
            ax.set_ylabel(ylabel, color='white', fontsize=9)
            ax.tick_params(colors='white', labelsize=8)
            ax.spines[:].set_color('#2a2a4a')
            ax.yaxis.grid(True, color='#2a2a4a',
                          linestyle='--', alpha=0.4)
            ax.set_facecolor('#16213e')

        # Shared legend at bottom
        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels,
                   loc='lower center',
                   ncol=4,
                   facecolor='#0f3460',
                   edgecolor='#00d4ff',
                   labelcolor='white',
                   fontsize=9,
                   bbox_to_anchor=(0.5, -0.02))

        fig.suptitle('Algorithm Performance Trend: Easy → Medium → Hard → Expert',
                     color='#f5a623', fontsize=12, fontweight='bold')
        fig.tight_layout(rect=[0, 0.08, 1, 1])

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True,
                                    padx=10, pady=10)

    # ══════════════════════════════════════════════════
    #  WINNER ANALYSIS
    # ══════════════════════════════════════════════════
    def _build_winner(self, parent):
        tk.Label(parent,
                 text='🏆 Algorithm Winner Analysis',
                 font=('Arial', 15, 'bold'),
                 bg=COLORS['bg'], fg='#f5a623').pack(pady=10)

        # Scrollable canvas
        container = tk.Frame(parent, bg=COLORS['bg'])
        container.pack(fill='both', expand=True)

        canvas    = tk.Canvas(container, bg=COLORS['bg'],
                              highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical',
                                 command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left',  fill='both', expand=True)

        inner     = tk.Frame(canvas, bg=COLORS['bg'])
        window_id = canvas.create_window((0, 0), window=inner,
                                         anchor='nw')

        inner.bind('<Configure>',
                   lambda e: canvas.configure(
                       scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
                    lambda e: canvas.itemconfig(
                        window_id, width=e.width))
        canvas.bind_all('<MouseWheel>',
                        lambda e: canvas.yview_scroll(
                            int(-1*(e.delta/120)), 'units'))

        for level in LEVELS:
            box = tk.Frame(inner, bg='#16213e',
                           relief='ridge', bd=2)
            box.pack(fill='x', pady=6, padx=10)

            tk.Label(box, text=f'  {level} Difficulty',
                     font=('Arial', 12, 'bold'),
                     bg='#16213e', fg='#f5a623').pack(
                         anchor='w', padx=10, pady=5)

            # Find winner (lowest time)
            best_time = None
            best_algo = None
            for algo in ALGOS:
                t = self._val(algo, level, 'time')
                if t > 0 and (best_time is None or t < best_time):
                    best_time = t
                    best_algo = algo

            row = tk.Frame(box, bg='#16213e')
            row.pack(fill='x', padx=10, pady=5)

            for algo in ALGOS:
                r     = self.results.get((algo, level), {})
                t     = r.get('time',       'N/A')
                s     = r.get('states',     'N/A')
                b     = r.get('backtracks', 'N/A')
                is_w  = (algo == best_algo)
                color = '#00ff88' if is_w else '#aaaaaa'
                badge = '🏆 '    if is_w else '   '
                bg_c  = '#0f3460' if is_w else '#1e2a3a'

                cell = tk.Frame(row, bg=bg_c,
                                relief='ridge', bd=1)
                cell.pack(side='left', padx=5, pady=3,
                          fill='x', expand=True)

                tk.Label(cell,
                         text=f'{badge}{algo}',
                         font=('Arial', 9, 'bold'),
                         bg=bg_c, fg=color).pack(pady=(5, 2))

                for emoji, val in [('⏱', t), ('🔍', s), ('↩', b)]:
                    tk.Label(cell,
                             text=f'{emoji} {val}',
                             font=('Courier', 8),
                             bg=bg_c, fg='white').pack()

                tk.Frame(cell, height=5, bg=bg_c).pack()