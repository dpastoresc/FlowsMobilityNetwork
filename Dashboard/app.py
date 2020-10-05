import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import json
import plotly.figure_factory as ff
import itertools

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt
import plotly.express as px

# DIFERENT FUNCTIONS
from paint.graphs import paint_map, paint_histogram, gen_network_graph, gen_network_graph_3D, paint_heatmap
from utils import getRootPath
from preprocess.process import prepare_descs, get_net_city, filter_network, normalize_df




NDdescs_COL = prepare_descs()[0]

NDdescs_COL_loc = prepare_descs()[1]
# For the dropdown
descs = NDdescs_COL.columns.tolist()
descs = descs[1:(len(descs) - 2)]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

###SLIDER

rangeslider = dcc.RangeSlider(
    id='my-range-slider',
    min=20,
    max=100,
    step=5,
    value=[40, 60]
)

#####DROPDOWNS
dropdown_cities = dcc.Dropdown(
    id='dropdown_cities',
    options=[{'label': 'Bogota', 'value': 'BOG'}, {'label': 'Medellin', 'value': 'MED'}],
    value='BOG',
    placeholder='Select a city'
)

dropdown_descs = dcc.Dropdown(
    id='dropdown_descs',
    options=[{'label': i, 'value': i} for i in descs],
    value='in_degree',
    placeholder='Select a desc'
)
'''
px_c = [75, 80, 90, 95, 97, 99]
dropdown_px_net = dcc.Dropdown(
    id='dropdown_px_net',
    options=[{'label': i, 'value': i} for i in px_c],
    value=95,
    placeholder='Select a px'
)
'''
dropdown_descs2 = dcc.Dropdown(
    id='dropdown_descs2',
    options=[{'label': i, 'value': i} for i in descs],
    value='out_degree',
    placeholder='Select a desc'
)
dims = ['2D', '3D']
dropdown_dim = dcc.Dropdown(
    id='dropdown_dim',
    options=[{'label': i, 'value': i} for i in dims],
    value='3D'
)

dropdown_descSortHM = dcc.Dropdown(
    id='dropdown_descSortHM',
    options=[{'label': i, 'value': i} for i in descs],
    value='in_degree'
)



app.layout = html.Div(

    children=[
        html.Div(
            className='row',
            children=[
                # column for user controls

                html.Div(
                    className="three columns div-user-controls",
                    children=[
                        html.H2("FLOW DESCRIPTORS OF HUMAN MOBILITY NETWORKS"),
                        html.P(
                            """Select a city 
                            """
                        ),

                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                # Place the city dropdown
                                dropdown_cities
                            ]
                        ),
                        html.P(
                            '''Select the Descriptor 1 (will be shown in the histogram 1, the map and the network graph)'''),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                # Place dropdown desc1
                                dropdown_descs
                            ]
                        ),
                        html.P('''Select the Descriptor 2 (will be shown in the histogram 2)'''),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                # Place dropdown desc2
                                dropdown_descs2
                            ]
                        ),

                        #       html.Div(
                        #            className='div-for-dropdown',
                        #            children=[
                        #                # Place dropdown desc2
                        #                dropdown_px_net
                        #            ]
                        #        ),
                        html.P('''Select a range of percentiles to filter the network graph'''),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                # Place dropdown desc2
                                rangeslider
                            ]
                        ),

                        html.Div(id='output-container-range-slider'),
                        html.Br(),
                        html.P('Select a dimension for the network graph'),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                dropdown_dim
                            ]
                        )
                    ]
                ),

                html.Div(
                    className="nine columns div-for-charts bg-grey",
                    style={'overflow': 'auto'},
                    children=[
                        html.Div(
                            className='row',
                            children=[
                                html.Div(
                                    className="six columns div-for-charts bg-grey",
                                    children=[
                                        dcc.Graph(id="histogram"),
                                    ]

                                ),
                                html.Div(
                                    className="six columns div-for-charts bg-grey",
                                    children=[
                                        dcc.Graph(id="histogram2"),
                                    ]

                                ),
                            ],
                            style={'height': '200px'}),

                        html.Div(
                            className='row',
                            children=[dcc.Graph(id='map2')]
                        ),



                        html.Hr(),
                        html.H5('Network graph'),

                        html.P(id="TextNodes"),
                        html.P(id="TextEdges"),
                        dcc.Graph(id='networkgraph'),

                        html.H6('Annotated heatmap for the city selected'),
                        html.P('''Select a descriptor to sort the values ''',
                               style={'padding-left': '1px'}),
                        html.Div(
                            className='div-for-dropdown',
                            children=[
                                # Place the city dropdown
                                dropdown_descSortHM
                            ],
                            style={'margin-right': '800px'}
                        ),

                        dcc.Graph(id='heatmap-graph'),

                    ]
                )

            ]
        )
    ])


@app.callback(
    Output("histogram", "figure"),
    [
        Input('dropdown_cities', "value"),
        Input('dropdown_descs', 'value')
    ]
)
def update_histogram(city, desc):
    column = desc

    df = NDdescs_COL[NDdescs_COL['city'] == city]
    title = 'Histogram of ' + desc + ' for the antennas of ' + city
    label_dict = {desc: desc + ' bill'}
    color = ['#7FA6EE']
    fig = paint_histogram(df, title, column, label_dict, color)

    return fig


