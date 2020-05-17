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

datapath='/home/davidpastor/TEF_mob/'
netpath=datapath+'nets/'
GD={}
for yDay in range(1,61):
    
    print(yDay)
    start = timer()
    
    with open(netpath+'Net'+'_'+str(yDay)+'.cnf', 'rb') as fpp:
        G=pickle.load(fpp)
        
    with open(netpath+'Netu'+'_'+str(yDay)+'.cnf', 'rb') as fpp:
        Gu=pickle.load(fpp)
    
    my_ns=G.nodes
    
    for n in my_ns:
        #print(n)
        if n not in GD:
            GD[n]={}

        #Edge descriptors statistics: Flow, distance, time
        succ=G.successors(n)
        lensuc=len(list(succ))
        pred=G.predecessors(n)
        lenpred=len(list(pred))
        
        out_flow=0
        in_flow=0
        out_dis=0
        in_dis=0
        out_delta=0
        in_delta=0
        
        for ns in succ:
            out_flow=out_flow+G[n][ns]['weight']
            out_dis=out_dis+G[n][ns]['distance']
            out_delta=out_delta+G[n][ns]['time']
            out_delta=out_delta/out_flow
        
        for np in pred:
            in_flow=in_flow+G[np][n]['weight']
            in_dis=in_dis+G[np][n]['distance']
            in_delta=in_delta+G[np][n]['time']
            in_delta=in_delta/in_flow
        
        if lensuc>0:
            
            ave_out_flow=out_flow/lensuc
            out_dis=out_dis/lensuc 
            out_delta=out_delta/lensuc
            
        if lenpred>0:
    
            ave_in_flow=in_flow/lenpred
            in_dis=in_dis/lenpred
            in_delta=in_delta/lenpred
        
        
        GD[n]['out_flow']=out_flow
        GD[n]['in_flow']=in_flow
        GD[n]['out_ave_flow']=ave_out_flow
        GD[n]['in_ave_flow']=ave_in_flow
        GD[n]['out_distace']=out_dis
        GD[n]['in_distace']=in_dis
        GD[n]['out_time']=out_delta
        GD[n]['in_time']=in_delta
        
        #We could add socio-economic descriptors to the node
        
    with open(netpath+'/NDedge_'+str(yDay)+'.cnf', 'wb') as handle:
        pickle.dump(GD, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('Finished '+str(yDay))
    end = timer()
    print(end - start)
