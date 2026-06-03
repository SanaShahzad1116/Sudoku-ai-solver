import tkinter as tk
from tkinter import messagebox
import threading
import copy
import time

from puzzle.generator               import PuzzleGenerator
from algorithms.backtracking        import BacktrackingSolver
from algorithms.ac3_mrv             import AC3MRVSolver
from algorithms.forward_checking    import ForwardCheckingSolver
from algorithms.simulated_annealing import SimulatedAnnealingSolver
from gui.board_widget               import BoardWidget
from gui.control_panel              import ControlPanel
from gui.dashboard                  import Dashboard

ALGO_MAP = {
    'Backtracking':        BacktrackingSolver,
    'AC3 + MRV':           AC3MRVSolver,
    'Forward Checking':    ForwardCheckingSolver,
    'Simulated Annealing': SimulatedAnnealingSolver,
}

class SudokuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('🧩 Sudoku AI Solver')
        self.configure(bg='#1a1a2e')

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = min(1100, sw - 40), min(700, sh - 60)
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f'{w}x{h}+{x}+{y}')
        self.resizable(True, True)
        self.minsize(900, 600)

        self.generator     = PuzzleGenerator()
        self.current_board = None
        self.solution      = None
        self.solving       = False
        self.results       = {}

        # ── Per-difficulty puzzle store ──────────────────
        # boards['Easy'] = (puzzle, solution) jab generate ho
        # Same puzzle tab tak rahega jab tak naya generate na ho
        self.boards = {
            'Easy':   None,
            'Medium': None,
            'Hard':   None,
            'Expert': None,
        }
        self.current_diff = None

        self._build_layout()

    def _build_layout(self):
        self.control = ControlPanel(
            self,
            on_generate    = self._generate,
            on_solve       = self._solve,
            on_compare     = self._compare,
            on_stop        = self._stop,
            on_adversarial = self._adversarial,
        )
        self.control.pack(side='left', fill='y')

        tk.Frame(self, width=3, bg='#00d4ff').pack(side='left', fill='y')

        right = tk.Frame(self, bg='#1a1a2e')
        right.pack(side='left', fill='both', expand=True)

        tk.Label(
            right,
            text='PUZZLE BOARD',
            font=('Arial', 13, 'bold'),
            bg='#1a1a2e', fg='#00d4ff'
        ).pack(pady=(10, 0))

        self.board_widget = BoardWidget(right)
        self.board_widget.pack(pady=5, padx=10)

        self.info_var = tk.StringVar(value='Generate a puzzle to begin!')
        tk.Label(
            right,
            textvariable=self.info_var,
            font=('Arial', 11),
            bg='#1a1a2e', fg='#aaaaaa'
        ).pack(pady=3)

    # ── GENERATE ──────────────────────────────────────────
    def _generate(self):
        diff = self.control.get_difficulty()
        self.control.set_status(f'Generating {diff} puzzle...')
        self.update()

        board, solution = self.generator.generate(diff)

        # Is difficulty ke liye puzzle SAVE karo
        self.boards[diff]  = (copy.deepcopy(board), solution)
        self.current_diff  = diff
        self.current_board = copy.deepcopy(board)
        self.solution      = solution

        self.board_widget.load_board(self.current_board)
        self.control.set_status(f'{diff} puzzle ready!')
        self.info_var.set(
            f'Difficulty: {diff}  |  '
            f'All algorithms will use this same {diff} puzzle')

    # ── SOLVE ─────────────────────────────────────────────
    def _solve(self, algo_name, speed):
        diff = self.control.get_difficulty()

        # Us difficulty ka saved puzzle check karo
        if self.boards[diff] is None:
            messagebox.showwarning(
                'No Puzzle',
                f'Please generate a {diff} puzzle first!\n'
                f'Select {diff} difficulty and click Generate Puzzle.')
            return

        if self.solving:
            return

        # SAME saved puzzle use karo — screen pe reload karo
        board, _ = self.boards[diff]
        self.current_board = copy.deepcopy(board)
        self.current_diff  = diff
        self.board_widget.load_board(self.current_board)

        self.solving = True
        self.control.set_status(f'Solving {diff} with {algo_name}...')

        threading.Thread(
            target=self._solve_thread,
            args=(algo_name, speed, copy.deepcopy(board), diff),
            daemon=True
        ).start()

    def _solve_thread(self, algo_name, speed, board, diff):
        solver   = ALGO_MAP[algo_name]()
        solution = solver.solve(board)
        steps    = solver.get_steps()
        if algo_name == "Simulated Annealing":
            initial_board = solver.get_initial_board()
            if initial_board:
                self.board_widget.show_solution(initial_board)
                self.update()
                time.sleep(1)
                tracker  = solver.get_tracker()
                delay    = (101 - speed) / 1000.0

        for step in steps:
            if not self.solving:
                break
            r, c, val = step
            self.board_widget.update_cell(
                r, c, val,
                '#00d4ff' if val != 0 else None)
            self.update()
            time.sleep(delay)

        if solution and self.solving:
            self.board_widget.show_solution(solution)
            self.board_widget.flash_solved()

        algo_key = algo_name.replace(' + ', '+')
        key      = (algo_key, diff)
        res      = tracker.get_results(algo_name)
        self.results[key] = res
        self.results[key]['status'] = 'Solved' if solution else 'Failed'

        self.control.set_metrics(
            res['time'], res['states'], res['backtracks'])
        self.control.set_status(
            '✅ Solved!' if solution else '❌ Failed')
        self.solving = False

    # ── COMPARE ALL ───────────────────────────────────────
    def _compare(self):
        # Kitne puzzles generate hue hain check karo
        generated = {
            d: v for d, v in self.boards.items()
            if v is not None
        }

        if not generated:
            messagebox.showwarning(
                'No Puzzles',
                'Please generate at least one puzzle first!\n\n'
                'For complete comparison:\n'
                'Generate Easy, Medium, Hard, Expert puzzles.')
            return

        # Fresh start
        self.results = {}

        total = len(generated) * len(ALGO_MAP)
        done  = 0

        for diff, (board, _) in generated.items():
            for algo_name, cls in ALGO_MAP.items():
                done += 1
                self.control.set_status(
                    f'[{done}/{total}] {algo_name} on {diff}...')
                self.update()

                try:
                    solver = cls()
                    # Har algo ko SAME puzzle ka fresh copy milta hai
                    solution_result = solver.solve(
                        copy.deepcopy(board))
                    res      = solver.get_tracker().get_results(
                        algo_name)
                    algo_key = algo_name.replace(' + ', '+')
                    key      = (algo_key, diff)
                    self.results[key] = res
                    self.results[key]['status'] = (
                        'Solved' if solution_result else 'Failed')

                except Exception as e:
                    algo_key = algo_name.replace(' + ', '+')
                    key      = (algo_key, diff)
                    self.results[key] = {
                        'algorithm':  algo_name,
                        'time':       'Error',
                        'states':     'Error',
                        'backtracks': 'Error',
                        'status':     str(e)
                    }

        self.control.set_status('Done! Opening dashboard...')
        Dashboard(self, self.results)

    # ── ADVERSARIAL MODE ──────────────────────────────────
    def _adversarial(self):
        diff = self.control.get_difficulty()

        if self.boards[diff] is None:
            messagebox.showwarning(
                'No Puzzle',
                f'Please generate a {diff} puzzle first!')
            return

        board, _ = self.boards[diff]
        AdversarialWindow(self, copy.deepcopy(board))

    # ── STOP ──────────────────────────────────────────────
    def _stop(self):
        self.solving = False
        self.control.set_status('Stopped.')


