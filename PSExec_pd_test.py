import subprocess
import pandas as pd
import numpy as np
import glob
import os
import time
import threading
import keyboard


# Data Frame
feature_names =["Timestamp","CUDA","Memory","Encoder","Decoder"]
df = pd.DataFrame(columns=feature_names) 

# PSExex Path
psexec_path = r'"C:\Windows\System32\PsExec.exe"'

# Set the remote computer's name or IP address and the command to execute
remote_computer = '10.82.1.15'
command2 = r'cmd /c "nvidia-smi -q"'

# Use subprocess to execute the PSExec command

psexec_cmd = f'{psexec_path} \\\\{remote_computer} {command2}'

#
stop_event = threading.Event()

def print_GPU_Every_Second():
    global df
    start_time  = time.time()
    while True and not stop_event.is_set():

        result = subprocess.check_output(psexec_cmd)

        Output = result.decode('utf-8')
        Output_List = Output.split()

        Timestamp_idx = Output_List.index("Timestamp")
        Utilization_idx = Output_List.index("Utilization")

        Timestamp_List = Output_List[Timestamp_idx+5:Timestamp_idx+6]
        Timestamp = " ".join(Timestamp_List)
        cuda = Output_List[Utilization_idx+1:Utilization_idx+5:2]
        Memory = Output_List[Utilization_idx+5:Utilization_idx+9:2]
        Encoder = Output_List[Utilization_idx+9:Utilization_idx+13:2]
        Decoder = Output_List[Utilization_idx+13:Utilization_idx+17:2]

        data = [{'Timestamp':Timestamp, 'CUDA':cuda[-1],'Memory':Memory[-1],'Encoder':Encoder[-1],'Decoder':Decoder[-1]}]
        df2 = pd.DataFrame(data = data, columns=feature_names)
      
        df = df.append(df2,ignore_index = True)
       
        time.sleep(1)

    if stop_event.is_set():
        print("Exiting print_message()...")
    else:
        print("print_message() finished successfully.")
  
# Start the function in a separate thread
print_thread = threading.Thread(target=print_GPU_Every_Second)
print_thread.start()

# Wait for the user to press the "q" key to stop the loop
keyboard.add_hotkey('esc', lambda: stop_event.set())

while print_thread.is_alive():
    time.sleep(1)

# Wait for the thread to finish
print_thread.join()
print(df)  