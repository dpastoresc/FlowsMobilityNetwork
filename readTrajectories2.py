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

print('Reading trajectories...')

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

cdr_folder='/Volumes/OS Disk/Tef_Colombia/data_sorted/'
cdr_folder='/home/davidpastor/TEF_mob/'
trajpath=cdr_folder+"trajs/"
year=['2014']
month=['01','02','03','04','05']
day=[31,28,31,30,31]

month=['03','04','05']
day=[26,30,31]
day_start=14
ant_file='antennas/antennas_colombia.csv'
pattern='%Y-%m-%d %H:%M:%S'


#READ ANTENNAS
sheet=pd.read_csv(ant_file,delimiter=',')
print(sheet.head())
#LAC=sheet['LAC_HEX']
#Cell=sheet['Celda_HEX']
lon=sheet['LONGITUD']
lat=sheet['LATITUD']
#sheet['antenna_id']=LAC+Cell
aid=sheet['antenna_id']
#print(sheet.head())

#sheet2=sheet[sheet['LONGITUD']<0]
#sheet3=sheet2[sheet2['LATITUD']>-50]
print(len(sheet))

minlat=np.float64(np.min(lat))
maxlat=np.float64(np.max(lat))
minlon=np.float64(np.min(lon))
maxlon=np.float64(np.max(lon))
print(minlat,maxlat,minlon,maxlon)

cd=0
c=0
count2=0

#READ CDRs
for y in year:
    for m in month:
        for di in range (day_start, day[cd]+1):
            usersTracking={}
            d=getday(di)
            cdr_file=y+m+d
            print(cdr_file)
            start = timer()
            
            with open(cdr_folder+cdr_file, 'r') as fl:
                #D_rows = pd.read_csv(fl, header=None)
                D_rows=json.load(fl)
            print(len(D_rows))

            for row in D_rows:
                my_id=row[1]
                ix=aid.index[aid==my_id]
                if len(ix)>0:#only take the cdrs with known antenna loc
                    ix=ix[0]
                    userId=row[0]
                    dated=y+'-'+m+'-'+d+' '+row[2]
                    #td=(datetime.strptime(dated, '%Y-%m-%d %H:%M:%S'))
                    #month=td.month
                    #day=td.day
                    #idate=indexdate(month,day)
                    #timed=td.strftime("%Y-%m-%d %H:%M:%S")
                    tdd=time.strptime(dated,pattern)
                    ts=int(time.mktime(tdd))
                    #print(idate)
                    if userId not in usersTracking:
                        usersTracking[userId]={}
                        usersTracking[userId]['ss']={}
                        usersTracking[userId]['sc']=0
                        usersTracking[userId]['ts']={}
                    c_s=usersTracking[userId]['sc']+1
                    usersTracking[userId]['sc']=c_s
                    usersTracking[userId]['ss'][c_s]=my_id
                    usersTracking[userId]['ts'][c_s]=ts
                else:
                    count2=count2+1
            yDay=tdd.tm_yday        
            with open(trajpath+'usersTracking'+'_'+str(yDay)+'.tff', 'wb') as fpp:
                pickle.dump(usersTracking, fpp, protocol=pickle.HIGHEST_PROTOCOL)
            end = timer()
            print(end - start)
        cd=cd+1

print("Non found antennas "+str(count2))
print("Read trajectories finished")
