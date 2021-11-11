import utilities
import pandas as pd
import cust_GUI as GUI
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()
    main = GUI.MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.wm_geometry("800x800+400+100")
    root.mainloop()