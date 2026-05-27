

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
ALGOS       = ['Backtracking', 'AC3+MRV', 'Fwd Checking', 'Sim Annealing']
LEVELS      = ['Easy', 'Medium', 'Hard', 'Expert']

class Dashboard(tk.Toplevel):
    def __init__(self, parent, results):
        super().__init__(parent)
        self.title('📊 Performance Comparison Dashboard')
        self.configure(bg=COLORS['bg'])
        self.geometry('1100x750')
        self.results = results
        self._build_ui()

    def _build_ui(self):
        # Title
        tk.Label(
            self,
            text='📊 Algorithm Performance Comparison',
            font=('Arial', 18, 'bold'),
            bg=COLORS['bg'],
            fg=COLORS['accent']
        ).pack(pady=10)

        # Notebook (tabs)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'TNotebook',
            background=COLORS['bg'],
            borderwidth=0
        )
        style.configure(
            'TNotebook.Tab',
            background='#16213e',
            foreground='white',
            padding=[12, 5],
            font=('Arial', 11, 'bold')
        )
        style.map(
            'TNotebook.Tab',
            background=[('selected', '#0f3460')],
            foreground=[('selected', '#00d4ff')]
        )

        nb = ttk.Notebook(self)
        nb.pack(fill='both', expand=True, padx=10, pady=5)

        # Tab 1 - Table
        tab_table = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(tab_table, text='📋 Data Table')
        self._build_table(tab_table)

        # Tab 2 - Time Chart
        tab_time = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(tab_time, text='⏱ Time Comparison')
        self._build_chart(tab_time, 'time', 'Solve Time (seconds)', 'Time Comparison')

        # Tab 3 - States Chart
        tab_states = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(tab_states, text='🔍 States Explored')
        self._build_chart(tab_states, 'states', 'States Explored', 'States Explored')

        # Tab 4 - Backtracks Chart
        tab_backs = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(tab_backs, text='↩ Backtracks')
        self._build_chart(tab_backs, 'backtracks', 'Backtracks', 'Backtracks Comparison')

        # Tab 5 - Radar Chart
        tab_radar = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(tab_radar, text='🕸 Radar Overview')
        self._build_radar(tab_radar)

        # Tab 6 - Winner
        tab_winner = tk.Frame(nb, bg=COLORS['bg'])
        nb.add(tab_winner, text='🏆 Winner Analysis')
        self._build_winner(tab_winner)

    # ── TABLE ──────────────────────────────────────────────
    def _build_table(self, parent):
        tk.Label(
            parent,
            text='Performance Metrics - All Algorithms × All Difficulty Levels',
            font=('Arial', 13, 'bold'),
            bg=COLORS['bg'], fg=COLORS['accent']
        ).pack(pady=8)

        frame = tk.Frame(parent, bg=COLORS['bg'])
        frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Scrollbars
        vsb = tk.Scrollbar(frame, orient='vertical')
        hsb = tk.Scrollbar(frame, orient='horizontal')
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        cols = ('Algorithm', 'Difficulty', 'Time (s)', 'States', 'Backtracks', 'Status')
        tree = ttk.Style()
        tree.configure(
            'Custom.Treeview',
            background='#16213e',
            foreground='white',
            rowheight=28,
            fieldbackground='#16213e',
            font=('Courier', 10)
        )
        tree.configure(
            'Custom.Treeview.Heading',
            background='#0f3460',
            foreground='#00d4ff',
            font=('Arial', 11, 'bold')
        )

        tv = ttk.Treeview(
            frame,
            columns=cols,
            show='headings',
            style='Custom.Treeview',
            yscrollcommand=vsb.set,
            xscrollcommand=hsb.set
        )
        vsb.config(command=tv.yview)
        hsb.config(command=tv.xview)

        for col in cols:
            tv.heading(col, text=col)
            tv.column(col, width=140, anchor='center')

        # Row colors
        row_colors = ['#1e2a3a', '#16213e']
        i = 0
        for algo in ALGOS:
            for level in LEVELS:
                r = self.results.get((algo, level), {})
                time_s   = r.get('time', 'N/A')
                states   = r.get('states', 'N/A')
                backs    = r.get('backtracks', 'N/A')
                status   = r.get('status', 'N/A')
                tag = f'row{i%2}'
                tv.insert(
                    '', 'end',
                    values=(algo, level, time_s, states, backs, status),
                    tags=(tag,)
                )
                tv.tag_configure(tag, background=row_colors[i%2])
                i += 1

        tv.pack(fill='both', expand=True)

    # ── BAR CHART ──────────────────────────────────────────
    def _build_chart(self, parent, metric, ylabel, title):
        fig, ax = plt.subplots(figsize=(9, 4.5))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#16213e')

        x      = np.arange(len(LEVELS))
        width  = 0.18
        offset = 0

        for idx, algo in enumerate(ALGOS):
            vals = []
            for level in LEVELS:
                r = self.results.get((algo, level), {})
                v = r.get(metric, 0)
                try:
                 vals.append(float(v) if v not in (None, 'N/A', '') else 0.0)
                except:
                 vals.append(0.0)
                # try:    vals.append(float(v))
                # except: vals.append(0)
            bars = ax.bar(
                x + offset, vals, width,
                label=algo,
                color=ALGO_COLORS[idx],
                alpha=0.85,
                edgecolor='white',
                linewidth=0.5
            )
            # Value labels on bars
            for bar in bars:
                h = bar.get_height()
                if h > 0:
                    ax.text(
                        bar.get_x() + bar.get_width()/2,
                        h * 1.01,
                        f'{h:.3f}' if metric == 'time' else str(int(h)),
                        ha='center', va='bottom',
                        color='white', fontsize=7, fontweight='bold'
                    )
            offset += width

        ax.set_xticks(x + width*1.5)
        ax.set_xticklabels(LEVELS, color='white', fontsize=11)
        ax.set_ylabel(ylabel, color='white', fontsize=11)
        ax.set_title(title, color='#00d4ff', fontsize=14, fontweight='bold')
        ax.legend(
            facecolor='#0f3460', edgecolor='#00d4ff',
            labelcolor='white', fontsize=9
        )
        ax.tick_params(colors='white')
        ax.spines[:].set_color('#2a2a4a')
        ax.yaxis.grid(True, color='#2a2a4a', linestyle='--', alpha=0.5)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)

    # ── RADAR CHART ────────────────────────────────────────
    def _build_radar(self, parent):
        tk.Label(
            parent,
            text='Overall Performance Overview (Lower = Better)',
            font=('Arial', 13, 'bold'),
            bg=COLORS['bg'], fg=COLORS['accent']
        ).pack(pady=8)

        metrics = ['Time', 'States', 'Backtracks']
        N = len(metrics)
        angles = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 5), subplot_kw=dict(polar=True))
        fig.patch.set_facecolor('#1a1a2e')
        ax.set_facecolor('#16213e')

        for idx, algo in enumerate(ALGOS):
            # Average across all levels
            vals = []
            for m in ['time', 'states', 'backtracks']:
                total = 0
                count = 0
                for level in LEVELS:
                    r = self.results.get((algo, level), {})
                    v = r.get(m, 0)
                    try:
                        total += float(v)
                        count += 1
                    except:
                        pass
                vals.append(total / count if count else 0)

            # Normalize 0-1
            max_vals = [max([
                float(self.results.get((a, l), {}).get(m, 0) or 0)
                for a in ALGOS for l in LEVELS
            ]) or 1 for m in ['time', 'states', 'backtracks']]

            norm = [v/mx for v, mx in zip(vals, max_vals)]
            norm += norm[:1]

            ax.plot(angles, norm, 'o-', linewidth=2,
                    color=ALGO_COLORS[idx], label=algo)
            ax.fill(angles, norm, alpha=0.1, color=ALGO_COLORS[idx])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(metrics, color='white', size=12)
        ax.set_yticklabels([])
        ax.spines['polar'].set_color('#2a2a4a')
        ax.grid(color='#2a2a4a')
        ax.legend(
            loc='upper right',
            bbox_to_anchor=(1.3, 1.1),
            facecolor='#0f3460',
            edgecolor='#00d4ff',
            labelcolor='white',
            fontsize=9
        )
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=5)

    def _build_winner(self, parent):
        tk.Label(
            parent,
            text='🏆 Algorithm Winner Analysis',
            font=('Arial', 15, 'bold'),
            bg=COLORS['bg'], fg='#f5a623'
        ).pack(pady=10)

        # ── Scrollable canvas ──────────────────────────
        container = tk.Frame(parent, bg=COLORS['bg'])
        container.pack(fill='both', expand=True)

        canvas = tk.Canvas(container, bg=COLORS['bg'],
                           highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient='vertical',
                                 command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        inner = tk.Frame(canvas, bg=COLORS['bg'])
        window_id = canvas.create_window((0, 0), window=inner, anchor='nw')

        def on_frame_configure(e):
            canvas.configure(scrollregion=canvas.bbox('all'))
        inner.bind('<Configure>', on_frame_configure)

        def on_canvas_configure(e):
            canvas.itemconfig(window_id, width=e.width)
        canvas.bind('<Configure>', on_canvas_configure)

        # Touchpad / mousewheel scroll
        def _on_mousewheel(e):
            canvas.yview_scroll(int(-1*(e.delta/120)), 'units')
        canvas.bind_all('<MouseWheel>', _on_mousewheel)

        # ── Content ────────────────────────────────────
        for level in LEVELS:
            box = tk.Frame(inner, bg='#16213e', relief='ridge', bd=2)
            box.pack(fill='x', pady=6, padx=10)

            tk.Label(
                box,
                text=f'  {level} Difficulty',
                font=('Arial', 12, 'bold'),
                bg='#16213e', fg='#f5a623'
            ).pack(anchor='w', padx=10, pady=5)

            best_time = None
            best_algo = None
            for algo in ALGOS:
                r = self.results.get((algo, level), {})
                try:
                    t = float(r.get('time', None))
                    if best_time is None or t < best_time:
                        best_time = t
                        best_algo = algo
                except:
                    pass

            row = tk.Frame(box, bg='#16213e')
            row.pack(fill='x', padx=10, pady=5)

            for algo in ALGOS:
                r    = self.results.get((algo, level), {})
                t    = r.get('time', 'N/A')
                s    = r.get('states', 'N/A')
                b    = r.get('backtracks', 'N/A')
                is_w = (algo == best_algo)
                color = '#00ff88' if is_w else '#aaaaaa'
                badge = '🏆 ' if is_w else '   '
                bg_c  = '#0f3460' if is_w else '#1e2a3a'

                cell = tk.Frame(row, bg=bg_c, relief='ridge', bd=1)
                cell.pack(side='left', padx=5, pady=3,
                          fill='x', expand=True)

                tk.Label(cell, text=f'{badge}{algo}',
                         font=('Arial', 10, 'bold'),
                         bg=bg_c, fg=color).pack(pady=(5,2))

                for emoji, val in [('⏱', t), ('🔍', s), ('↩', b)]:
                    tk.Label(cell, text=f'{emoji} {val}',
                             font=('Courier', 9),
                             bg=bg_c, fg='white').pack()

                tk.Frame(cell, height=5, bg=bg_c).pack()