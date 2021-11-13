import utilities
import pandas as pd
import cust_GUI as GUI
import tkinter as tk


if __name__ == "__main__":
    win = tk.Tk()
    main = GUI.MainView(win)
    main.pack(side="top", fill="both", expand=True)
    win.wm_geometry("800x800+400+100")
    win.mainloop()