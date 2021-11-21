import numpy as np
import pandas as pd
import os
import time
import psutil as pu
from datetime import datetime
import matplotlib.animation as animation
from matplotlib import pyplot as plt
import pyRAPL
pyRAPL.setup() 

def info_of_process():
    #Empty list to store all process data 
    process_infos = []
    
    for proc in pu.process_iter():
        proc_info = dict()
        #Suggested in documentation to speed up working
        
        meter = pyRAPL.Measurement('bar')
        meter.begin()
        
        with proc.oneshot():
            process_id = -100
            if proc.pid == 0:
                continue
            else:
                process_id = proc.pid
                
            proc_info["pid"] = process_id
            proc_info["ppid"] = proc.ppid()
            proc_info["name"] = proc.name()
            proc_info["cpu_usage_percent"] = proc.cpu_percent()
            proc_info["status"] = proc.status()
            proc_info["number_of_threads"] = proc.num_threads()
            
            try:
                time_of_create = proc.create_time()
                time_create = datetime.fromtimestamp(time_of_create)
            except OSError:
                time_of_create = pu.boot_time()
                time_create = datetime.fromtimestamp(time_of_create)
                
            try:
                cores = len(proc.cpu_affinity())
            except pu.AccessDenied:
                cores = 0
            
            try:
                nice_priority = int(proc.nice())
            except pu.AccessDenied:
                nice_priority = 0
                
            try:
                memory_usage = proc.memory_full_info().uss
            except pu.AccessDenied:
                memory_usage = 0
                
            try:
                username = proc.username()
            except pu.AccessDenied:
                username = "Not run at Sudo"
                
            wait_cat = ''
            if proc.status() == 'idle':
                if proc.cpu_times().iowait > 0.0:
                    wait_cat = 'I/O_WAIT'
                else:
                    wait_cat = 'CPU_WAIT'
            else:
                wait_cat = 'N/A'
                
            proc_info["creation_time"] = time_create
            proc_info["Cores_of_CPU"] = cores
            proc_info["Nice_Priority"] = nice_priority
            proc_info["Memory_Used"] = memory_usage
            proc_info["UserName"] = username
            proc_info["Wait_Bound"] = wait_cat
            meter.end()
            proc_info["Power_Consumption(in uJ)"] = meter.result.dram
            
        
        process_infos.append(proc_info)
        
    return process_infos


def pretty_print(mem):
    for start in ['', 'K', 'M', 'G', 'T', 'P']:
        if mem < 1024:
            return f"{mem:.2f}{start}B"
        mem /= 1024


def animate(i, cpu, ram, ax, ax1):

    # clear axis
    ax.clear()
    ax1.clear()

    # get data
    cpu.popleft()
    cpu.append(pu.cpu_percent())
    ram.popleft()
    ram.append(pu.virtual_memory().percent)    

    x_len = len(cpu)-1
    
    
    # plot cpu
    ax.plot(cpu)
    ax.title.set_text("CPU Usage")
    ax.scatter(x_len, cpu[-1])
    ax.text(x_len-.5, cpu[-1]+2, "{}%".format(cpu[-1]))
    ax.set_ylim(0,100)    
    ax.set_xticks([])
    ax.grid()
    
    # plot memory
    ax1.plot(ram)
    ax1.title.set_text("RAM Usage")
    ax1.scatter(x_len, ram[-1])
    ax1.text(x_len-.5, ram[-1]+2, "{}%".format(ram[-1]))
    ax1.set_ylim(0,100)
    ax1.set_xticks([])
    ax1.grid()
