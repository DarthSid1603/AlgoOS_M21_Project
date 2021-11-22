import utilities
import pandas as pd
import utilities
import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import psutil
import datetime as dt
import matplotlib.animation as animation
import collections
import numpy as np
import os
import distro
import shutil
import platform
import subprocess as sp


# Defining Main Page
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

# Tab 1 : Processes
class Processes(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        Processes.render(self)
        Processes.kill_button(self)
        Processes.refresh_button(self)

    # Refresh Button Implementation
    def refresh_button(self):
        frame3 = tk.Frame(self)

        label3 = tk.Label(frame3, text = "")
        label3.pack()
        frame3.grid(row = 3, column=0, padx=2, sticky=tk.NW)
        refresh_Button = tk.Button(frame3,
                        text = "Refresh", 
                        command = lambda: Processes.render(self),
                        bg = "blue",
                        fg = "white")
        refresh_Button.pack(side = "left")

    # Message Box For Killing Process
    def messageconfirm(self, inputtxt):
        answer_message = tk.messagebox.askyesno(title='Confirmation', message='Are you sure you want to kill the process?')

        if answer_message:
            Processes.kill_proc(self, inputtxt)
        else:
            tk.messagebox.showinfo('Return','You will now be returned to the application window.')
            inputtxt.delete(1.0,tk.END)
            Processes.render(self)

    # Process Killing
    def kill_proc(self, inputtxt):
        inp = inputtxt.get(1.0, tk.END)
        kill_pid = int(inp)
        try:
            if psutil.pid_exists(kill_pid):
                proc = psutil.Process(kill_pid)
                proc.kill()
                inputtxt.delete(1.0,tk.END)
                tk.messagebox.showinfo("Success","The Process with given PID has been successfully terminated.")
                Processes.render(self)
            else:
                tk.messagebox.showwarning("Warning", "The Process with the given PID does not exist.")
        except psutil.AccessDenied:
            tk.messagebox.showwarning("Warning", "Important System Process, cannot be terminated.")

    # Kill Process Button Implementation
    def kill_button(self):
        frame2 = tk.Frame(self)

        label5 = tk.Label(frame2, text = "")
        label5.pack()
        inputtxt = tk.Text(frame2,
                   height = 1,
                   width = 15)
        inputtxt.pack(side = "right")

        frame2.grid(row = 3, column=0, padx=2, sticky=tk.SE)
        kill_Button = tk.Button(frame2,
                        text = "Kill", 
                        command = lambda: Processes.messageconfirm(self, inputtxt),
                        bg = "red",
                        fg = "white")
        kill_Button.pack()

    # Table Showing all process and refresh the database    
    def render(self,sortby="pid",order = True):
        process_infos = utilities.info_of_process()
        df = pd.DataFrame(process_infos)
        cust_cols = ["pid","name","cpu_usage_percent","status","Memory_Used","Wait_Bound","Power_Consumption(in uJ)"]
        df = df[cust_cols]

        user_name = (sp.run(["whoami"], stdout= sp.PIPE))
        user = str(user_name.stdout)
        user = user[2:-3]
        
        coms_util = sp.run(['ps', '-o', 'pid', '-u', user], stdout=sp.PIPE)
        coms_temp = str(coms_util.stdout.decode("utf-8"))
        coms = []
        for x in coms_temp.split():
            if x.isdigit():
                coms.append(int(x))
        
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
                 
# Tab 2 : CPU Usage
class CPU_Usage(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text=" ")
        label.pack(side="top", fill="both")

        # Graph definition        
        fig = plt.figure(figsize = (7, 5), dpi = 100)
        plot1 = fig.add_subplot(121)
        plot2 = fig.add_subplot(122)

        cpu = collections.deque(np.zeros(25))
        ram = collections.deque(np.zeros(25))

        canvas = FigureCanvasTkAgg(fig, self)  
        ani = animation.FuncAnimation(fig, utilities.animate, fargs=(cpu, ram, plot1, plot2), interval=1000)
        canvas.draw()
       
        # Placing canvas on the Main window
        canvas.get_tk_widget().pack()
            
# Tab 3 : System Summary : 
class SystemSummary(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        SystemSummary.render(self)

    def render(self):
        label = tk.Label(self, text=" ")
        label.pack(side="top", fill="both")
        frg_color = "gray40"
        
        # Images 
        self.llogo = tk.PhotoImage(file="../icon/image.png")
        lab_logo = tk.Label(self, image=self.llogo)
        lab_logo.pack(side="left", anchor="nw")
        
        
        frame_grid = tk.Frame(self)
        mem = psutil.virtual_memory()
        mswap = psutil.swap_memory()
        PSUTIL_V = psutil.version_info
        frame_grid.pack(side="left", anchor="n")
        
        create_space = tk.Label(frame_grid, text="").grid(column=0, row=0)
        
        # OS DETAILS
        # Username Details
        uname_list = os.uname()
        lab_un = tk.Label(frame_grid, text="User Name  ", foreground=frg_color).grid(column=0, row=1, sticky="NE")
        u_username = psutil.Process().username()
        lab_un2 = tk.Label(frame_grid, text=u_username).grid(column=1, row=1, sticky="NW")
        
        # Node name
        lab_netnm = tk.Label(frame_grid, text="Node Name  ", foreground=frg_color).grid(column=0, row=2, sticky="NE")
        lab_netnm2 = tk.Label(frame_grid, text=uname_list.nodename).grid(column=1, row=2, sticky="NW")

        # Distribution
        lab_distronm = tk.Label(frame_grid, text="Distribution  ", foreground=frg_color).grid(column=0, row=3, sticky="NE")
        distri = distro.linux_distribution()
        lab_distronm2 = tk.Label(frame_grid, text=(distri or "None")).grid(column=1, row=3, sticky="NW")
        
        # Kernel Version
        lab_kernel = tk.Label(frame_grid, text="Kernel Version  ", foreground=frg_color).grid(column=0, row=4, sticky="NE")
        kernel_release = uname_list.release
        lab_kernel2 = tk.Label(frame_grid, text=kernel_release).grid(column=1, row=4, sticky="NW")
        
        # desktop
        lab_desktop = tk.Label(frame_grid, text="Desktop Environment  ", foreground=frg_color).grid(column=0, row=5, sticky="NE")
        u_dmname = os.environ['XDG_CURRENT_DESKTOP']
        lab_desktop2 = tk.Label(frame_grid, text=u_dmname).grid(column=1, row=5, sticky="NW")

        # Architecture
        arch = tk.Label(frame_grid, text="Hardware Architecture  ", foreground=frg_color).grid(column=0, row=6, sticky="NE")
        arch2 = tk.Label(frame_grid, text=uname_list.machine).grid(column=1, row=6, sticky="NW")
        
        # CPU
        lab_cpu = tk.Label(frame_grid, text="CPU  ", foreground=frg_color).grid(column=0, row=7, sticky="NE")
        
        totalCores = psutil.cpu_count()
        physicalCores = psutil.cpu_count(logical=False)
        modelName = ""
        model = ""
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line.rstrip('\n').startswith('model name'):
                    modelName = line.rstrip('\n').split(':')[1].strip()
                    break
            f.close()
        except:
            modelName("#")
        if physicalCores == totalCores:
            model = modelName+" x "+str(physicalCores)
        else:
            model = modelName+" x ("+str(physicalCores)+"+"+str(totalCores)+")"
        lab_processor2 = tk.Label(frame_grid, text=model).grid(column=1, row=7, sticky="NW")

        # GPU
        lab_gpu = tk.Label(frame_grid, text="GPU  ", foreground=frg_color).grid(column=0, row=8, sticky="NE")
        
        gpu_name = "#"
        try:
            if shutil.which("nvidia-smi"):
                gpu_name = sp.check_output("nvidia-smi --query-gpu=gpu_name --format=csv,noheader",shell=True).decode().strip()
            else:
                gpu_name = sp.check_output('lspci | grep VGA | cut -d ":" -f3', shell=True).decode().strip()
        except:
            pass
        lab_gpu2 = tk.Label(frame_grid, text=gpu_name).grid(column=1, row=8, sticky="NW")

        # RAM
        lab_inst_mem = tk.Label(frame_grid, text="RAM  ", foreground=frg_color).grid(column=0, row=9, sticky="NE")
        lab_inst_mem2 = tk.Label(frame_grid, text=utilities.pretty_print(mem.total)).grid(column=1, row=9, sticky="NW")
        
        # Swap Memory
        lab_swap = tk.Label(frame_grid, text="Swap Memory ", foreground=frg_color).grid(column=0, row=10, sticky="NE")
        
        u_swapmem = 0
        try:
            u_swapmem = mswap.total
            if u_swapmem == None:
                u_swapmem = 0
        except:
            u_swapmem = 0
        
        lab_swap2 = tk.Label(frame_grid, text=utilities.pretty_print(u_swapmem)).grid(column=1, row=10, sticky="NW")
        
        # root or home disk size
        # partitions
        partitions = psutil.disk_partitions(all=False)
        num_partitions = len(partitions)
        # check the moutpoint
        home_partition = ""
        for i in range(num_partitions):
            if partitions[i].mountpoint == "/":
                root_partition = partitions[i].device
                root_fstype = partitions[i].fstype
                root_disk_usage = psutil.disk_usage('/')
                root_disk_total = utilities.pretty_print(root_disk_usage.total)
            if partitions[i].mountpoint == "/home":
                home_partition = partitions[i].device
                home_fstype = partitions[i].fstype
                home_disk_usage = psutil.disk_usage('/home')
                home_disk_total = utilities.pretty_print(home_disk_usage.total)
        # root disk size
        lab_root_disk_size = tk.Label(frame_grid, text="Disk Size  ", foreground=frg_color).grid(column=0, row=11, sticky="NE")
        lab_root_disk_size2 = tk.Label(frame_grid, text=root_disk_total).grid(column=1, row=11, sticky="NW")
        # root device and type
        lab_root_disk_type = tk.Label(frame_grid, text="Root Device and Type  ", foreground=frg_color).grid(column=0, row=12, sticky="NE")
        root_dev_type = root_partition + " - " + root_fstype
        lab_root_disk_type2 = tk.Label(frame_grid, text=root_dev_type).grid(column=1, row=12, sticky="NW")
        
        # if the home partition is present
        if home_partition != "":
            # home disk size
            lab_home_disk_size = tk.Label(frame_grid, text="Home Size  ", foreground=frg_color).grid(column=0, row=13, sticky="NE")
            lab_home_disk_size2 = tk.Label(frame_grid, text=home_disk_total).grid(column=1, row=13, sticky="NW")
        
            # home device and type
            lab_home_disk_type = tk.Label(frame_grid, text="Home Device and Type  ", foreground=frg_color).grid(column=0, row=14, sticky="NE")
            home_dev_type = home_partition + " - " + home_fstype
            lab_home_disk_type2 = tk.Label(frame_grid, text=root_dev_type).grid(column=1, row=14, sticky="NW")
        
        # Battery 
        battery = psutil.sensors_battery()
        if battery != None:
            lab_battery = tk.Label(frame_grid, text="Battery  ", foreground=frg_color).grid(column=0, row=15, sticky="NE")
            label12 = str(int(battery.percent))+"% "
            lab_battery2 = tk.Label(frame_grid, text=label12).grid(column=1, row=15, sticky="NW")

# Tab 4 : Memory and Network Details
class MemoryAndNetwork(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        MemoryAndNetwork.render(self)
        
    def render(self):
        label = tk.Label(self, text=" ")
        label.pack(side="top", fill="both")
        frg_color = "gray40"    
        self.llogo = tk.PhotoImage(file="../icon/page4.png")
        lab_logo = tk.Label(self, image=self.llogo)
        lab_logo.pack(side="left", anchor="nw")
        uname_list = os.uname()
        mem = psutil.virtual_memory()
        PSUTIL_V = psutil.version_info
        
        frame1 = tk.Frame(self)
        frame1.pack(side="left", anchor="n")
        lab_memory = tk.Label(frame1, text="\n Memory").grid(column=0, row=0, sticky="NW")
        # installed memory
        lab_inst_memory = tk.Label(frame1, text="RAM  ", foreground=frg_color).grid(column=1, row=1, sticky="NE")
        inst_mem = utilities.pretty_print(mem.total)
        lab_inst_memory2 = tk.Label(frame1, text=inst_mem).grid(column=2, row=1, sticky="NW")
        # memory available
        lab_avail_memory = tk.Label(frame1, text="Available Memory  ", foreground=frg_color).grid(column=1, row=2, sticky="NE")
        avail_mem = utilities.pretty_print(mem.available)
        lab_avail_memory2 = tk.Label(frame1, text=avail_mem).grid(column=2, row=2, sticky="NW")
        # used memory
        lab_used_memory = tk.Label(frame1, text="Used Memory  ", foreground=frg_color).grid(column=1, row=3, sticky="NE")
        used_mem = utilities.pretty_print(mem.used)
        lab_used_memory2 = tk.Label(frame1, text=used_mem).grid(column=2, row=3, sticky="NW")
        # freee memory
        lab_free_memory = tk.Label(frame1, text="Free Memory  ", foreground=frg_color).grid(column=1, row=4, sticky="NE")
        free_mem = utilities.pretty_print(mem.free)
        lab_free_memory2 = tk.Label(frame1, text=free_mem).grid(column=2, row=4, sticky="NW")
        # buffer/cache
        lab_buff_memory = tk.Label(frame1, text="Buff/Cached Memory  ", foreground=frg_color).grid(column=1, row=5, sticky="NE")
        buff_mem = utilities.pretty_print(mem.buffers+mem.cached)
        lab_buff_memory2 = tk.Label(frame1, text=buff_mem).grid(column=2, row=5, sticky="NW")
        # shared memory
        lab_shared_memory = tk.Label(frame1, text="Shared Memory  ", foreground=frg_color).grid(column=1, row=6, sticky="NE")
        shared_mem = utilities.pretty_print(mem.shared)
        lab_shared_memory2 = tk.Label(frame1, text=shared_mem).grid(column=2, row=6, sticky="NW")
        
        ## Swap
        mswap = psutil.swap_memory()
        tnet = psutil.net_io_counters()
        u_swapmem = 0
        try:
            u_swapmem = mswap.total
            if u_swapmem == None:
                u_swapmem = 0
        except:
            u_swapmem = 0
        lab_swap = tk.Label(frame1, text="\n Swap").grid(column=0, row=7, sticky="NW")
        # total
        lab_total_swap = tk.Label(frame1, text="Total  ", foreground=frg_color).grid(column=1, row=8, sticky="NE")
        total_swap = utilities.pretty_print(mswap.total) or ""
        lab_total_swap2 = tk.Label(frame1, text=total_swap).grid(column=2, row=8, sticky="NW")
        # used - if it exists
        if u_swapmem > 0:          
            lab_free_swap = tk.Label(frame1, text="Free  ", foreground=frg_color).grid(column=1, row=9, sticky="NE")
            free_swap = utilities.pretty_print(mswap.free)
            lab_free_swap2 = tk.Label(frame1, text=free_swap).grid(column=2, row=9, sticky="NW")

            lab_used_swap = tk.Label(frame1, text="Used  ", foreground=frg_color).grid(column=1, row=10, sticky="NE")
            used_swap = utilities.pretty_print(mswap.used)+" ("+str(mswap.percent)+"%)"
            lab_used_swap2 = tk.Label(frame1, text=used_swap).grid(column=2, row=10, sticky="NW")

            
        
        ## net
        lab_net = tk.Label(frame1, text="\n Net").grid(column=0, row=10, sticky="NW")
        # bytes/packets received
        lab_bytes_recv = tk.Label(frame1, text="bytes/packets received  ", foreground=frg_color).grid(column=1, row=12, sticky="NE")
        bytes_recv = str(utilities.pretty_print(tnet.bytes_recv))+" - "+str(tnet.packets_recv)
        lab_bytes_recv2 = tk.Label(frame1, text=bytes_recv).grid(column=2, row=12, sticky="NW")
        # bytes/packets sent
        lab_bytes_sent = tk.Label(frame1, text="bytes/packets sent  ", foreground=frg_color).grid(column=1, row=13, sticky="NE")
        bytes_sent = str(utilities.pretty_print(tnet.bytes_sent))+" - "+str(tnet.packets_sent)
        lab_bytes_sent2 = tk.Label(frame1, text=bytes_sent).grid(column=2, row=13, sticky="NW")
        

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Processes(self)
        p2 = CPU_Usage(self)
        p3 = SystemSummary(self)
        p4 = MemoryAndNetwork(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Processes", command=p1.show)
        b2 = tk.Button(buttonframe, text="CPU Details", command=p2.show)
        b3 = tk.Button(buttonframe, text="System Summary", command=p3.show)
        b4 = tk.Button(buttonframe, text="Memory and Network", command=p4.show)


        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        p1.show()