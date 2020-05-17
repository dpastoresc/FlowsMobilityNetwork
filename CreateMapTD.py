#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 23:50:08 2020

@author: davidpastor
"""
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

#Project onto map the statistics of a decriptor at the trajectory level

region='_kaffrine'
tag=''

datapath='/home/davidpastor/D4D/'
netpath=datapath+'D2nets/'
netdescpath=datapath+'D2nets_desc/'
trajpath=datapath+'D2trajs/'
trajdesc=datapath+'D2traj_net/'

descs=['d_in_degree', 'd_out_degree','d_in_eigenvalue','d_out_eigenvalue',
       'd_in_betweenness','d_out_betweenness','d_dis_betweenness','d_cfbetweenness',
       'd_in_closeness','d_out_closeness','d_dis_closeness', 'd_cfcloseness', 
       'd_in_ave_flow','d_out_ave_flow',
       'd_in_std_flow','d_out_std_flow','d_in_ave_distance','d_out_ave_distance',
       'distance', 'flow', 'd_time']



ant_file='antennas/antennas.csv'
sheet=pd.read_csv(ant_file,delimiter=';')
print(sheet.head())
LAC=sheet['LAC_HEX']
Cell=sheet['Celda_HEX']
sheet['antenna_id']=LAC+Cell

with open(trajpath+'HL.tff', 'rb') as fpp:
    HL=pickle.load(fpp) 
    
for d in descs:
    
    with open(trajdesc+'TD'+tag+'_'+str(fn)+'_'+d+region+'.cnf', 'rb') as fpp:
        VD=pickle.load(fpp) 
    
    vector=[]
    vectoru=[]
    vectorh=[]
    for u in VD:
        vector.append(VD[u][stat[ic]])
        vectoru.append(u)
        vectorh.append(HL[u]['homeloc'])
    
    print(len(vector))
    print(len(vectoru))
        
    df = pd.DataFrame(list(zip(vectoru, vector, vectorh)), columns =['user', d, 'home']) 
    
    locations=df['home'].values
    Hvalues={}
    
    print(len(locations))
    mv_v=[]
    stdv_v=[]
    lon=[]
    lat=[]
    for h in locations:
        df_h=df[df['home']==h]
        v=df_h[d].values
        m_v=np.nanmean(v)
        std_v=np.nanstd(v)
        mv_v.append(m_v)
        stdv_v.append(std_v)
        reg=sheet[sheet['antenna_id']==h]
        lon.append(reg['LONGITUD'].values[0])
        lat.append(reg['LATITUD'].values[0])
        
    df2 = pd.DataFrame(list(zip(average, std, location, lon, lat)), columns =['average', 'std', 'antenna', 'l1', 'l2']) 
    print(df2.head())
    print(len(df2))
    df2.to_csv('TVDstats_'+d+'_'+stat[ic]+region+'.csv',index=False)