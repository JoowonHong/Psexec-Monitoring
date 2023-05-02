import subprocess
import pandas as pd
import numpy as np
import glob
import os
import time
import threading
import keyboard
import matplotlib as mpl
import matplotlib.pylab as plt
import datetime

import json
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolsrcValidator

#주원의 다시 도전 버전
# 깃허브에서 
# vscode 에서
# PSExex Path
psexec_path = r'"C:\Windows\System32\PsExec.exe"'


# Set the remote computer's name or IP address and the command to execute
IP_LIST = []

Client_IP_1 = input('Please input 3rd and 4th IP adress with dot(.)  (10.82.[].[]) (First) :')
# Client_IP_2 = input('Please input 3rd and 4th IP adress with dot(.) (10.82.[].[]) (Last) :')

remote_computer=f'10.82.{Client_IP_1}'
Environment_Variable_Command = r'setx PATH "%PATH%;C:\Program Files\NVIDIA Corporation\NVSMI"'

nvidia_smi_command = 'nvidia-smi -q'
command1 = fr'cmd /c "{nvidia_smi_command}"'
# Use subprocess to execute the PSExec command
psexec_cmd = f'{psexec_path} \\\\{remote_computer} {command1}'




# Set Enviroment PATH 
Environment_PATH_cmd = f'{psexec_path} \\\\{remote_computer} {Environment_Variable_Command}'
ok = subprocess.check_output(Environment_PATH_cmd)
Output = ok.decode('utf-8')
print (Output)




stop_event = threading.Event()
#Start Time
now = datetime.datetime.now()
Date = now.strftime('%Y-%m-%d')
Time = now.strftime('%H_%M_%S')
# Save to csv log
foldername = f'Data/{Date}/{remote_computer}'
os.makedirs(foldername , exist_ok=True)

# Create a file name for the CSV file in the new folder
file_name_time = f'GPU_Data_{Time}.csv'
# file_name_time = 'data.csv'
file_name = os.path.join(foldername,file_name_time)


# Data Frame
feature_names =["Timestamp","CUDA","GPU_Memory","Encoder","Decoder"]
df = pd.DataFrame(columns=feature_names) 

def print_GPU_Every_Second():
    global df
 
    while True and not stop_event.is_set():

        result = subprocess.check_output(psexec_cmd)

        Output = result.decode('utf-8')
        Output_List = Output.split()

        Timestamp_idx = Output_List.index("Timestamp")
        Utilization_idx = Output_List.index("Utilization")

        Timestamp_List = Output_List[Timestamp_idx+5:Timestamp_idx+6]
        Timestamp = " ".join(Timestamp_List)
        cuda = Output_List[Utilization_idx+1:Utilization_idx+5:2]
        GPU_Memory = Output_List[Utilization_idx+5:Utilization_idx+9:2]
        Encoder = Output_List[Utilization_idx+9:Utilization_idx+13:2]
        Decoder = Output_List[Utilization_idx+13:Utilization_idx+17:2]

        data = [{'Timestamp':Timestamp, 
                 'CUDA':int(cuda[-1]),
                 'GPU_Memory':int(GPU_Memory[-1]),
                 'Encoder':int(Encoder[-1]),
                 'Decoder':int(Decoder[-1])}]
        
        df2 = pd.DataFrame(data = data, columns=feature_names)

        df = df.append(df2,ignore_index = True)
        print(df2)
        time.sleep(0.1)

    if stop_event.is_set():
        print("Exiting print_GPU_Every_Second()...")
    else:
        print("print_message() finished successfully.")
  
# Start the function in a separate thread
print_thread = threading.Thread(target=print_GPU_Every_Second)
print_thread.start()

# Wait for the user to press the "q" key to stop the loop
keyboard.add_hotkey('q', lambda: stop_event.set())

while print_thread.is_alive():
    time.sleep(1)

# Wait for the thread to finish
print_thread.join()
  






# Save the DataFrame to a CSV file in the new folder
df.to_csv(file_name, index=False)
print(df)







#Plotly Graph
fig = make_subplots(rows=2,cols=2 ,
                    subplot_titles=('CUDA', 'GPU_Memory','Encoder', 'Decoder'))

fig.add_trace(go.Scatter(x = df['Timestamp'] , y = df['CUDA']
                 ,mode = 'lines'
                 ,name='CUDA')
                 ,row=1,col=1)

fig.add_trace(go.Scatter(x = df['Timestamp'] , y = df['GPU_Memory']
                 ,mode = 'lines'
                 ,name='GPU_Memory')
                 ,row=1,col=2)

fig.add_trace(go.Scatter(x = df['Timestamp'] , y = df['Encoder']
                 ,mode = 'lines'
                 ,name='Encoder')
                 ,row=2,col=1)

fig.add_trace(go.Scatter(x = df['Timestamp'] , y = df['Decoder']
                 ,mode = 'lines'
                 ,name='Decoder')
                 ,row=2,col=2)

# Update xaxis properties
fig.update_xaxes(title_text="Time", row=1, col=1)
fig.update_xaxes(title_text="Time",  row=1, col=2)
fig.update_xaxes(title_text="Time",  row=2, col=1)
fig.update_xaxes(title_text="Time",  row=2, col=2)

# Update yaxis properties
fig.update_yaxes(title_text="Usage Percentage(%)", range=[0, 100],row=1, col=1)
fig.update_yaxes(title_text="Usage Percentage(%)", range=[0, 100],row=1, col=2)
fig.update_yaxes(title_text="Usage Percentage(%)", range=[0, 100],row=2, col=1)
fig.update_yaxes(title_text="Usage Percentage(%)", range=[0, 100],row=2, col=2)

# Edit the layout
fig.update_layout(title=f'Usage of GPU_{remote_computer}')

fig.show()