# ══════════════════════════════════════════════════════════
#  ADVERSARIAL MODE WINDOW — bilkul same as before
# ══════════════════════════════════════════════════════════
class AdversarialWindow(tk.Toplevel):
    """Two AI agents race to solve the same puzzle side by side."""

    def __init__(self, parent, board):
        super().__init__(parent)
        self.title('⚔️  Adversarial Mode — AI Race!')
        self.configure(bg='#1a1a2e')

        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w  = min(1100, sw - 40)
        h  = min(900,  sh - 40)
        self.geometry(f'{w}x{h}+{(sw-w)//2}+{(sh-h)//2}')
        self.resizable(True, True)

        self.board   = board
        self.running = False
        self.winner  = None
        self.result1 = {}
        self.result2 = {}

        self._build_ui()

    def _build_ui(self):
        outer_canvas = tk.Canvas(
            self, bg='#1a1a2e', highlightthickness=0)
        outer_vsb = tk.Scrollbar(
            self, orient='vertical', command=outer_canvas.yview)
        outer_canvas.configure(yscrollcommand=outer_vsb.set)
        outer_vsb.pack(side='right', fill='y')
        outer_canvas.pack(side='left', fill='both', expand=True)

        self.inner = tk.Frame(outer_canvas, bg='#1a1a2e')
        win_id = outer_canvas.create_window(
            (0, 0), window=self.inner, anchor='nw')

        def _on_frame(e):
            outer_canvas.configure(
                scrollregion=outer_canvas.bbox('all'))
        self.inner.bind('<Configure>', _on_frame)

        def _on_canvas(e):
            outer_canvas.itemconfig(win_id, width=e.width)
        outer_canvas.bind('<Configure>', _on_canvas)

        def _scroll(e):
            outer_canvas.yview_scroll(
                int(-1*(e.delta/120)), 'units')
        outer_canvas.bind_all('<MouseWheel>', _scroll)

        tk.Label(
            self.inner,
            text='⚔️  ADVERSARIAL MODE — AI RACE',
            font=('Arial', 18, 'bold'),
            bg='#1a1a2e', fg='#f5a623'
        ).pack(pady=(12, 2))

        tk.Label(
            self.inner,
            text='Two AI agents compete to solve the same puzzle. '
                 'Fastest wins!',
            font=('Arial', 10),
            bg='#1a1a2e', fg='#aaaaaa'
        ).pack()

        sel   = tk.Frame(self.inner, bg='#1a1a2e')
        sel.pack(pady=8)
        algos = list(ALGO_MAP.keys())

        tk.Label(sel, text='Agent 1 🔴',
                 font=('Arial', 12, 'bold'),
                 bg='#1a1a2e', fg='#e94560').grid(
                     row=0, column=0, padx=30)
        self.agent1_var = tk.StringVar(value=algos[0])
        a1_menu = tk.OptionMenu(sel, self.agent1_var, *algos)
        a1_menu.config(bg='#0f3460', fg='white',
                       font=('Arial', 10, 'bold'),
                       activebackground='#e94560',
                       highlightthickness=0)
        a1_menu.grid(row=1, column=0, padx=30)

        tk.Label(sel, text='VS',
                 font=('Arial', 16, 'bold'),
                 bg='#1a1a2e', fg='white').grid(
                     row=0, column=1, rowspan=2)

        tk.Label(sel, text='Agent 2 🔵',
                 font=('Arial', 12, 'bold'),
                 bg='#1a1a2e', fg='#00d4ff').grid(
                     row=0, column=2, padx=30)
        self.agent2_var = tk.StringVar(value=algos[1])
        a2_menu = tk.OptionMenu(sel, self.agent2_var, *algos)
        a2_menu.config(bg='#0f3460', fg='white',
                       font=('Arial', 10, 'bold'),
                       activebackground='#00d4ff',
                       highlightthickness=0)
        a2_menu.grid(row=1, column=2, padx=30)

        spd = tk.Frame(self.inner, bg='#1a1a2e')
        spd.pack(pady=4)
        tk.Label(spd, text='Speed:', bg='#1a1a2e',
                 fg='white', font=('Arial', 10)).pack(
                     side='left', padx=5)
        self.speed_var = tk.IntVar(value=80)
        tk.Scale(spd, from_=1, to=100, orient='horizontal',
                 variable=self.speed_var,
                 bg='#1a1a2e', fg='#00d4ff',
                 highlightthickness=0, troughcolor='#2a2a4a',
                 length=220).pack(side='left')

        tk.Button(
            self.inner,
            text='🚀  START RACE',
            command=self._start_race,
            bg='#e94560', fg='white',
            font=('Arial', 13, 'bold'),
            relief='flat', cursor='hand2', pady=7
        ).pack(pady=8, ipadx=20)

        boards_row = tk.Frame(self.inner, bg='#1a1a2e')
        boards_row.pack(fill='x', padx=10, pady=5)

        left = tk.Frame(boards_row, bg='#1a1a2e')
        left.pack(side='left', fill='both', expand=True)
        self.label1 = tk.Label(
            left, text='Agent 1 🔴',
            font=('Arial', 12, 'bold'),
            bg='#1a1a2e', fg='#e94560')
        self.label1.pack()
        self.board1 = BoardWidget(left)
        self.board1.pack()
        self.status1 = tk.Label(
            left, text='Waiting...',
            font=('Arial', 10),
            bg='#1a1a2e', fg='#aaaaaa')
        self.status1.pack(pady=3)

        tk.Label(boards_row, text='VS',
                 font=('Arial', 20, 'bold'),
                 bg='#1a1a2e', fg='#f5a623').pack(
                     side='left', padx=15)

        right = tk.Frame(boards_row, bg='#1a1a2e')
        right.pack(side='left', fill='both', expand=True)
        self.label2 = tk.Label(
            right, text='Agent 2 🔵',
            font=('Arial', 12, 'bold'),
            bg='#1a1a2e', fg='#00d4ff')
        self.label2.pack()
        self.board2 = BoardWidget(right)
        self.board2.pack()
        self.status2 = tk.Label(
            right, text='Waiting...',
            font=('Arial', 10),
            bg='#1a1a2e', fg='#aaaaaa')
        self.status2.pack(pady=3)

        self.winner_var = tk.StringVar(value='')
        self.winner_label = tk.Label(
            self.inner,
            textvariable=self.winner_var,
            font=('Arial', 15, 'bold'),
            bg='#1a1a2e', fg='#00ff88')
        self.winner_label.pack(pady=6)

        tk.Frame(self.inner, height=2, bg='#00d4ff').pack(
            fill='x', padx=20, pady=5)
        tk.Label(
            self.inner,
            text='📊 Race Comparison',
            font=('Arial', 14, 'bold'),
            bg='#1a1a2e', fg='#00d4ff'
        ).pack(pady=(5, 2))

        self.table_frame = tk.Frame(
            self.inner, bg='#16213e', relief='ridge', bd=2)
        self.table_frame.pack(fill='x', padx=30, pady=5)
        tk.Label(
            self.table_frame,
            text='Race results will appear here after solving...',
            font=('Arial', 10), bg='#16213e', fg='#555555'
        ).pack(pady=15)

        self.chart_frame = tk.Frame(self.inner, bg='#1a1a2e')
        self.chart_frame.pack(fill='x', padx=20, pady=5)
        tk.Label(
            self.chart_frame,
            text='Chart will appear here after both agents finish...',
            font=('Arial', 10), bg='#1a1a2e', fg='#555555'
        ).pack(pady=10)

    def _start_race(self):
        if self.running:
            return
        self.running = True
        self.winner  = None
        self.winner_var.set('')
        self.result1 = {}
        self.result2 = {}
        self.finished = 0

        for w in self.table_frame.winfo_children():
            w.destroy()
        for w in self.chart_frame.winfo_children():
            w.destroy()

        tk.Label(
            self.table_frame,
            text='Race in progress...',
            font=('Arial', 10), bg='#16213e', fg='#f5a623'
        ).pack(pady=15)

        a1 = self.agent1_var.get()
        a2 = self.agent2_var.get()
        self.label1.config(text=f'Agent 1 🔴  {a1}')
        self.label2.config(text=f'Agent 2 🔵  {a2}')
        self.status1.config(text='Solving...', fg='#00d4ff')
        self.status2.config(text='Solving...', fg='#00d4ff')
        self.board1.load_board(self.board)
        self.board2.load_board(self.board)

        speed = self.speed_var.get()

        threading.Thread(
            target=self._agent_thread,
            args=(1, a1, self.board1,
                  self.status1, self.result1, speed),
            daemon=True
        ).start()
        threading.Thread(
            target=self._agent_thread,
            args=(2, a2, self.board2,
                  self.status2, self.result2, speed),
            daemon=True
        ).start()

    def _agent_thread(self, agent_id, algo_name, board_widget,
                      status_label, result_dict, speed):
        solver   = ALGO_MAP[algo_name]()
        solution = solver.solve(copy.deepcopy(self.board))
        steps    = solver.get_steps()
        tracker  = solver.get_tracker()
        delay    = (101 - speed) / 2000.0

        for step in steps:
            if not self.running:
                break
            r, c, val = step
            color = '#e94560' if agent_id == 1 else '#00d4ff'
            board_widget.update_cell(
                r, c, val, color if val != 0 else None)
            self.update()
            time.sleep(delay)

        res = tracker.get_results(algo_name)
        result_dict.update(res)
        result_dict['solved']   = solution is not None
        result_dict['algo']     = algo_name
        result_dict['agent_id'] = agent_id

        if solution:
            board_widget.show_solution(solution)

        if solution:
            status_label.config(
                text=f"✅ Done!  {res['time']}s | "
                     f"{res['states']} states | "
                     f"{res['backtracks']} backtracks",
                fg='#00ff88')
        else:
            status_label.config(
                text='❌ Failed', fg='#e94560')

        if self.winner is None and solution:
            self.winner = agent_id
            icon = '🔴' if agent_id == 1 else '🔵'
            self.winner_var.set(
                f'🏆 Agent {agent_id} {icon} WINS!   '
                f'{algo_name}   |   '
                f'Time: {res["time"]}s   |   '
                f'States: {res["states"]}')

        self.finished = getattr(self, 'finished', 0) + 1
        if self.finished >= 2:
            self.running = False
            self.after(200, self._show_comparison)

    def _show_comparison(self):
        import matplotlib
        matplotlib.use('TkAgg')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        r1 = self.result1
        r2 = self.result2
        a1_name = r1.get('algo', 'Agent 1')
        a2_name = r2.get('algo', 'Agent 2')

        for w in self.table_frame.winfo_children():
            w.destroy()

        tk.Label(
            self.table_frame,
            text='📋 Side-by-Side Metrics',
            font=('Arial', 12, 'bold'),
            bg='#16213e', fg='#00d4ff'
        ).pack(pady=(8, 4))

        cols_frame = tk.Frame(self.table_frame, bg='#16213e')
        cols_frame.pack(padx=15, pady=5, fill='x')

        headers      = ['Metric',
                        f'🔴 {a1_name}',
                        f'🔵 {a2_name}',
                        'Winner']
        col_widths   = [15, 20, 20, 15]
        header_colors = ['#aaaaaa', '#e94560',
                         '#00d4ff', '#f5a623']

        for i, (h, w) in enumerate(
                zip(headers, col_widths)):
            tk.Label(
                cols_frame, text=h,
                font=('Arial', 10, 'bold'),
                bg='#0f3460', fg=header_colors[i],
                width=w, relief='ridge', pady=5
            ).grid(row=0, column=i,
                   sticky='nsew', padx=1, pady=1)

        metrics = [
            ('Time (s)',   'time',       True),
            ('States',     'states',     True),
            ('Backtracks', 'backtracks', True),
            ('Solved?',    'solved',     None),
        ]
        row_bgs = ['#1e2a3a', '#16213e']

        for row_i, (label, key, lower_better) in enumerate(
                metrics):
            v1 = r1.get(key, 'N/A')
            v2 = r2.get(key, 'N/A')

            if lower_better is not None:
                try:
                    f1, f2 = float(v1), float(v2)
                    metric_winner = (
                        f'🔴 {a1_name}'
                        if (f1 < f2) == lower_better
                        else f'🔵 {a2_name}')
                except Exception:
                    metric_winner = 'N/A'
            else:
                metric_winner = '—'

            row_data = [label, str(v1), str(v2), metric_winner]
            bg = row_bgs[row_i % 2]
            for col_i, (val, w) in enumerate(
                    zip(row_data, col_widths)):
                fg = '#ffffff'
                if col_i == 3:
                    fg = ('#e94560' if '🔴' in val
                          else '#00d4ff' if '🔵' in val
                          else '#aaaaaa')
                tk.Label(
                    cols_frame, text=val,
                    font=('Courier', 9),
                    bg=bg, fg=fg,
                    width=w, relief='ridge', pady=4
                ).grid(row=row_i + 1, column=col_i,
                       sticky='nsew', padx=1, pady=1)

        try:
            t1 = float(r1.get('time', 999))
            t2 = float(r2.get('time', 999))
            overall = (f'🏆 🔴 {a1_name}'
                       if t1 < t2
                       else f'🏆 🔵 {a2_name}')
            ov_fg = '#e94560' if t1 < t2 else '#00d4ff'
        except Exception:
            overall = 'N/A'
            ov_fg   = '#aaaaaa'

        tk.Label(
            self.table_frame,
            text=f'Overall Winner (by Time): {overall}',
            font=('Arial', 11, 'bold'),
            bg='#16213e', fg=ov_fg
        ).pack(pady=8)

        for w in self.chart_frame.winfo_children():
            w.destroy()

        tk.Label(
            self.chart_frame,
            text='📈 Performance Chart',
            font=('Arial', 13, 'bold'),
            bg='#1a1a2e', fg='#00d4ff'
        ).pack(pady=(10, 4))

        fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
        fig.patch.set_facecolor('#1a1a2e')

        chart_metrics = [
            ('Time (s)',   'time'),
            ('States',     'states'),
            ('Backtracks', 'backtracks'),
        ]

        for ax, (ylabel, key) in zip(axes, chart_metrics):
            ax.set_facecolor('#16213e')
            try:
                v1 = float(r1.get(key, 0))
                v2 = float(r2.get(key, 0))
            except Exception:
                v1, v2 = 0, 0

            bars = ax.bar(
                [f'🔴\n{a1_name[:8]}',
                 f'🔵\n{a2_name[:8]}'],
                [v1, v2],
                color=['#e94560', '#00d4ff'],
                width=0.5,
                edgecolor='white',
                linewidth=0.8)

            for bar, val in zip(bars, [v1, v2]):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() * 1.02,
                    (f'{val:.4f}' if key == 'time'
                     else str(int(val))),
                    ha='center', va='bottom',
                    color='white', fontsize=8,
                    fontweight='bold')

            winner_bar = 0 if v1 < v2 else 1
            bars[winner_bar].set_edgecolor('#f5a623')
            bars[winner_bar].set_linewidth(2.5)

            ax.set_title(ylabel, color='#00d4ff',
                         fontsize=10, fontweight='bold')
            ax.tick_params(colors='white', labelsize=8)
            ax.spines[:].set_color('#2a2a4a')
            ax.yaxis.grid(True, color='#2a2a4a',
                          linestyle='--', alpha=0.5)

        fig.suptitle(
            'Agent 1 🔴  vs  Agent 2 🔵 — Performance Comparison',
            color='#f5a623', fontsize=11, fontweight='bold')
        fig.tight_layout()

        canvas_chart = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas_chart.draw()
        canvas_chart.get_tk_widget().pack(
            fill='x', padx=15, pady=10)

        try:
            t1 = float(r1.get('time', 0))
            t2 = float(r2.get('time', 0))
            s1 = int(r1.get('states', 0))
            s2 = int(r2.get('states', 0))
            b1 = int(r1.get('backtracks', 0))
            b2 = int(r2.get('backtracks', 0))
            faster  = a1_name if t1 < t2 else a2_name
            speedup = (max(t1, t2)
                       / max(min(t1, t2), 0.0001))
            analysis = (
                f"📝 Analysis:  {faster} was "
                f"{speedup:.1f}x faster.  "
                f"States — {a1_name}: {s1} vs "
                f"{a2_name}: {s2}.  "
                f"Backtracks — {a1_name}: {b1} vs "
                f"{a2_name}: {b2}.")
        except Exception:
            analysis = 'Complete the race to see analysis.'

        tk.Label(
            self.chart_frame,
            text=analysis,
            font=('Arial', 9),
            bg='#1a1a2e', fg='#aaaaaa',
            wraplength=750, justify='center'
        ).pack(pady=(0, 15))