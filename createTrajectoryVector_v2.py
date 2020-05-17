# coding: utf-8

# In[1]:

# DELIVERABLE FOR THE PROJECT:
# "MOBILITY KINEMATICS"
# David Pastor-Escuredo
# with LifeD Lab
# Copyright <2018-2019> <David Pastor Escuredo>

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# THIS FILE
# READS TRAJECTORIES

#imports
import pandas as pd
import numpy as np
#from nltk.tokenize import word_tokenize
import re
#import networkx as nx
import matplotlib.pyplot as plt
import datetime
import collections
from sklearn.cluster import KMeans
#import plotly.plotly as py
#import plotly.graph_objs as go
import matplotlib.mlab as mlab
import os
import codecs
#import pymysql
import networkx as nx
import pickle
import csv
import gzip
import json
import time
from datetime import datetime, timedelta, date
from os import listdir
from os.path import isfile, join
from timeit import default_timer as timer

#Create a descriptor vector from the net values of the trajectories
region='_bogota'
doFilter=1

datapath='/home/davidpastor/TEF_mob/'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'
trajdesc=datapath+'traj_net/'

UVD={}
dayRef=14

with open(trajdesc+'UD_v2.cnf', 'rb') as fpp:
    UD=pickle.load(fpp) 
    
with open(netpath+'Net2ref.cnf', 'rb') as fpp:
    G=pickle.load(fpp)
    
