import networkx as nx
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.figure_factory as ff

import pickle
from utils import getRootPath
from preprocess.process import calc_positions, normalize_df
import os

# Token for mapbox
TOKEN = 'pk.eyJ1IjoiY3RhcmF6b25hIiwiYSI6ImNrZDkxcW1sYjBwOWkycnM4NDRpbXViYnYifQ.jK8gChNK_dzVpKlrKKfJgA'


def paint_histogram(df, title, column, label_dict, color):
    # Cojo el df, filtro por el desc y el id
    desc = column

    df_desc = df[[desc, 'antenna']]
    vb = df_desc[desc].to_list()

    # filter based on the px
    pv = np.percentile(vb, 80)

    df2_desc = df_desc[(df_desc[desc] < pv)]

    data = df
    v_column = column
    fig = px.histogram(df2_desc, x=column,
                       # title=title,
                       labels=label_dict,  # {'polarity': 'polarity bill'},  # can specify one label per df column
                       opacity=0.8,
                       log_y=True,  # represent bars with log scale
                       color_discrete_sequence=color,  # color of histogram bars,
                       marginal='rug',
                       #nbins=60
                       )
    fig.update_layout(
        margin=dict(l=10, r=0, t=0, b=50),
        height=200,
        clickmode= 'event+select'

    )
    return fig


def paint_map(df, desc_color, desc_size, title):
    px.set_mapbox_access_token(TOKEN)

    m_col = df[desc_color],
    pmin = np.percentile(m_col, 5)
    pmax = np.percentile(m_col, 95)

    df2 = df[(df[desc_color] < pmax)]
    df2 = df2[(df2[desc_color] > pmin)]

    fig = px.scatter_mapbox(df2,
                            # title = title,
                            lat="LATITUD",
                            lon="LONGITUD",
                            color=np.log10(df2[desc_color]),

                            # size=desc_size,
                            hover_name='city',
                            hover_data={'city': True,
                                        'LATITUD': False,
                                        'LONGITUD': False},
                            color_continuous_scale=px.colors.sequential.Plotly3,
                            size_max=15,
                            zoom=2,  # CAMBIAR ESTE VALOR
                            #center=dict(lat=4.61, lon=-74.12)

                            )

    fig.update_layout(
        margin=dict(l=10, r=0, t=0, b=50),
        height=500

    )

    return fig;


# Funcion visualizacion red (calcula dentro el algoritmo de layout) -- parametro red networkx Gu
# Devuelve un objeto Figure
def gen_network_graph(Gu, divisor, title, desc, px, city):
    # number of nodes, edges network
    N = Gu.number_of_nodes()
    V = Gu.number_of_edges()

    # if not (os.path.exists(
    #        os.path.join(getRootPath(), 'data/positionsNetworks/' + city + '/Laytout_' + desc + '_px_' + str(px)))):
    #    pos = calc_positions(Gu, px, desc, city)

    # with open(os.path.join(getRootPath(), 'data/positionsNetworks/' + city + '/Laytout_' + desc + '_px_' + str(px)),
    #          'rb') as f:
    #    pos = pickle.load(f)

    # Layout algortithm
    # pos = nx.spring_layout(Gu)

    pos = calc_positions(Gu)  # , px, desc, city)

    # Construccion red
    Xv = [pos[k][0] for k in Gu.nodes()]
    Yv = [pos[k][1] for k in Gu.nodes()]
    Xed = []
    Yed = []
    for edge in Gu.edges():
        Xed += [pos[edge[0]][0], pos[edge[1]][0], None]
        Yed += [pos[edge[0]][1], pos[edge[1]][1], None]

    trace1 = go.Scatter(
        x=Xed,
        y=Yed,
        mode='lines',
        line=dict(
            color='rgb(210,210,210)',
            width=1
        ),

        hoverinfo='none'
    )

    trace2 = go.Scatter(
        x=Xv,
        y=Yv,
        mode='markers',
        name='net',
        marker=dict(
            symbol='circle-dot',
            size=[Gu.degree[node] / divisor for node in Gu.nodes()],  # Size is degree of node
            color='#6959CD',  # Se puede llamar a un array
            line=dict(
                color='rgb(1,1,1)',
                width=1
            )
        ),

        # Label of nodes -
        text=[' #degree: ' + str(Gu.degree[node]) for node in Gu.nodes()],
        hoverinfo='text'
    )

    layout2d = go.Layout(
        # title=title,
        width=1000,
        height=500,
        showlegend=False,
        xaxis={
            'showgrid': False,
            'visible': False
        },
        yaxis={
            'showgrid': False,
            'showline': False,
            'zeroline': False,
            # 'autorange':'reversed',
            'visible': False
        },

        margin=dict(r=0, l=0, t=50, b=0),
        # hovermode='closest',

        paper_bgcolor='rgba(0,0,0,0)',  # Sets the background color of the paper where the graph is drawn
        plot_bgcolor='rgba(0,0,0,0)'  # Sets the background color of the plotting area in-between x and y axes.
    )

    data = [trace1, trace2]
    fig_net = go.Figure(data=data, layout=layout2d)
    return fig_net


