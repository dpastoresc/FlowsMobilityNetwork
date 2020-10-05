import pandas as pd
import numpy as np
import networkx as nx
import os
from utils import getRootPath
import pickle
from sklearn import preprocessing


#Load undirected graphs

with open(os.path.join(getRootPath(),'data/Netu2refc_bogota_th1.cnf'), 'rb') as f:
    Net_undBog = pickle.load(f)

with open(os.path.join(getRootPath(),'data/Netu2refc_medellin_th1.cnf'), 'rb') as f:
    Net_undMed = pickle.load(f)



#MERGE descs of BOG and MED and join with latitude and longitude
def prepare_descs():
    ###LOAD DATA
    ND_desc_BOG = pd.read_csv(os.path.join(getRootPath(), 'data/ND_descriptors_bogota.csv'))
    ND_desc_MED = pd.read_csv(os.path.join(getRootPath(), 'data/ND_descriptors_medellin.csv'))

    antenas_loc = pd.read_csv(os.path.join(getRootPath(),'data/sites_random2.csv'))

    ND_desc_BOG['city'] = 'BOG'
    ND_desc_MED['city'] = 'MED'

    NDdescs_COL = ND_desc_BOG.append(ND_desc_MED, ignore_index=True)

    df_antennasJoin = NDdescs_COL.merge(antenas_loc, left_on='antenna', right_on='antenna_id', how='inner')

    return NDdescs_COL, df_antennasJoin

#Get the network for the selected city
def get_net_city(city):
    Net_und = nx.Graph()
    if city == 'BOG':
        Net_und = Net_undBog

    elif city == 'MED':
        Net_und = Net_undMed

    return Net_und


# px, desc, Gu, Gd
def filter_network(px, desc, Gu, df, limit_inf, limit_sup):

    # Get the desc selected
    df_desc = df[[desc, 'antenna']]
    vb = df_desc[desc].to_list()

    # filter based on the px
    pv_inf = np.percentile(vb, limit_inf)
    pv_sup = np.percentile(vb, limit_sup)
    df2_desc = df_desc[(df_desc[desc] > pv_inf) & (df_desc[desc] < pv_sup )]

    # Hace una copia y filtra los nodos
    Guf = Gu.copy()
    nus = Gu.nodes()

    nsel = df2_desc["antenna"].values

    for n in nus:
        if n not in nsel:
            Guf.remove_node(n)
    return Guf



def calc_positions(Gu): #, px, desc, city):

    pos_layout = nx.spring_layout(Gu)
    # Lo guarda en una carpeta de layouts
    #with open(os.path.join(getRootPath(), 'data/positionsNetworks/'+city+'/Laytout_' + desc + '_px_' + str(px)), 'wb') as handle:
    #    pickle.dump(pos_layout, handle, protocol=pickle.HIGHEST_PROTOCOL)

    #print('Saved'+'data/positionsNetworks/'+city+'/Laytout_' + desc + '_px_' + str(px))

    return pos_layout


#Function that normalize the values of the dataframe
def normalize_df (df):
    columns_name = df.columns
    x = df.values  # returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    normalized_df = pd.DataFrame(x_scaled)
    normalized_df.columns = columns_name

    return normalized_df
