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

def getday(d):
    if d<10:
        ds='0'+str(d)
    else:
        ds=str(d)
    return ds

def getDateIndexHour(s):
    mdays=[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    f = "%d-%m-%Y %H"
    dt = datetime.strptime(s, f)
    index1=dt.month
    print(index1)
    print(mdays[index1-1])
    index=(mdays[index1-1]+dt.day-1)*24+dt.hour
    return index

def getDateIndex(s):
    mdays=[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    f = "%d-%m-%Y %H"
    dt = datetime.strptime(s, f)
    index1=dt.month
    index=(mdays[index1-1]+dt.day-1)
    return index

def indexdate(month,day):
    m=[0,31,59,90,120,151,181,212,243,273,304,334,365]
    month=int(month)
    day=int(day)
    return m[month-1]+day

def getDate(i):
    mdays=[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    moff=i-np.array(mdays)
    mt=moff<0
    moff[mt]=8888
    
    ind=np.argmin(abs(moff))
    day=1+moff[ind]
    month=1+ind
    
    if day<10:
        dday='0'+str(day)
    else:
        dday=str(day)
    if month<10:
        dmon='0'+str(month)
    else:
        dmon=str(month)
    return dday+'-'+dmon+'-2017'

def getMonth(i):
    mdays=[0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    moff=i-np.array(mdays)
    mt=moff<0
    moff[mt]=8888
    
    ind=np.argmin(abs(moff))
    day=1+moff[ind]
    month=1+ind
    return month
    
def dms2dec(d, m, s):
    if len(d)>0:
        dd = int(d) + float(m)/60 + float(s)/3600
    else:
        dd = float(m)/60 + float(s)/3600
    return dd

#HOME LOCATION
#Indetify reference location for each user

datapath='/home/davidpastor/TEF_mob/'

netpath=datapath+'nets/'
netdescpath=datapath+'nets_desc/'
trajpath=datapath+'trajs/'

vector={}
HL={}
vector2={}
hour_th=19
dayoffset=20#monday 20/01/2014
ndays=5#monday to thrusday

for yDay in range(dayoffset,dayoffset+ndays):
    
    with open(trajpath+'usersTracking'+'_'+str(yDay)+'.tff', 'rb') as fpp:
        usersTracking=pickle.load(fpp)
 
    
    for u in usersTracking:    
        if u not in vector:
            vector[u]=[]
            vector2[u]=[]
            avisited=usersTracking[u]['ss']
            tvisited=usersTracking[u]['ts']#we could include time
            
            for i in range(1, len(avisited)+1):
                aid=avisited[i]
                timevisited=time.localtime(tvisited[i])
                hourvisited=timevisited.tm_hour
                if hourvisited>hour_th:
                    vector[u].append(aid)
                vector2[u].append(aid)
                
    del usersTracking
    
for u in vector:
    if u not in HL:
        HL[u]={}
        HL[u]['homeloc']=-1
        HL[u]['n_homeloc']=-1
    v=vector[u]
    my_counter=collections.Counter(v)
    mc=my_counter.most_common()
    if len(mc)<1:
        v=vector2[u]
        my_counter=collections.Counter(v)
        mc=my_counter.most_common()
        
    HL[u]['homeloc']=mc[0][0]#most frequent location
    HL[u]['n_homeloc']=mc[0][1]#ntimes of the most frequent location
                
with open(trajpath+'HL'+'.tff', 'wb') as handle:
    pickle.dump(HL, handle, protocol=pickle.HIGHEST_PROTOCOL)  