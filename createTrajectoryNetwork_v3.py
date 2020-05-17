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
import math

#Create a descriptor vector from the net values of the trajectories
region='_medellin'
th=1

datapath='/home/davidpastor/TEF_mob/'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'
trajdesc=datapath+'traj_net/'

UD={}

with open(netdescpath+'NDref'+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
        GD=pickle.load(fpp)
        
with open(netdescpath+'NDcfref'+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
        GDcf=pickle.load(fpp) 
        
with open(netdescpath+'NDedgeref'+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
        GDedge=pickle.load(fpp) 
             

for yDay in range(20,25):
    
    with open(trajpath+'usersTracking'+'_'+str(yDay)+'.tff', 'rb') as fpp:
        usersTracking=pickle.load(fpp)
   
    #with open(netpath+'Net2c'+'_'+str(yDay)+region+'.cnf', 'rb') as fpp:
    #    G=pickle.load(fpp)
        
    for u in usersTracking:
        avisited=usersTracking[u]['ss']
        tvisited=usersTracking[u]['ts']
        if u not in UD:
            UD[u]={}
            UD[u]['ind']=[]
            UD[u]['outd']=[]
            UD[u]['in_degree']=[]
            UD[u]['out_degree']=[]
            UD[u]['in_eigenvalue']=[]
            UD[u]['out_eigenvalue']=[]
            UD[u]['in_betweenness']=[]
            UD[u]['out_betweenness']=[]
            UD[u]['dis_betweenness']=[]
            UD[u]['cfbetweenness']=[]
            UD[u]['in_closeness']=[]
            UD[u]['out_closeness']=[]
            UD[u]['dis_closeness']=[]
            UD[u]['cfcloseness']=[] 
            UD[u]['in_flow']=[]
            UD[u]['out_flow']=[]
            UD[u]['in_ave_flow']=[]
            UD[u]['out_ave_flow']=[]
            UD[u]['in_std_flow']=[]
            UD[u]['out_std_flow']=[]
            UD[u]['in_ave_distance']=[]
            UD[u]['out_ave_distance']=[]
            UD[u]['in_std_distance']=[]
            UD[u]['out_std_distance']=[]
            UD[u]['in_ave_time']=[]
            UD[u]['out_ave_time']=[]
            UD[u]['in_std_time']=[]
            UD[u]['out_std_time']=[]             
            UD[u]['time']=[]
            UD[u]['position']=[]
                       
        for i in range(1, len(avisited)+1):
            aid=avisited[i]    
            if aid in GD and aid in GDcf and aid in GDedge:#we impose this double condition
                UD[u]['ind'].append(GD[aid]['ind'])
                UD[u]['outd'].append(GD[aid]['outd'])
                UD[u]['in_degree'].append(GD[aid]['in_degree'])
                UD[u]['out_degree'].append(GD[aid]['out_degree'])
                UD[u]['in_eigenvalue'].append(GD[aid]['in_eigenvalue'])
                UD[u]['out_eigenvalue'].append(GD[aid]['out_eigenvalue'])  
                UD[u]['in_betweenness'].append(GD[aid]['in_betweenness'])
                UD[u]['out_betweenness'].append(GD[aid]['out_betweenness'])
                UD[u]['dis_betweenness'].append(GD[aid]['dis_betweenness'])
                UD[u]['cfbetweenness'].append(GDcf[aid]['cfbetweenness'])
                UD[u]['in_closeness'].append(GD[aid]['in_closeness'])
                UD[u]['out_closeness'].append(GD[aid]['out_closeness'])
                UD[u]['dis_closeness'].append(GD[aid]['dis_closeness'])
                UD[u]['cfcloseness'].append(GDcf[aid]['cfcloseness'])
                UD[u]['in_flow'].append(GDedge[aid]['in_flow'])
                UD[u]['out_flow'].append(GDedge[aid]['out_flow'])
                UD[u]['in_ave_flow'].append(GDedge[aid]['in_ave_flow'])
                UD[u]['out_ave_flow'].append(GDedge[aid]['out_ave_flow'])
                UD[u]['in_std_flow'].append(GDedge[aid]['in_std_flow'])
                UD[u]['out_std_flow'].append(GDedge[aid]['out_std_flow'])
                UD[u]['in_ave_distance'].append(GDedge[aid]['in_ave_distance'])
                UD[u]['out_ave_distance'].append(GDedge[aid]['out_ave_distance'])
                UD[u]['in_std_distance'].append(GDedge[aid]['in_std_distance'])
                UD[u]['out_std_distance'].append(GDedge[aid]['out_std_distance'])
                UD[u]['in_ave_time'].append(GDedge[aid]['in_ave_time'])
                UD[u]['out_ave_time'].append(GDedge[aid]['out_ave_time'])
                UD[u]['in_std_time'].append(GDedge[aid]['in_std_time'])
                UD[u]['out_std_time'].append(GDedge[aid]['out_std_time'])                 
                UD[u]['time'].append(tvisited[i])
                UD[u]['position'].append(aid)
            else:
                UD[u]['ind'].append(math.nan)
                UD[u]['outd'].append(math.nan)
                UD[u]['in_degree'].append(math.nan)
                UD[u]['out_degree'].append(math.nan)
                UD[u]['in_eigenvalue'].append(math.nan)
                UD[u]['out_eigenvalue'].append(math.nan)
                UD[u]['in_betweenness'].append(math.nan)
                UD[u]['out_betweenness'].append(math.nan)
                UD[u]['dis_betweenness'].append(math.nan)
                UD[u]['cfbetweenness'].append(math.nan)
                UD[u]['in_closeness'].append(math.nan)
                UD[u]['out_closeness'].append(math.nan)
                UD[u]['dis_closeness'].append(math.nan)
                UD[u]['cfcloseness'].append(math.nan)
                UD[u]['in_flow'].append(math.nan)
                UD[u]['out_flow'].append(math.nan)
                UD[u]['in_ave_flow'].append(math.nan)
                UD[u]['out_ave_flow'].append(math.nan)
                UD[u]['in_std_flow'].append(math.nan)
                UD[u]['out_std_flow'].append(math.nan)
                UD[u]['in_ave_distance'].append(math.nan)
                UD[u]['out_ave_distance'].append(math.nan)
                UD[u]['in_std_distance'].append(math.nan)
                UD[u]['out_std_distance'].append(math.nan)
                UD[u]['in_ave_time'].append(math.nan)
                UD[u]['out_ave_time'].append(math.nan)
                UD[u]['in_std_time'].append(math.nan)
                UD[u]['out_std_time'].append(math.nan)               
                UD[u]['time'].append(tvisited[i])
                UD[u]['position'].append(aid)

    del usersTracking

print('writing to file')                        
with open(trajdesc+'UD_v4'+region+'_th'+str(th)+'.cnf', 'wb') as handle:
    pickle.dump(UD, handle, protocol=pickle.HIGHEST_PROTOCOL) 