for u in UD:
    v=UD[u]['position']
    if len(v)>1:
        if u not in UVD:
            UVD[u]={}
            UVD[u]['d_ind']=[]
            UVD[u]['d_outd']=[]
            UVD[u]['d_in_degree']=[]
            UVD[u]['d_out_degree']=[]
            UVD[u]['d_in_eigenvalue']=[]
            UVD[u]['d_out_eigenvalue']=[] 
            UVD[u]['d_in_betweenness']=[]
            UVD[u]['d_out_betweenness']=[]
            UVD[u]['d_dis_betweenness']=[]
            UVD[u]['d_cfbetweenness']=[]
            UVD[u]['d_in_closeness']=[]
            UVD[u]['d_out_closeness']=[]
            UVD[u]['d_dis_closeness']=[]
            UVD[u]['d_cfcloseness']=[]
            UD[u]['d_in_ave_flow']=[]
            UD[u]['d_out_ave_flow']=[]
            UD[u]['d_in_std_flow']=[]
            UD[u]['d_out_std_flow']=[]
            UD[u]['d_in_ave_distance']=[] 
            UD[u]['d_out_ave_distance']=[] 
            UD[u]['d_in_std_distance']=[] 
            UD[u]['d_out_std_distance']=[] 
            UD[u]['d_in_ave_time']=[] 
            UD[u]['d_out_ave_time']=[] 
            UD[u]['d_in_std_time']=[]
            UD[u]['d_out_std_time']=[]
            
            UVD[u]['d_time']=[]
            UVD[u]['distance']=[]     
            UVD[u]['ratio_time']=[]
            UVD[u]['flow']=[]
            
        for t in range(0,len(v)-1):
            pos=v[t]
            npos=v[t+1]
            if doFilter and (npos is pos):
                continue
            else: 
                UVD[u]['d_ind'].append(UD[u]['ind'][t+1]-UD[u]['ind'][t])
                UVD[u]['d_outd'].append(UD[u]['outd'][t+1]-UD[u]['outd'][t])
                UVD[u]['d_in_degree'].append(UD[u]['in_degree'][t+1]-UD[u]['in_degree'][t])
                UVD[u]['d_out_degree'].append(UD[u]['out_degree'][t+1]-UD[u]['out_degree'][t])
                UVD[u]['d_in_eigenvalue'].append(UD[u]['in_eigenvalue'][t+1]-UD[u]['in_eigenvalue'][t])
                UVD[u]['d_out_eigenvalue'].append(UD[u]['out_eigenvalue'][t+1]-UD[u]['out_eigenvalue'][t])  
                UVD[u]['d_in_betweenness'].append(UD[u]['in_betweenness'][t+1]-UD[u]['in_betweenness'][t])
                UVD[u]['d_out_betweenness'].append(UD[u]['out_betweenness'][t+1]-UD[u]['out_betweenness'][t])
                UVD[u]['d_dis_betweenness'].append(UD[u]['dis_betweenness'][t+1]-UD[u]['dis_betweenness'][t])
                UVD[u]['d_cfbetweenness'].append(UD[u]['cfbetweenness'][t+1]-UD[u]['cfbetweenness'][t])
                UVD[u]['d_in_closeness'].append(UD[u]['in_closeness'][t+1]-UD[u]['in_closeness'][t])
                UVD[u]['d_out_closeness'].append(UD[u]['out_closeness'][t+1]-UD[u]['out_closeness'][t])
                UVD[u]['d_dis_closeness'].append(UD[u]['dis_closeness'][t+1]-UD[u]['dis_closeness'][t])
                UVD[u]['d_cfcloseness'].append(UD[u]['cfcloseness'][t+1]-UD[u]['cfcloseness'][t])
  
                UD[u]['d_in_ave_flow'].append(UD[u]['in_ave_flow'][t+1]-UD[u]['in_ave_flow'][t]) 
                UD[u]['d_out_ave_flow'].append(UD[u]['out_ave_flow'][t+1]-UD[u]['out_ave_flow'][t])
                UD[u]['d_in_std_flow'].append(UD[u]['in_std_flow'][t+1]-UD[u]['in_std_flow'][t]) 
                UD[u]['d_out_std_flow'].append(UD[u]['out_std_flow'][t+1]-UD[u]['out_std_flow'][t]) 
                UD[u]['d_in_ave_distance'].append(UD[u]['in_ave_distance'][t+1]-UD[u]['in_ave_distance'][t]) 
                UD[u]['d_out_ave_distance'].append(UD[u]['out_ave_distance'][t+1]-UD[u]['out_ave_distance'][t]) 
                UD[u]['d_in_std_distance'].append(UD[u]['in_std_distance'][t+1]-UD[u]['in_std_distance'][t]) 
                UD[u]['d_out_std_distance'].append(UD[u]['out_std_distance'][t+1]-UD[u]['out_std_distance'][t]) 
                UD[u]['d_in_ave_time'].append(UD[u]['in_ave_time'][t+1]-UD[u]['in_ave_time'][t]) 
                UD[u]['d_out_ave_time'].append(UD[u]['out_ave_time'][t+1]-UD[u]['out_ave_time'][t]) 
                UD[u]['d_in_std_time'].append(UD[u]['in_std_time'][t+1]-UD[u]['in_std_time'][t]) 
                UD[u]['d_out_std_time'].append(UD[u]['out_std_time'][t+1]-UD[u]['out_std_time'][t])
                
                d_time=UD[u]['time'][t+1]-UD[u]['time'][t]
                UVD[u]['d_time'].append(d_time)
        
            #ns=G.nodes()         
            #if G.has_edge(pos,npos):
                #Descriptors of the vector - edge of the network
            #    UVD[u]['distance'].append(G[pos][npos]['distance'])#distance is fix
            #    UVD[u]['ratio_time'].append(d_time/(G[pos][npos]['time']))#velocity can change
            #    UVD[u]['flow'].append(G[pos][npos]['weight'])
            #else:
            #    UVD[u]['distance'].append(-1)#distance is fix
            #    UVD[u]['ratio_time'].append(-1)#velocity can change
            #    UVD[u]['flow'].append(-1)
   
if doFilter:
    with open(trajdesc+'UVD_v2'+'.cnf', 'wb') as handle:
        pickle.dump(UVD, handle, protocol=pickle.HIGHEST_PROTOCOL)    
else:
    with open(trajdesc+'UVD_v2filtered'+'.cnf', 'wb') as handle:
        pickle.dump(UVD, handle, protocol=pickle.HIGHEST_PROTOCOL) 
    