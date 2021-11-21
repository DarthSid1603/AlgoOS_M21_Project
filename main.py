import utilities
import pandas as pd
import tkinter as tk
import cust_GUI as GUI

# Main Tab of Task Manager
if __name__ == "__main__":
    win = tk.Tk()
    win.title(string="Task Manager")
    main = GUI.MainView(win)
    main.pack(side="top", fill="both", expand=True)
    win.wm_geometry("800x800+400+100")
    win.mainloop()