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
import math
from datetime import datetime, timedelta, date
from os import listdir
from os.path import isfile, join
from timeit import default_timer as timer

#Create a descriptor vector from the net values of the trajectories
region='_bogota'
th=1

datapath='/home/davidpastor/TEF_mob/'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'
trajdesc=datapath+'traj_net/'
trajdescexp=datapath+'traj_vis/'


with open(trajdesc+'UVD_v3f'+region+'_th'+str(th)+'.cnf', 'rb') as handle:
    UVD=pickle.load(handle) 

descs=['d_ind', 'd_outd', 'd_in_degree', 'd_out_degree','d_in_eigenvalue','d_out_eigenvalue',
       'd_in_betweenness','d_out_betweenness','d_dis_betweenness','d_cfbetweenness',
       'd_in_closeness','d_out_closeness','d_dis_closeness', 'd_cfcloseness', 
       'd_in_ave_flow','d_out_ave_flow',
       'd_in_std_flow','d_out_std_flow','d_in_ave_distance','d_out_ave_distance','d_in_std_distance', 
       'd_out_std_distance','d_in_ave_time','d_out_ave_time','d_in_std_time','d_out_std_time',
       'distance', 'flow', 'd_time']

descs=['d_in_degree', 'd_out_degree','d_in_eigenvalue','d_out_eigenvalue',
       'd_in_betweenness','d_out_betweenness','d_dis_betweenness','d_cfbetweenness',
       'd_in_closeness','d_out_closeness','d_dis_closeness', 'd_cfcloseness', 
       'd_in_ave_flow','d_out_ave_flow',
       'd_in_std_flow','d_out_std_flow','d_in_ave_distance','d_out_ave_distance',
       'distance', 'flow', 'd_time']

for desc in descs:
    print(desc)
    TVD={}
    for u in UVD:
        v=UVD[u][desc]
        #v = [x for x in v if not math.isnan(x)]
        if len(v)>0:
            if u not in TVD:
                TVD[u]={}
            TVD[u]=v
            
    with open(trajdescexp+'Trajectories_'+desc+region+'.vtf', 'w') as handle:
        json.dump(TVD, handle) 
            
