"""
This script was created at 17-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from s0_cases_dictionaries import dict_cases


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Parameters
    title = 'Sensors Window & Overlap Selection - HeatMaps'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.H2('Figure 1'),
        html.P('Case:'),
        dcc.RadioItems(
            id='case1',
            options=[{'value': x, 'label': x}
                     for x in ['case4', 'case5']],
            value='case4',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen1',
            options=[{'value': x, 'label': x}
                     for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Module:'),
        dcc.RadioItems(
            id='module1',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Metric:'),
        dcc.RadioItems(
            id='metric1',
            options=[{'value': x, 'label': x}
                     for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData', 'NumOfAtt',
                               'FRR_trn', 'FRR_tst', 'FAR']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='graph1'),

        html.H2('Figure 2'),
        html.P('Case:'),
        dcc.RadioItems(
            id='case2',
            options=[{'value': x, 'label': x}
                     for x in ['case4', 'case5']],
            value='case5',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen2',
            options=[{'value': x, 'label': x}
                     for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Module:'),
        dcc.RadioItems(
            id='module2',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Metric:'),
        dcc.RadioItems(
            id='metric2',
            options=[{'value': x, 'label': x}
                     for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData', 'NumOfAtt',
                               'FRR_trn', 'FRR_tst', 'FAR']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='graph2')
    ])

    @app.callback(
        [Output('graph1', 'figure'),
         Output('graph2', 'figure')],
        [Input('case1', 'value'),
         Input('screen1', 'value'),
         Input('module1', 'value'),
         Input('metric1', 'value'),
         Input('case2', 'value'),
         Input('screen2', 'value'),
         Input('module2', 'value'),
         Input('metric2', 'value')]
    )
    def generate_chart(c1, s1, m1, met1, c2, s2, m2, met2):

        results_path1 = os.path.join('cases', c1, s1, 'results.csv')
        results1 = pd.read_csv(results_path1)
        windows = ['_' + str(x) for x in dict_cases[c1]['GetResults']['FeatureExtraction']['sns']['window']]
        overlaps = ['_' + str(x) for x in dict_cases[c1]['GetResults']['FeatureExtraction']['sns']['overlap']]
        metric_means1 = pd.DataFrame(index=windows, columns=overlaps)
        for window in dict_cases[c1]['GetResults']['FeatureExtraction']['sns']['window']:
            for overlap in dict_cases[c1]['GetResults']['FeatureExtraction']['sns']['overlap']:
                sr = results1.loc[(results1['Module'] == m1) &
                                  (results1['Window'] == window) &
                                  (results1['Overlap'] == overlap)][met1]
                metric_means1.at['_' + str(window), '_' + str(overlap)] = sr.mean()

        # Make figure
        fig1 = go.Figure(data=go.Heatmap(z=metric_means1, x=overlaps, y=windows, xgap=1, ygap=1, colorscale='Viridis'))
        fig1.update_layout(title_text='Corrplot', width=len(windows) * 100, height=len(overlaps) * 100)
        fig1.update_xaxes(title='Overlap')
        fig1.update_yaxes(title='Window')

        results_path2 = os.path.join('cases', c2, s2, 'results.csv')
        results2 = pd.read_csv(results_path2)
        windows = ['_' + str(x) for x in dict_cases[c2]['GetResults']['FeatureExtraction']['sns']['window']]
        overlaps = ['_' + str(x) for x in dict_cases[c2]['GetResults']['FeatureExtraction']['sns']['overlap']]
        metric_means2 = pd.DataFrame(index=windows, columns=overlaps)
        for window in dict_cases[c2]['GetResults']['FeatureExtraction']['sns']['window']:
            for overlap in dict_cases[c2]['GetResults']['FeatureExtraction']['sns']['overlap']:
                sr = results2.loc[(results2['Module'] == m2) &
                                  (results2['Window'] == window) &
                                  (results2['Overlap'] == overlap)][met2]
                metric_means2.at['_' + str(window), '_' + str(overlap)] = sr.mean()

        # Make figure
        fig2 = go.Figure(data=go.Heatmap(z=metric_means2, x=overlaps, y=windows, xgap=1, ygap=1, colorscale='Viridis'))
        fig2.update_layout(title_text='Corrplot', width=len(windows) * 100, height=len(overlaps) * 100)
        fig2.update_xaxes(title='Overlap')
        fig2.update_yaxes(title='Window')

        return fig1, fig2

    # Run
    app.run_server(debug=True)
