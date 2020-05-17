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
    
#Creates mobility network
#The traffic of the network is computed in a daily basis
#ToDo -> use other temporal resolutions

datapath='/home/davidpastor/TEF_mob/'
trajpath=datapath+'trajs/'
netpath=datapath+'nets/'
ant_file='antennas/antennas_colombia.csv'
sheet=pd.read_csv(ant_file,delimiter=',')
print(len(sheet))
aid=sheet['antenna_id']
i
#48
#55

for yDay in range(61,71):
    print(yDay)
    start = timer()
    
    with open(trajpath+'usersTracking'+'_'+str(yDay)+'.tff', 'rb') as fpp:
        usersTracking=pickle.load(fpp)
    users=usersTracking.keys()
    print(len(users))
    avuser=[]
    avuser2=[]
    G=nx.DiGraph()
    Gu=nx.Graph()
    for u in users:
        #print(usersTracking[u].keys())
        avisited=usersTracking[u]['ss']
        tvisited=usersTracking[u]['ts']
        avuser.append(len(avisited))
        avuser2.append(usersTracking[u]['sc'])
        #print(len(avisited))
        #print(usersTracking[u][yDay]['sc'])
        if len(avisited)>1:
            for i in range(1, len(avisited)):
                
                orig=avisited[i]
                dest=avisited[i+1]
                ao=sheet[aid==orig]
                ad=sheet[aid==dest]
                aolat=ao.LATITUD.values[0]
                aolon=ao.LONGITUD.values[0]
                adlat=ad.LATITUD.values[0]
                adlon=ad.LONGITUD.values[0]
                
                delta=tvisited[i+1]-tvisited[i]
                
                #print(avisited[i])
                #print(avisited[i+1])
                if not G.has_node(orig):
                    G.add_node(orig)
                if not G.has_node(dest):
                    G.add_node(dest)
                if not G.has_edge(orig,dest):  
                    G.add_edge(orig,dest)  
                    #Flow
                    G[orig][dest]['weight']=1
                    #Distance
                    d=math.sqrt(math.pow((aolat-adlat),2)+math.pow((aolon-adlon),2))
                    G[orig][dest]['distance']=d
                    #Speed-> too sensitive to sampling
                    G[orig][dest]['time']=delta
                else:
                    G[orig][dest]['weight']=G[orig][dest]['weight']+1
                    G[orig][dest]['time']=G[orig][dest]['time']+delta
                 
                if not Gu.has_node(orig):
                    Gu.add_node(orig)
                if not Gu.has_node(dest):
                    Gu.add_node(dest)
                if not Gu.has_edge(orig,dest):  
                    Gu.add_edge(orig,dest)  
                    #Flow
                    Gu[orig][dest]['weight']=1
                    #Distance
                    d=math.sqrt(math.pow((aolat-adlat),2)+math.pow((aolon-adlon),2))
                    Gu[orig][dest]['distance']=d
                    #Speed-> too sensitive to sampling
                    Gu[orig][dest]['time']=delta
                else:
                    Gu[orig][dest]['weight']=Gu[orig][dest]['weight']+1
                    Gu[orig][dest]['time']=Gu[orig][dest]['time']+delta
                
        else:
            #print('sole node')
            orig=avisited[1]
            #if not G.has_node(orig):
            #    G.add_node(orig)
            #if not Gu.has_node(orig):
            #    Gu.add_node(orig)

    with open(netpath+'Net_'+str(yDay)+'.cnf', 'wb') as handle:
        pickle.dump(G, handle, protocol=pickle.HIGHEST_PROTOCOL) 
        
    with open(netpath+'Netu_'+str(yDay)+'.cnf', 'wb') as handle:
        pickle.dump(Gu, handle, protocol=pickle.HIGHEST_PROTOCOL) 
    
    end = timer()
    print(end - start)
