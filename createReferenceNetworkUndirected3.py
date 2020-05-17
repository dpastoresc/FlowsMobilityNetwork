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
    
datapath='/home/davidpastor/TEF_mob/'
netpath=datapath+'nets/'

Gf=nx.Graph()
start = timer()
    
for yDay in range(20,25):
    
    print(yDay)
   
    with open(netpath+'Netu2'+'_'+str(yDay)+'.cnf', 'rb') as fpp:
        G=pickle.load(fpp)
    
    my_ns=G.nodes  
    print(len(my_ns))

    es = G.edges()

    for e in es:
        
            n1=e[0]
            n2=e[1]
            
            if not Gf.has_node(n1):
                Gf.add_node(n1)
                
            if not Gf.has_node(n2):
                Gf.add_node(n2)   

            if not Gf.has_edge(n1,n2):  
                    Gf.add_edge(n1,n2)
                    Gf[n1][n2]['time']= 0
                    Gf[n1][n2]['weight']= 0
                    Gf[n1][n2]['inv_flow']= 0
                    Gf[n1][n2]['count']= 0
            Gf[n1][n2]['distance']= G[n1][n2]['distance']
            Gf[n1][n2]['time']= Gf[n1][n2]['time']+G[n1][n2]['time']
            Gf[n1][n2]['weight']= Gf[n1][n2]['weight']+G[n1][n2]['weight']
            Gf[n1][n2]['inv_flow']= Gf[n1][n2]['inv_flow']+G[n1][n2]['inv_flow']
            Gf[n1][n2]['count']=Gf[n1][n2]['count']+1

            
    my_ns2=Gf.nodes  
    print(len(my_ns2))
            
    es = G.edges()
    es2= Gf.edges()
    print(len(es))
    print(len(es2))

es2= Gf.edges()    
for e in es2:
    n1=e[0]
    n2=e[1]
    Gf[n1][n2]['time']=Gf[n1][n2]['time']/Gf[n1][n2]['count']
    Gf[n1][n2]['weight']=Gf[n1][n2]['weight']/Gf[n1][n2]['count']
    Gf[n1][n2]['inv_flow']=Gf[n1][n2]['inv_flow']/Gf[n1][n2]['count']
        
with open(netpath+'/Netu2ref.cnf', 'wb') as handle:
     pickle.dump(Gf, handle, protocol=pickle.HIGHEST_PROTOCOL)    
        
print('Finished '+str(yDay))
end = timer()
print(end - start)
