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
do_connected=1#not implemented  yet
th=0


datapath='/home/davidpastor/TEF_mob/'
netpath=datapath+'nets/'

#FILTER BY ANTENNAS -> BOGOTA
ant_file='antennas/antennas'+region+'.csv'
sheet=pd.read_csv(ant_file,delimiter=',')
print(sheet.head())
target_aids=sheet['antenna_id'].values
print(len(target_aids))



start = timer()
    
    #with open(netpath+'Net'+'_'+str(yDay)+'.cnf', 'rb') as fpp:
    #    G=pickle.load(fpp)
Gf=nx.DiGraph()
    
with open(netpath+'Net2ref.cnf', 'rb') as fpp:
        G=pickle.load(fpp)
    
my_ns=G.nodes  
print(len(my_ns))

for n in my_ns:
        #The node is in the region of interest, we keep all the edges to that node
        if n in target_aids:
            succ=G.successors(n)
            #lensuc=len(succ)
            pred=G.predecessors(n)
            #lenpred=len(pred)
            if not Gf.has_node(n):
                Gf.add_node(n)
               
            for ns in succ:
                
                if ns in target_aids:
            
                    if not Gf.has_node(ns):
                        Gf.add_node(ns)
                        
                    w=G[n][ns]['weight']
                    if w>th:
                        
                        if not Gf.has_edge(n,ns):  
                            Gf.add_edge(n,ns)
                            Gf[n][ns]['distance']= G[n][ns]['distance']
                            Gf[n][ns]['time']= G[n][ns]['time']
                            Gf[n][ns]['weight']= G[n][ns]['weight']
                            Gf[n][ns]['inv_flow']= G[n][ns]['inv_flow']                        
                
            for np in pred:
                
                if np in target_aids:
                
                    if not Gf.has_node(np):
                        Gf.add_node(np)
                    
                    w=G[np][n]['weight']
                    if w>th:
                        
                        if not Gf.has_edge(np,n):  
                            Gf.add_edge(np,n)
                            Gf[np][n]['distance']= G[np][n]['distance']
                            Gf[np][n]['time']= G[np][n]['time']
                            Gf[np][n]['weight']= G[np][n]['weight']
                            Gf[np][n]['inv_flow']= G[np][n]['inv_flow']
        
my_ns2=Gf.nodes  
print(len(my_ns2))  
my_ns2copy=list(my_ns2).copy()      

es1=G.edges()
es2=Gf.edges()
print(len(es1))
print(len(es2))

 
if nx.is_weakly_connected(Gf):
        print('weakly connected')
else:
        print('unconnected')
        if do_connected:
            largest_cc = max(nx.weakly_connected_components(Gf), key=len)
            #print(largest_cc)
            print(len(largest_cc))
            for n2 in my_ns2copy:
                if not n2 in largest_cc:
                    Gf.remove_node(n2)
            if nx.is_weakly_connected(Gf):
                print('weakly connected')
            else:
                print('unconnected')        
            my_ns3=Gf.nodes  
            print(len(my_ns3))
            
         
if do_connected:
        with open(netpath+'/Net2refc'+region+'_th'+str(th)+'.cnf', 'wb') as handle:
            pickle.dump(Gf, handle, protocol=pickle.HIGHEST_PROTOCOL)
else:
        with open(netpath+'/Net2ref'+region+'_th'+str(th)+'.cnf', 'wb') as handle:
            pickle.dump(Gf, handle, protocol=pickle.HIGHEST_PROTOCOL)    
        
end = timer()
print(end - start)
