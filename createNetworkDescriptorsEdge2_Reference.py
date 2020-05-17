# DELIVERABLE FOR THE PROJECT:
# "KINEMATICS OF MOBILITY"
# David Pastor-Escuredo (Life D Lab)
# Licencia MIT

#Copyright <2019> <David Pastor Escuredo>

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import pandas as pd
import numpy as np
import json
from nltk.tokenize import word_tokenize
import re
import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import collections
from sklearn.cluster import KMeans
from PIL import Image
import time
from datetime import datetime, timedelta, date
from os import listdir
from os.path import isfile, join
from geopandas import GeoDataFrame
from shapely.geometry import Point
import pickle
import math
from timeit import default_timer as timer

def getday(d):
    if d<10:
        ds='0'+str(d)
    else:
        ds=str(d)
    return ds

def distAntenna(origvector,desvector):
    d=math.pow((origvector[0]-desvector[0]),2)+math.pow((origvector[1]-desvector[1]),2)
    d=math.sqrt(d)
    
#Creates mobility network descriptors
tag_connected='c'
region='_medellin'
th=0

datapath='/home/davidpastor/TEF_mob/'
netpath=datapath+'nets/'
descpath=datapath+'nets_desc/'

GD={}

start = timer()

with open(netpath+'Net2ref'+tag_connected+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
    G=pickle.load(fpp)
    
#with open(netpath+'Netu2'+'_'+str(yDay)+region+'.cnf', 'rb') as fpp:
#    Gu=pickle.load(fpp)

my_ns=G.nodes
c1=0
c2=0
print(len(my_ns))
for n in my_ns:
    #print(n)
    if n not in GD:
        GD[n]={}

    #Edge descriptors statistics: Flow, distance, time
    succ=G.successors(n)
    pred=G.predecessors(n)

    #print(lensuc)
    #print(lenpreds)
    
    out_flow=[]
    in_flow=[]
    out_dis=[]
    in_dis=[]
    out_delta=[]
    in_delta=[]
    
    lc1=0
    for ns in succ:
        lc1=lc1+1
        c1=c1+1
        out_flow.append(G[n][ns]['weight'])
        out_dis.append(G[n][ns]['distance'])
        oud=G[n][ns]['time']/G[n][ns]['weight']
        out_delta.append(oud)
    
    lc2=0
    for npd in pred:
        lc2=lc2+1
        c2=c2+1
        in_flow.append(G[npd][n]['weight'])
        in_dis.append(G[npd][n]['distance'])
        ind=G[npd][n]['time']/G[npd][n]['weight']
        in_delta.append(ind)
    
    tot_out_flow=math.nan
    ave_out_flow=math.nan
    std_out_flow=math.nan
    ave_out_dis=math.nan
    std_out_dis=math.nan
    ave_out_delta=math.nan
    std_out_delta=math.nan
    
    if lc1>0:
        
        tot_out_flow=np.sum(out_flow)
        ave_out_flow=np.mean(out_flow)
        std_out_flow=np.std(out_flow)
        ave_out_dis=np.mean(out_dis)
        std_out_dis=np.std(out_dis)
        ave_out_delta=np.mean(out_delta)
        std_out_delta=np.std(out_delta)
       
    tot_in_flow=math.nan
    ave_in_flow=math.nan
    std_in_flow=math.nan
    ave_in_dis=math.nan
    std_in_dis=math.nan
    ave_in_delta=math.nan
    std_in_delta=math.nan
    
    if lc2>0:

        tot_in_flow=np.sum(in_flow)
        ave_in_flow=np.mean(in_flow)
        std_in_flow=np.std(in_flow)
        ave_in_dis=np.mean(in_dis)
        std_in_dis=np.std(in_dis)
        ave_in_delta=np.mean(in_delta)
        std_in_delta=np.mean(in_delta)
    
    GD[n]['out_flow']=tot_out_flow
    GD[n]['in_flow']=tot_in_flow
    GD[n]['out_ave_flow']=ave_out_flow
    GD[n]['in_ave_flow']=ave_in_flow
    GD[n]['out_std_flow']=std_out_flow
    GD[n]['in_std_flow']=std_in_flow
    
    GD[n]['out_ave_distance']=ave_out_dis
    GD[n]['in_ave_distance']=ave_in_dis
    GD[n]['out_std_distance']=std_out_dis
    GD[n]['in_std_distance']=std_in_dis
    
    GD[n]['out_ave_time']=ave_out_delta
    GD[n]['in_ave_time']=ave_in_delta
    GD[n]['out_std_time']=std_out_delta
    GD[n]['in_std_time']=std_in_delta
    #We could add socio-economic descriptors to the node

print(c1)
print(c2)

with open(descpath+'/NDedgeref'+region+'_th'+str(th)+'.cnf', 'wb') as handle:
    pickle.dump(GD, handle, protocol=pickle.HIGHEST_PROTOCOL)
   
end = timer()
print(end - start)