def gen_network_graph_3D(Gu, divisor, title):
    # number of nodes, edges network
    N = Gu.number_of_nodes()
    V = Gu.number_of_edges()

    G = Gu

    G_new = nx.convert_node_labels_to_integers(G)
    pos = nx.spring_layout(G_new, dim=3)

    Xn = [pos[k][0] for k in range(N)]  # x-coordinates of nodes
    Yn = [pos[k][1] for k in range(N)]  # y-coordinates
    Zn = [pos[k][2] for k in range(N)]  # z-coordinates

    Xe = []
    Ye = []
    Ze = []
    for e in G_new.edges():
        Xe += [pos[e[0]][0], pos[e[1]][0], None]  # x-coordinates of edge ends
        Ye += [pos[e[0]][1], pos[e[1]][1], None]
        Ze += [pos[e[0]][2], pos[e[1]][2], None]
    axis = dict(
        showbackground=False,
        showline=False,
        zeroline=False,
        showgrid=False,
        showticklabels=False,
        title=''
    )

    trace1 = go.Scatter3d(
        x=Xe,
        y=Ye,
        z=Ze,
        mode='lines',
        line=dict(
            color='rgb(210,210,210)',
            width=1
        ),
        opacity=0.7,
        hoverinfo='none'
    )

    trace2 = go.Scatter3d(
        x=Xn,
        y=Yn,
        z=Zn,
        name='net',
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=[G.degree[node] / divisor for node in G.nodes()],
            color='#6959CD',
            line=dict(
                color='rgb(1,1,1)',
                width=1
            ),
            opacity=0.9
        ),
        text=['Degree: ' + str(G.degree[node]) for node in G.nodes()]
    )

    layout = go.Layout(
        hovermode='closest',
        title='',
        height=500,
        showlegend=False,
        margin=dict(r=0, l=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',  # Sets the background color of the paper where the graph is drawn
        plot_bgcolor='rgba(0,0,0,0)',  # Sets the background color of the plotting area in-between x and y axes.
        scene=dict(
            xaxis=dict(axis),
            yaxis=dict(axis),
            zaxis=dict(axis),
        ),
    )
    data = [trace1, trace2]
    graph = go.Figure(data=data, layout=layout)

    return graph


# Pensar la posibilidad de que en el heatmap se pinten solo los valores de la red o del mapa seleccionados????
def paint_heatmap(df, list_descs):
    # antennas_list = df[['antenna']].values.tolist()

    print('Ha entrado')

    df_descs = df[list_descs]
    df_norm = normalize_df(df_descs)
    print('ya ha normalizado')

    annotatedvalues = df_descs.values.tolist()
    annotatedvalues_r = [[np.round(float(i), 3) for i in nested] for nested in annotatedvalues]
    print('redondeado DONE')

    list_norm_values = df_norm.values.tolist()
    # list_norm_values_r = [[np.round(float(i), 3) for i in nested] for nested in list_norm_values]

    labels = list_descs




    fig = ff.create_annotated_heatmap(list_norm_values,
                                      x=labels,
                                      annotation_text=annotatedvalues_r,
                                      text=annotatedvalues,
                                      hoverinfo='text',
                                      colorscale='Greys',  # Posible cambiar la escala de colores por Viridis
                                      showscale=True)
    print('fig created')
    #for i in range(len(fig.layout.annotations)):
    #    fig.layout.annotations[i].font.size = 8
    fig['layout']['xaxis'].update(side='bottom')
    print('fin heatmap')

    return fig
