import numpy as np
import pandas as pd
import os
import time
import psutil as pu
from datetime import datetime
import pyRAPL
def info_of_process():
    #Empty list to store all process data 
    process_infos = []
    
    for proc in pu.process_iter():
        proc_info = dict()
        #Suggested in documentation to speed up working
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
            except psutil.AccessDenied:
                username = "Not run at Sudo"
                
            proc_info["creation_time"] = time_create
            proc_info["Cores_of_CPU"] = cores
            proc_info["Nice_Priority"] = nice_priority
            proc_info["Memory_Used"] = memory_usage
            proc_info["UserName"] = username
        
        process_infos.append(proc_info)
        
    return process_infos