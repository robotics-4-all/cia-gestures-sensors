"""
This script was created at 05-Nov-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import json
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from s0_cases_dictionaries import dict_cases


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Parameters
    case = 'case11'
    exp = '01'
    screens = ['Reacton', 'Memoria', 'Speedy']
    # screens = ['Mathisis', 'Focus', 'Reacton']

    # Load results
    path_save = os.path.join(os.path.dirname(__file__), '04_01_GridSearch_results_' + case + '_' + exp + '.json')
    f = open(path_save, )
    results = json.load(f)

    # Init app
    title = 'GridSearch Results ' + case

    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.P('Screen:'),
        dcc.RadioItems(
            id='screen',
            options=[{'value': x, 'label': x}
                     for x in screens],
            value=screens[0],
            labelStyle={'display': 'inline-block'}
        ),

        html.P('Data:'),
        dcc.RadioItems(
            id='data',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr', 'ges']],
            value='ges',
            labelStyle={'display': 'inline-block'}
        ),

        html.P('Metrics:'),
        dcc.RadioItems(
            id='metric',
            options=[{'value': x, 'label': x}
                     for x in ['FRR', 'FAR']],
            value='FRR',
            labelStyle={'display': 'inline-block'}
        ),

        dcc.Graph(id='graph'),
    ])

    @app.callback(
        Output('graph', 'figure'),
        [Input('screen', 'value'),
         Input('data', 'value'),
         Input('metric', 'value')])
    def generate_heatmap(screen, data, metric):
        fig = px.imshow(results[screen][data][metric],
                        labels=dict(x='Gamma', y='Nu', color=metric, range_color=[0, 1]),
                        x=['>'+str(n) for n in results['gammas']], y=['>'+str(n) for n in results['nus']])
        fig.update_xaxes(side="top")
        return fig

    # Run
    app.run_server(debug=True)
