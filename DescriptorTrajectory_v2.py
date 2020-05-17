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
import  math
from datetime import datetime, timedelta, date
from os import listdir
from os.path import isfile, join
from timeit import default_timer as timer

#Create a descriptor vector from the net values of the trajectories
region='_medellin'
th=1

datapath='/home/davidpastor/TEF_mob/'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'
trajdesc=datapath+'traj_net/'


with open(trajdesc+'UD_v3'+region+'_th'+str(th)+'.cnf', 'rb') as handle:
    UD=pickle.load(handle) 
    
descs=['ind', 'outd', 'in_degree', 'out_degree','in_eigenvalue',
       'out_eigenvalue','in_betweenness','out_betweenness','dis_betweenness','cfbetweenness',
       'in_closeness','out_closeness','dis_closeness', 'cfcloseness','in_ave_flow','out_ave_flow',
       'in_std_flow','out_std_flow','in_ave_distance','out_ave_distance','in_std_distance', 
       'out_std_distance','in_ave_time','out_ave_time','in_std_time','out_std_time']

descs=['in_degree', 'out_degree','in_eigenvalue',
       'out_eigenvalue','in_betweenness','out_betweenness','dis_betweenness','cfbetweenness',
       'in_closeness','out_closeness','dis_closeness', 'cfcloseness','in_flow', 'out_flow', 'in_ave_flow','out_ave_flow',
       'in_std_flow','out_std_flow','in_ave_distance','out_ave_distance']




for desc in descs:
    print(desc)
    TD={}
    for u in UD:
        v=UD[u][desc]
        #v = [x for x in v if not math.isnan(x)]
        if len(v)>0:
            if u not in TD:
                TD[u]={}
            TD[u]['max']=np.nanmax(v)
            TD[u]['min']=np.nanmin(v)
            TD[u]['mean']=np.nanmean(v)
            TD[u]['std']=np.nanstd(v)
            TD[u]['median']=np.nanmedian(v)
        
    #with open(trajdesc+'TD_'+desc+region+'_th'+str(th)+'.cnf', 'wb') as handle:
    with open(trajdesc+'TD_'+desc+region+'.cnf', 'wb') as handle:
        pickle.dump(TD, handle, protocol=pickle.HIGHEST_PROTOCOL) 
                
