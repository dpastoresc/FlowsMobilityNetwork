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
import math
import time
from datetime import datetime, timedelta, date
from os import listdir
from os.path import isfile, join
from timeit import default_timer as timer

# -> createTrajectoryHome.py
#Create a descriptor vector from the gradient in the trajectory
region='_medellin'
doFilter=1
th=1

datapath='/home/davidpastor/TEF_mob/'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'
trajdesc=datapath+'traj_net/'

UHD={}

with open(trajdesc+'UD_v3'+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
    UD=pickle.load(fpp) 
    
with open(trajpath+'HL.tff', 'rb') as fpp:
    HL=pickle.load(fpp) 
    
with open(netpath+'Net2ref.cnf', 'rb') as fpp:
    G=pickle.load(fpp)
    
with open(netdescpath+'NDref'+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
    GD=pickle.load(fpp)
        
with open(netdescpath+'NDcfref'+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
    GDcf=pickle.load(fpp)    
            
with open(netdescpath+'NDedgeref'+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
    GDedge=pickle.load(fpp)   
   
print('loaded, iterating') 

for u in UD:
    v=UD[u]['position']
    
    if len(v)>0 and u in HL:
        hpos=HL[u]['homeloc']
        if hpos in GD and hpos in GDcf and hpos in GDedge:
            if u not in UHD:
                    UHD[u]={}
                    #UHD[u]['d_ind']=[]
                    #UHD[u]['d_outd']=[]
                    UHD[u]['d_in_degree']=[]
                    UHD[u]['d_out_degree']=[]
                    UHD[u]['d_in_eigenvalue']=[]
                    UHD[u]['d_out_eigenvalue']=[] 
                    UHD[u]['d_in_betweenness']=[]
                    UHD[u]['d_out_betweenness']=[]
                    UHD[u]['d_dis_betweenness']=[]
                    UHD[u]['d_cfbetweenness']=[]
                    UHD[u]['d_in_closeness']=[]
                    UHD[u]['d_out_closeness']=[]
                    UHD[u]['d_dis_closeness']=[]
                    UHD[u]['d_cfcloseness']=[]
                    
                    UHD[u]['d_in_ave_flow']=[]
                    UHD[u]['d_out_ave_flow']=[]
                    UHD[u]['d_in_std_flow']=[]
                    UHD[u]['d_out_std_flow']=[]
                    UHD[u]['d_in_ave_distance']=[] 
                    UHD[u]['d_out_ave_distance']=[] 
                    #UHD[u]['d_in_std_distance']=[] 
                    #UHD[u]['d_out_std_distance']=[] 
                    #UHD[u]['d_in_ave_time']=[] 
                    #UHD[u]['d_out_ave_time']=[] 
                    #UHD[u]['d_in_std_time']=[]
                    #UHD[u]['d_out_std_time']=[]
                    
                    #UVD[u]['d_time']=[]
                    UHD[u]['distance']=[]
                    #UVD[u]['ratio_time']=[]
                    UHD[u]['flow']=[]
                    
            for t in range(0,len(v)):
                
                pos=v[t]
                if doFilter and (pos is hpos):
                    continue
                
                x1=UD[u]['in_degree'][t]
                if math.isnan(x1):
                    continue
              
                pos=UD[u]['position'][t]
                #UHD[u]['d_ind'].append(UD[u]['ind'][t]-GD[hpos]['ind'])
                #UHD[u]['d_outd'].append(UD[u]['outd'][t]-GD[hpos]['outd'])
                UHD[u]['d_in_degree'].append(UD[u]['in_degree'][t]-GD[hpos]['in_degree'])
                UHD[u]['d_out_degree'].append(UD[u]['out_degree'][t]-GD[hpos]['out_degree'])
                UHD[u]['d_in_eigenvalue'].append(UD[u]['in_eigenvalue'][t]-GD[hpos]['in_eigenvalue'])
                UHD[u]['d_out_eigenvalue'].append(UD[u]['out_eigenvalue'][t]-GD[hpos]['out_eigenvalue'])
                UHD[u]['d_in_betweenness'].append(UD[u]['in_betweenness'][t]-GD[hpos]['in_betweenness'])
                UHD[u]['d_out_betweenness'].append(UD[u]['out_betweenness'][t]-GD[hpos]['out_betweenness'])
                UHD[u]['d_dis_betweenness'].append(UD[u]['dis_betweenness'][t]-GD[hpos]['dis_betweenness'])
                UHD[u]['d_cfbetweenness'].append(UD[u]['cfbetweenness'][t]-GDcf[hpos]['cfbetweenness'])
                UHD[u]['d_in_closeness'].append(UD[u]['in_closeness'][t]-GD[hpos]['in_closeness'])
                UHD[u]['d_out_closeness'].append(UD[u]['out_closeness'][t]-GD[hpos]['out_closeness'])
                UHD[u]['d_dis_closeness'].append(UD[u]['dis_closeness'][t]-GD[hpos]['dis_closeness'])
                UHD[u]['d_cfcloseness'].append(UD[u]['cfcloseness'][t]-GDcf[hpos]['cfcloseness'])
                #VD[u]['d_time']=UD[u]['time'][t]-GD[hpos]['out_degree']
                UHD[u]['d_in_ave_flow'].append(UD[u]['in_ave_flow'][t]-GDedge[hpos]['in_ave_flow']) 
                UHD[u]['d_out_ave_flow'].append(UD[u]['out_ave_flow'][t]-GDedge[hpos]['out_ave_flow'])
                UHD[u]['d_in_std_flow'].append(UD[u]['in_std_flow'][t]-GDedge[hpos]['in_std_flow']) 
                UHD[u]['d_out_std_flow'].append(UD[u]['out_std_flow'][t]-GDedge[hpos]['out_std_flow']) 
                UHD[u]['d_in_ave_distance'].append(UD[u]['in_ave_distance'][t]-GDedge[hpos]['in_ave_distance']) 
                UHD[u]['d_out_ave_distance'].append(UD[u]['out_ave_distance'][t]-GDedge[hpos]['out_ave_distance']) 
                #UHD[u]['d_in_std_distance'].append(UD[u]['in_std_distance'][t+1]-GDedge[hpos]['in_std_distance'][t]) 
                #UHD[u]['d_out_std_distance'].append(UD[u]['out_std_distance'][t+1]-GDedge[hpos]['out_std_distance'][t]) 
                #UHD[u]['d_in_ave_time'].append(UD[u]['in_ave_time'][t+1]-GDedge[hpos]['in_ave_time'][t]) 
                #UHD[u]['d_out_ave_time'].append(UD[u]['out_ave_time'][t+1]-GDedge[hpos]['out_ave_time'][t]) 
                #UHD[u]['d_in_std_time'].append(UD[u]['in_std_time'][t+1]-GDedge[hpos]['in_std_time'][t]) 
                #UHD[u]['d_out_std_time'].append(UD[u]['out_std_time'][t+1]-GDedge[hpos]['out_std_time'][t])
            
                ns=G.nodes()         
                if G.has_edge(hpos,pos):
                
                    #Descriptors of the vector - edge of the network
                    UHD[u]['distance'].append(G[hpos][pos]['distance'])#distance is fix
                   # UVD[u]['ratio_time'].append(d_time/(G[pos][npos]['time']))#velocity can change
                    UHD[u]['flow'].append(G[hpos][pos]['weight'])
                else:
                    UHD[u]['distance'].append(math.nan)#distance is fix
                    #UVD[u]['ratio_time'].append(-1)#velocity can change
                    UHD[u]['flow'].append(math.nan)

  
print('finish, writing') 
             
if doFilter:
    with open(trajdesc+'UHD_v3f'+region+'_th'+str(th)+'.cnf', 'wb') as handle:
        pickle.dump(UHD, handle, protocol=pickle.HIGHEST_PROTOCOL)    
else:
    with open(trajdesc+'UHD_v3'+region+'_th'+str(th)+'.cnf', 'wb') as handle:
        pickle.dump(UHD, handle, protocol=pickle.HIGHEST_PROTOCOL)  