@app.callback(
    Output("histogram2", "figure"),
    [
        Input('dropdown_cities', "value"),
        Input('dropdown_descs2', 'value')
    ]
)
def update_histogram2(city, desc):
    column = desc

    df = NDdescs_COL[NDdescs_COL['city'] == city]
    title = 'Histogram of ' + desc + ' for the antennas of ' + city
    label_dict = {desc: desc + ' bill'}
    color = ['rgb(0, 200, 200)']
    fig = paint_histogram(df, title, column, label_dict, color)

    return fig





@app.callback(
    [Output('networkgraph', 'figure'),
     Output('TextNodes', 'children'),
     Output('TextEdges', 'children')],
    [
        Input('dropdown_cities', 'value'),
        Input('dropdown_descs', 'value'),
        Input('my-range-slider', 'value'),
        Input('dropdown_dim', 'value')
    ]
)
def update_netgraph(city, desc, value, dim):
    px = 0
    limit_inf = value[0]
    limit_sup = value[1]
    # Get the dataframe and Network for the city selected
    df_descs_cit = NDdescs_COL[NDdescs_COL['city'] == city]
    Gu = get_net_city(city)

    Gu_f = filter_network(px, desc, Gu, df_descs_cit, limit_inf, limit_sup)
    divisor = 3
    num_nodes = str(len(Gu_f.nodes()))
    num_edges = str(len(Gu_f.edges()))
    title = 'Network graph of ' + city + ' antennas for ' + desc + ' with ' + num_nodes + ' nodes and ' + num_edges + ' edges'

    if dim == '2D':
        fig = gen_network_graph(Gu_f, divisor, title, desc, px, city)
    elif dim == '3D':
        fig = gen_network_graph_3D(Gu_f, divisor, title)

    text_nodes = "Total nodes: {}".format(num_nodes)
    text_edges = "Total edges: {}".format(num_edges)

    return fig, text_nodes, text_edges


@app.callback(
    Output('output-container-range-slider', 'children'),
    [Input('my-range-slider', 'value')])
def update_output(value):
    return 'You have selected {}'.format(value)


# paint_heatmap(df, list_descs)

@app.callback(
    Output('heatmap-graph', 'figure'),
    [Input('dropdown_cities', 'value'),
     Input('dropdown_descSortHM', 'value')]
)
def update_heatmap(city, desc):
    # Based on the city
    city = city
    df_descs_cit = NDdescs_COL[NDdescs_COL['city'] == city]
    descs = df_descs_cit.columns.tolist()
    descs = descs[1:(len(descs) - 2)]

    df = df_descs_cit
    list_descs = descs

    df = df.sort_values(by=desc)

    df = df[:25]

    df_descs = df[list_descs]
    df_norm = normalize_df(df_descs)

    annotatedvalues = df_descs.values.tolist()
    annotatedvalues_r = [[np.round(float(i), 3) for i in nested] for nested in annotatedvalues]

    list_norm_values = df_norm.values.tolist()
    # list_norm_values_r = [[np.round(float(i), 3) for i in nested] for nested in list_norm_values]

    labels = list_descs

    fig = ff.create_annotated_heatmap(list_norm_values,
                                      x=labels,
                                      annotation_text=annotatedvalues_r,
                                      text=annotatedvalues,
                                      hoverinfo='text',
                                      colorscale='Viridis',  # Posible cambiar la escala de colores por Viridis
                                      showscale=True)

    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 8
    fig['layout']['xaxis'].update(side='bottom')

    # fig = paint_heatmap(df_descs_cit, descs)

    return fig


@app.callback(
    Output('map2', 'figure'),
    [
        Input('histogram', 'selectedData'),
        Input('histogram', 'clickData'),
        Input('histogram', 'hoverData'),
        Input('dropdown_cities', "value"),
        Input('dropdown_descs', 'value')
    ]
)
def update_map2(selectedData, clickData, hoverData, city, desc):
    df = NDdescs_COL_loc[NDdescs_COL_loc['city'] == city]
    desc_size = 'in_flow'
    desc_color = desc
    city_label = ''
    if city == 'BOG':
        city_label = 'Bogotá'
    elif city == 'MED':
        city_label = 'Medellin'
    title = 'Map of ' + city_label + ' antennas by ' + desc

    clickData = clickData
    selectedData = selectedData

    if not (clickData or selectedData):
        df = df

    elif selectedData:
        results = selectedData['points']
        points = [results[x]['pointNumbers'] for x in range(0, len(results))]
        dats = list(itertools.chain.from_iterable(points))

        df = df.iloc[dats]

    elif clickData:
        dats = clickData.get('points')[0]['pointNumbers']
        df = df.iloc[dats]

    elif not (clickData or selectedData):
        print('nada')



    fig2 = paint_map(df, desc_color, desc_size, title)
    clickData = None
    selectedData = None

    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)
