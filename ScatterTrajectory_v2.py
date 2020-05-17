#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
region='_medellin'
th=1
datapath='/home/davidpastor/TEF_mob/'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'
trajdesc=datapath+'traj_net/'

descs=['ind', 'outd', 'in_degree', 'out_degree','in_eigenvalue',
       'out_eigenvalue','in_betweenness','out_betweenness','dis_betweenness','cfbetweenness',
       'in_closeness','out_closeness','dis_closeness', 'cfcloseness','in_ave_flow','out_ave_flow',
       'in_std_flow','out_std_flow','in_ave_distance','out_ave_distance','in_std_distance', 
       'out_std_distance','in_ave_time','out_ave_time','in_std_time','out_std_time']

descs=['in_degree', 'out_degree','in_eigenvalue',
       'out_eigenvalue','in_betweenness','out_betweenness','dis_betweenness','cfbetweenness',
       'in_closeness','out_closeness','dis_closeness', 'cfcloseness','in_flow', 'out_flow', 'in_ave_flow','out_ave_flow',
       'in_std_flow','out_std_flow','in_ave_distance','out_ave_distance']

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
             
df=pd.DataFrame(columns=descs)
print(df.head)

index=0
for aid in GDcf:
    if aid in GD and aid in GDedge:
        aid_vector =[GD[aid]['in_degree'], GD[aid]['out_degree'], GD[aid]['in_eigenvalue'], GD[aid]['out_eigenvalue'], GD[aid]['in_betweenness'], GD[aid]['out_betweenness'],
    GD[aid]['dis_betweenness'], GDcf[aid]['cfbetweenness'], GD[aid]['in_closeness'], GD[aid]['out_closeness'], GD[aid]['dis_closeness'], GDcf[aid]['cfcloseness'],
    GDedge[aid]['in_flow'], GDedge[aid]['out_flow'], GDedge[aid]['in_ave_flow'], GDedge[aid]['out_ave_flow'], GDedge[aid]['in_std_flow'], GDedge[aid]['out_std_flow'],
    GDedge[aid]['in_ave_distance'], GDedge[aid]['out_ave_distance']]
    x=dict(zip(df.columns, aid_vector))
    df=df.append(x, ignore_index=True)
    index=index+1
                #UD[u]['in_std_distance'].append(GDedge[aid]['in_std_distance'])

print(index)
print(len(df))
print(df.head())
df.to_csv(netdescpath+'ND_table'+region+'.csv')
pd.plotting.scatter_matrix(df, ax=None, diagonal='kde')
plt.savefig("Figs/Antenna_descriptor_scatter_matrix"+region+'_th'+str(th)+".png")
            