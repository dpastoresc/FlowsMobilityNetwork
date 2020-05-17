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
region='_medellin'
tag_connected='c'
th=0

datapath='/home/davidpastor/TEF_mob/'
netpath=datapath+'nets/'
descpath=datapath+'nets_desc/'

GD={}

start = timer()

with open(netpath+'Netu2ref'+tag_connected+region+'_th'+str(th)+'.cnf', 'rb') as fpp:
    Gu=pickle.load(fpp)

my_ns=Gu.nodes
print(len(my_ns))

if nx.is_connected(Gu):
    print('connected')
else:
    print('unconnected')
    #Get the connected part
    

#Betweenness centrality
BFCN=nx.current_flow_betweenness_centrality(Gu, weight='inv_flow')
#Closeness centrality
CFCN=nx.current_flow_closeness_centrality(Gu,weight='inv_flow')

for n in my_ns:
    #print(n)
    if n not in GD:
        GD[n]={}
        
    GD[n]['cfbetweenness']=BFCN[n]
    GD[n]['cfcloseness']=CFCN[n]      
    #We could add socio-economic descriptors to the node
    
with open(descpath+'/NDcfref'+region+'_th'+str(th)+'.cnf', 'wb') as handle:
    pickle.dump(GD, handle, protocol=pickle.HIGHEST_PROTOCOL)

end = timer()
print(end - start)
