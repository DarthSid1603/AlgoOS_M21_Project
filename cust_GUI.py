import utilities
import pandas as pd
import utilities
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import psutil
import datetime as dt
import matplotlib.animation as animation
import collections
import numpy as np

def animate(i, cpu, ram, ax, ax1):

    # get data
    cpu.popleft()
    cpu.append(psutil.cpu_percent())
    # cpu = cpu[-20:] 
    ram.popleft()
    ram.append(psutil.virtual_memory().percent)    
    # ram = ram[-20:] 
    
    # clear axis
    ax.cla()
    ax1.cla()    
    
    # plot cpu
    ax.plot(cpu)
    ax.scatter(len(cpu)-1, cpu[-1])
    ax.text(len(cpu)-1, cpu[-1]+2, "{}%".format(cpu[-1]))
    ax.set_ylim(0,100)    
    ax.grid()
    
    # plot memory
    ax1.plot(ram)
    ax1.scatter(len(ram)-1, ram[-1])
    ax1.text(len(ram)-1, ram[-1]+2, "{}%".format(ram[-1]))
    ax1.set_ylim(0,100)
    ax1.grid()


class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Processes(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        process_infos = utilities.info_of_process()
        df = pd.DataFrame(process_infos)
        cust_cols = ["pid","name","cpu_usage_percent","status","Memory_Used","Wait_Bound","Power_Consumption(in uJ)"]
        df = df[cust_cols]
        
        label = tk.Label(self, text="My Label")
        label.grid(row=0, column=0, padx=2, sticky=tk.NW)

        frame1 = tk.Frame(self)
        frame1.grid(row=1, column=0, sticky=tk.NW)

        canvas1 = tk.Canvas(frame1)
        canvas1.grid(row=0, column=0)

        # Headers in canvas1
        for i in range(df.shape[1]):
            label = tk.Label(canvas1, padx=7, pady=7, borderwidth=1, relief=tk.SOLID, width=10, height=2, text=df.columns[i])
            label.grid(row=0, column=i, sticky='news')

        # Create a frame for the canvas2 and scrollbars
        frame2 = tk.Frame(self)
        frame2.grid(row=2, column=0, sticky=tk.NW)

        # Add a canvas2 in that frame
        canvas2 = tk.Canvas(frame2)
        canvas2.grid(row=0, column=0)

        # Create a vertical scrollbar linked to canvas2
        vsbar = tk.Scrollbar(frame2, orient=tk.VERTICAL, command=canvas2.yview)
        vsbar.grid(row=0, column=1, sticky=tk.NS)
        canvas2.configure(yscrollcommand=vsbar.set)

        # Create a horizontal scrollbar linked to canvas2
        hsbar = tk.Scrollbar(frame2, orient=tk.HORIZONTAL, command=canvas2.xview)
        hsbar.grid(row=1, column=0, sticky=tk.EW)
        canvas2.configure(xscrollcommand=hsbar.set)

        # Create a frame on canvas2 to contain the labels
        labels_frame = tk.Frame(canvas2)

        # Add the labels to this frame
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                label = tk.Label(labels_frame, padx=7, pady=7, borderwidth=1, relief=tk.SOLID, width=10, height=2, text=df.iloc[i, j])
                label.grid(row=i, column=j, sticky='news')

        # Create canvas2 window to hold the label_frame
        canvas2.create_window((0,0), window=labels_frame, anchor=tk.NW)

        labels_frame.update_idletasks()  # Needed to make bbox info available
        bbox = canvas2.bbox(tk.ALL)  # Get bounding box of canvas2
        w, h = bbox[2]-bbox[1], bbox[3]-bbox[1]
        canvas2.configure(scrollregion=bbox, width=min(800, w), height=min(400, h))




class CPU_Usage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        y = []
        fig = Figure(figsize = (7, 6), dpi = 100)
        plot1 = fig.add_subplot(121)
        plot2 = fig.add_subplot(122)


        # cpu = []
        # ram = []

        cpu = collections.deque(np.zeros(20))
        ram = collections.deque(np.zeros(20))

        # plotting the graph

        
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, self)  
        ani = animation.FuncAnimation(fig, animate, fargs=(cpu, ram, plot1, plot2), interval=1000)
        canvas.draw()
    
        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()
            

class Page3(Page):
   def __init__(self, *args, **kwargs):
       Page.__init__(self, *args, **kwargs)
       label = tk.Label(self, text="This is page 3")
       label.pack(side="top", fill="both", expand=True)

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Processes(self)
        p2 = CPU_Usage(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Processes", command=p1.show)
        b2 = tk.Button(buttonframe, text="CPU Details", command=p2.show)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()

