import json
import plotly.io as pio
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots
from plotly.validators.scatter.marker import SymbolsrcValidator


import matplotlib as mpl
import matplotlib.pylab as plt

import pandas as pd
import numpy as np
import glob
import os

# df =pd.read_csv(r"C:\Users\4Dreplay\Documents\4DREPLAY\Coding\SSH_connect\2023-03-23\10.82.1.15\GPU_Data_14_58_50.csv")
# print (df)

# x = input("입력 : ")
# print(x)

feature_names =["IP","Timestamp","GPU","GPU_Memory","Encoder","Decoder"]
df2 = pd.DataFrame(columns=feature_names) 

path = r'.\Data\2023-03-30'

os.chdir(path)
for i in glob.glob('*csv'):
   df3 = pd.read_csv(i)
   df2 = df2.append(df3,ignore_index = True)


# print(df2)
IP_LIST =[]
IP_1 = df2[df2['IP']=='10.82.1.14']
IP_2 = df2[df2['IP']=='10.82.1.15']

IP_LIST.append(IP_1)
IP_LIST.append(IP_2)
print(IP_1)
# fig = go.Figure()

for df in IP_LIST:
   
   fig = make_subplots(rows=2,cols=2 ,
                     subplot_titles=('CUDA', 'GPU_Memory','Encoder', 'Decoder')
                        )

   fig.add_trace(go.Scatter(x = df['Timestamp'] , y = df['GPU']
                  ,mode = 'lines'
                  ,name='GPU')
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

   # Edit the layout
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
   fig.update_layout(title=f'Usage of GPU_all')


   fig.show()
   fig = px.line(df2 ,x ='Timestamp' , y = 'CUDA'
                    , hover_data= ['Encoder',"Decoder"]
                    ,title="GPU_DATA" )
   fig.show()