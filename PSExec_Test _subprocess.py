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


# PSExex Path
psexec_path = r'"C:\Windows\System32\PsExec.exe"'

# Set the remote computer's name or IP address and the command to execute

Client_IP_1 = input('Please input 3rd and 4th IP adress with dot(.) (10.82.[].[]) :')

remote_computer=f'10.82.{Client_IP_1}'
cd = 'cd'
Enviroment_Variable = r'C:\Program Files\NVIDIA Corporation\NVSMI'
nvidia_smi_command = 'nvidia-smi -q'
command  = fr'cmd /c "{Enviroment_Variable}"'
command2 = fr'cmd "{nvidia_smi_command}"'


# Use subprocess to execute the PSExec command

psexec_cmd = f'{psexec_path} \\\\{remote_computer}'
psexec_cmd2 = f'{psexec_path} \\\\{remote_computer} {command}'


# result = subprocess.run(psexec_cmd)
    
p = subprocess.run([f'{psexec_path}\\\{remote_computer}','cmd /c','cd',Enviroment_Variable,nvidia_smi_command],
                     stdout=subprocess.PIPE,)


result_as_string = p.stdout.decode('utf-8')
print(p)
# p = subprocess.Popen(nvidia_smi_command,
#                      stdout=subprocess.PIPE,
#                      stderr=subprocess.STDOUT,
#                      universal_newlines=True)                     
# while p.poll() == None:
# 	out = p.stdout.readline()
	
# 	print(out, end='')