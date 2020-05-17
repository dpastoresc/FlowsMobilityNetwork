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

datapath='/home/davidpastor/TEF_mob/'
region='_bogota'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'
trajdesc=datapath+'traj_net/'
  
GDall={}
GDcfall={}            
    
for yDay in range(13,18):
    
    print(yDay)
   
    with open(netdescpath+'ND'+'_'+str(yDay)+region+'.cnf', 'rb') as fpp:
        GD=pickle.load(fpp)
            
    with open(netdescpath+'NDcf'+'_'+str(yDay)+region+'.cnf', 'rb') as fpp:
        GDcf=pickle.load(fpp)  
        
    for d in GD:
        if d not in GDall:
            GDall[d]={}
            GDall[d]=GD[d]
            
    for d2 in GDcf:
        if d2 not in GDcfall:
            GDcfall[d2]={}
            GDcfall[d2]=GDcf[d2]
                    
with open(netdescpath+'NDref'+region+'.cnf', 'wb') as handle:
    pickle.dump(GDall, handle, protocol=pickle.HIGHEST_PROTOCOL) 
    
with open(netdescpath+'NDcfref'+region+'.cnf', 'wb') as handle:
    pickle.dump(GDcfall, handle, protocol=pickle.HIGHEST_PROTOCOL)     