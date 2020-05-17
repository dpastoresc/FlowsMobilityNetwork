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

start = timer()
     
with open(netpath+'Net2ref.cnf', 'rb') as fpp:
    Gf=pickle.load(fpp)
dif_time=[]

for yDay in range(13,18):
    
    print(yDay)
   
    with open(netpath+'Net2'+'_'+str(yDay)+'.cnf', 'rb') as fpp:
        G=pickle.load(fpp)
        
    dif=0
    
    es = Gf.edges()
    for e in es:
        n1=e[0]
        n2=e[1]
        if G.has_edge(n1,n2):
            dif=dif+(np.abs(Gf[n1][n2]['weight']-G[n1][n2]['weight']))
        else:
            dif=dif+Gf[n1][n2]['weight']
    
    dif_time.append(dif)    
        
print(dif_time)
end = timer()
