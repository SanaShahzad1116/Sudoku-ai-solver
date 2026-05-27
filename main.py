
import tkinter as tk
from tkinter import ttk
from gui.app import SudokuApp

root = tk.Tk()
root.title("AI Powered Sudoku Solver")
root.geometry("1500x950")
root.minsize(1300, 850)
root.configure(bg="#121212")

# Canvas setup
canvas = tk.Canvas(root, bg="#121212")
canvas.pack(side="left", fill="both", expand=True)

frame = ttk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_configure)

# Bind mouse wheel / touchpad scroll
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Windows + Linux
canvas.bind_all("<MouseWheel>", _on_mousewheel)
# MacOS touchpad
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

# Put SudokuApp inside frame
app = SudokuApp(frame)

root.mainloop()


# from gui.app import SudokuApp

# if __name__ == "__main__":
#     app = SudokuApp()
#     app.mainloop()