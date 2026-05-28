import tkinter as tk

COLORS = {
    'bg':       '#1a1a2e',
    'btn_blue': '#0f3460',
    'btn_red':  '#e94560',
    'btn_green':'#00b894',
    'btn_gold': '#f5a623',
    'btn_purp': '#6c5ce7',
    'text':     '#ffffff',
    'accent':   '#00d4ff',
}

class ControlPanel(tk.Frame):
    def __init__(self, parent, on_generate, on_solve,
                 on_compare, on_stop, on_adversarial, **kwargs):
        super().__init__(parent, bg=COLORS['bg'], **kwargs)

        self.on_generate    = on_generate
        self.on_solve       = on_solve
        self.on_compare     = on_compare
        self.on_stop        = on_stop
        self.on_adversarial = on_adversarial

        self._build_ui()

    def _build_ui(self):
        # Scrollable inner frame for small screens
        canvas = tk.Canvas(self, bg=COLORS['bg'],
                           highlightthickness=0, width=300)
        vsb = tk.Scrollbar(self, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        inner = tk.Frame(canvas, bg=COLORS['bg'])
        win_id = canvas.create_window((0,0), window=inner, anchor='nw')

        def _on_frame(e):
            canvas.configure(scrollregion=canvas.bbox('all'))
        inner.bind('<Configure>', _on_frame)

        def _on_canvas(e):
            canvas.itemconfig(win_id, width=e.width)
        canvas.bind('<Configure>', _on_canvas)

        def _scroll(e):
            canvas.yview_scroll(int(-1*(e.delta/120)), 'units')
        canvas.bind_all('<MouseWheel>', _scroll)

        # ── Title ──────────────────────────────────────
        tk.Label(
            inner,
            text='🧩 SUDOKU AI SOLVER',
            font=('Arial', 16, 'bold'),
            bg=COLORS['bg'], fg=COLORS['accent']
        ).pack(pady=(12, 2))

        tk.Label(
            inner,
            text='Multi-Algorithm AI Solver',
            font=('Arial', 9),
            bg=COLORS['bg'], fg='#aaaaaa'
        ).pack(pady=(0, 8))

        tk.Frame(inner, height=2, bg=COLORS['accent']).pack(fill='x', padx=10)

        # ── Difficulty ─────────────────────────────────
        tk.Label(inner, text='Difficulty Level',
                 font=('Arial', 11, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(10,2))

        self.difficulty_var = tk.StringVar(value='Easy')
        diff_frame = tk.Frame(inner, bg=COLORS['bg'])
        diff_frame.pack(pady=3)

        diff_colors = {'Easy':'#00b894','Medium':'#f5a623',
                       'Hard':'#e17055','Expert':'#e94560'}
        for d in ['Easy','Medium','Hard','Expert']:
            tk.Radiobutton(
                diff_frame, text=d,
                variable=self.difficulty_var, value=d,
                bg=COLORS['bg'], fg=diff_colors[d],
                selectcolor='#2a2a4a',
                activebackground=COLORS['bg'],
                font=('Arial', 10, 'bold')
            ).pack(side='left', padx=5)

        # ── Algorithm ──────────────────────────────────
        tk.Label(inner, text='Algorithm',
                 font=('Arial', 11, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(12,2))

        self.algo_var = tk.StringVar(value='Backtracking')
        algos = [
            ('Backtracking',        '#e94560'),
            ('AC3 + MRV',           '#00d4ff'),
            ('Forward Checking',    '#f5a623'),
            ('Simulated Annealing', '#00b894'),
        ]
        algo_frame = tk.Frame(inner, bg=COLORS['bg'])
        algo_frame.pack(pady=3)
        for i, (a, color) in enumerate(algos):
            tk.Radiobutton(
                algo_frame, text=a,
                variable=self.algo_var, value=a,
                bg=COLORS['bg'], fg=color,
                selectcolor='#2a2a4a',
                activebackground=COLORS['bg'],
                font=('Arial', 9, 'bold')
            ).grid(row=i//2, column=i%2, padx=8, pady=2, sticky='w')

        # ── Animation Speed ────────────────────────────
        tk.Label(inner, text='Animation Speed',
                 font=('Arial', 11, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack(pady=(12,2))

        tk.Label(inner,
                 text='Controls how fast cells fill during solving\n'
                      'Fast = quick finish  |  Slow = clearly visible',
                 font=('Arial', 8), bg=COLORS['bg'], fg='#aaaaaa',
                 justify='center').pack()

        spd_frame = tk.Frame(inner, bg=COLORS['bg'])
        spd_frame.pack(pady=3)
        tk.Label(spd_frame, text='Fast', bg=COLORS['bg'],
                 fg='#aaaaaa', font=('Arial', 9)).pack(side='left')
        self.speed_var = tk.IntVar(value=50)
        tk.Scale(
            spd_frame, from_=1, to=100,
            orient='horizontal', variable=self.speed_var,
            bg=COLORS['bg'], fg=COLORS['accent'],
            highlightthickness=0, troughcolor='#2a2a4a', length=130
        ).pack(side='left', padx=3)
        tk.Label(spd_frame, text='Slow', bg=COLORS['bg'],
                 fg='#aaaaaa', font=('Arial', 9)).pack(side='left')

        # ── Separator ──────────────────────────────────
        tk.Frame(inner, height=2, bg=COLORS['accent']).pack(fill='x', padx=10, pady=10)

        # ── Buttons ────────────────────────────────────
        btn_data = [
            ('🎲  Generate Puzzle',    COLORS['btn_blue'],  self.on_generate),
            ('▶   Solve',              COLORS['btn_green'], self._solve_click),
            ('⏹   Stop',              '#555555',            self.on_stop),
            ('📊  Compare All Algos', COLORS['btn_gold'],  self.on_compare),
            ('⚔️   Adversarial Race',  COLORS['btn_purp'],  self.on_adversarial),
        ]
        for text, color, cmd in btn_data:
            tk.Button(
                inner, text=text, command=cmd,
                bg=color, fg='white',
                font=('Arial', 11, 'bold'),
                relief='flat', cursor='hand2', pady=7
            ).pack(fill='x', padx=15, pady=3)

        # ── Status ─────────────────────────────────────
        tk.Frame(inner, height=2, bg='#2a2a4a').pack(fill='x', padx=10, pady=8)

        tk.Label(inner, text='Status',
                 font=('Arial', 11, 'bold'),
                 bg=COLORS['bg'], fg=COLORS['text']).pack()

        self.status_var = tk.StringVar(value='Ready')
        tk.Label(inner, textvariable=self.status_var,
                 font=('Arial', 10), bg=COLORS['bg'],
                 fg=COLORS['accent'], wraplength=220).pack(pady=3)

        # ── Metrics box ────────────────────────────────
        mf = tk.Frame(inner, bg='#16213e', relief='ridge', bd=2)
        mf.pack(fill='x', padx=10, pady=8)

        tk.Label(mf, text='Last Run Metrics',
                 font=('Arial', 10, 'bold'),
                 bg='#16213e', fg=COLORS['accent']).pack(pady=4)

        self.time_var   = tk.StringVar(value='Time:       --')
        self.states_var = tk.StringVar(value='States:     --')
        self.backs_var  = tk.StringVar(value='Backtracks: --')

        for var in [self.time_var, self.states_var, self.backs_var]:
            tk.Label(mf, textvariable=var,
                     font=('Courier', 9),
                     bg='#16213e', fg='#ffffff').pack(anchor='w', padx=8)

        tk.Frame(mf, height=5, bg='#16213e').pack()

    def _solve_click(self):
        self.on_solve(self.algo_var.get(), self.speed_var.get())

    def set_status(self, msg, color='#00d4ff'):
        self.status_var.set(msg)

    def set_metrics(self, time_s, states, backtracks):
        self.time_var.set(  f'Time:       {time_s}s')
        self.states_var.set(f'States:     {states}')
        self.backs_var.set( f'Backtracks: {backtracks}')

    def get_difficulty(self):
        return self.difficulty_var.get()