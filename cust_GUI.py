import utilities
import pandas as pd
import utilities
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import psutil
import datetime as dt
import matplotlib.animation as animation
import collections
import numpy as np
import subprocess as sp



class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Processes(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        Processes.render(self)
        Processes.kill_button(self)
        Processes.refresh_button(self)

    def refresh_button(self):
        frame3 = tk.Frame(self)

        frame3.grid(row = 3, column=0, padx=2, sticky=tk.NW)
        refresh_Button = tk.Button(frame3,
                        text = "Refresh", 
                        command = lambda: Processes.render(self),
                        bg = "blue",
                        fg = "green")
        refresh_Button.pack(side = "left")

        label3 = tk.Label(frame3, text = "")
        label3.pack()

    def kill_proc(self, inputtxt):
        inp = inputtxt.get(1.0, "end-1c")
        kill_pid = int(inp)
        #print(kill_pid)
        proc = psutil.Process(kill_pid)
        proc.kill()
        inputtxt.delete(1.0,tk.END)
        Processes.render(self)

    def kill_button(self):
        frame2 = tk.Frame(self)

        inputtxt = tk.Text(frame2,
                   height = 2,
                   width = 15)
        inputtxt.pack(side = "right")

        frame2.grid(row = 3, column=0, padx=2, sticky=tk.SE)
        #label4 = tk.Label(frame2, text = "")
        #label4.pack()

        kill_Button = tk.Button(frame2,
                        text = "Kill", 
                        command = lambda: Processes.kill_proc(self, inputtxt),
                        bg = "red",
                        fg = "yellow")
        kill_Button.pack()

        #label2 = tk.Label(frame2, text = "")
        #label2.pack()
        
    def render(self,sortby="pid",order = True):       
       
        process_infos = utilities.info_of_process()
        df = pd.DataFrame(process_infos)
        #df = df.tail()
        cust_cols = ["pid","name","cpu_usage_percent","status","Memory_Used","Wait_Bound","Power_Consumption(in uJ)"]
        df = df[cust_cols]

        user_name = (sp.run(["whoami"], stdout= sp.PIPE))
        user = str(user_name.stdout)
        user = user[2:-3]
        
        coms_util = sp.run(['ps', '-o', 'pid', '-u', user], stdout=sp.PIPE)
        coms_temp = str(coms_util.stdout)
        coms_temp = coms_temp[11:]
        coms_temp = coms_temp.split()
        # print(coms_temp)

        coms = []
        for x in coms_temp:
            coms.append(x[:-2])

        coms[-1] = coms[-1][:-1]
        
        coms = list(map(int,coms))

        # print(coms)

        df = df.loc[df["pid"].isin(coms)]

        df = df.sort_values(by=[sortby], ascending = order)
        label = tk.Label(self, text=" ")
        label.grid(row=0, column=0, padx=2, sticky=tk.NW)
        widths = [5,15,10,11,11,11,20]
        frame1 = tk.Frame(self)
        frame1.grid(row=1, column=0, sticky=tk.NW)
        b1 = tk.Button(frame1, text="pid",command= lambda: Processes.render(self,"pid",(not order)),width = widths[0]-1)
        b2 = tk.Button(frame1, text="name",command=lambda:Processes.render(self,"name",(not order)),width = widths[1]-2)
        b3 = tk.Button(frame1, text="CPU usage %",command=lambda:Processes.render(self,"cpu_usage_percent",(not order)),width = widths[2]-1)
        b4 = tk.Button(frame1, text="status",command=lambda:Processes.render(self,"status",(not order)),width = widths[3]-2)
        b5 = tk.Button(frame1, text="Memory Used",command=lambda:Processes.render(self,"Memory_Used",(not order)),width = widths[4]-1)
        b6 = tk.Button(frame1, text="Wait Bound",command=lambda:Processes.render(self,"Wait_Bound",(not order)),width = widths[5]-2)
        b7 = tk.Button(frame1, text="Power Consumption(in uJ)",command=lambda:Processes.render(self,"Power_Consumption(in uJ)",(not order)),width = widths[6]-2)
        

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")
        b6.pack(side="left")
        b7.pack(side="left")

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
                if(j == 4):
                    label = tk.Label(labels_frame, padx=7, pady=7, borderwidth=1, relief=tk.SOLID, width=widths[j], height=2, text=utilities.pretty_print(df.iloc[i, j]))
                    label.grid(row=i, column=j, sticky='news')
                else:   
                    label = tk.Label(labels_frame, padx=7, pady=7, borderwidth=1, relief=tk.SOLID, width=widths[j], height=2, text=df.iloc[i, j])
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
        
        fig = Figure(figsize = (7, 6), dpi = 100)
        plot1 = fig.add_subplot(121)
        plot2 = fig.add_subplot(122)

        cpu = collections.deque(np.zeros(20))
        ram = collections.deque(np.zeros(20))

        # plotting the graph

        
        # creating the Tkinter canvas
        # containing the Matplotlib figure
        canvas = FigureCanvasTkAgg(fig, self)  
        ani = animation.FuncAnimation(fig, utilities.animate, fargs=(cpu, ram, plot1, plot2), interval=1000)
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

