"""
This script was created at 09-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import os
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from s0_cases_dictionaries import dict_cases
cases = list(dict_cases)
cases.sort()


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Init app
    app = dash.Dash(__name__)

    app.title = 'Results'

    app.layout = html.Div([

        html.H1('Results', style={'textAlign': 'center'}),

        html.H2('Figure 1'),
        html.P('Case:'),
        dcc.Dropdown(
            id='case1',
            options=[{'value': x, 'label': x} for x in cases],
            value='case01'),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen1',
            options=[{'value': x, 'label': x} for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}),
        html.P('Metrics:'),
        dcc.RadioItems(
            id='x-axis1',
            options=[{'value': x, 'label': x} for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData', 'NumOfAtt',
                                                        'FRR_trn', 'FRRConf_trn', 'NumOfUnlocks_trn',
                                                        'FRR_tst', 'FRRConf_tst', 'NumOfUnlocks_tst',
                                                        'FAR', 'NumOfAcceptTL', 'NumOfAcceptS', 'NumOfAcceptG']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='plot1'),

        html.H2('Figure 2'),
        html.P('Case:'),
        dcc.Dropdown(
            id='case2',
            options=[{'value': x, 'label': x} for x in cases],
            value='case01'),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen2',
            options=[{'value': x, 'label': x} for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}),
        html.P('Metrics:'),
        dcc.RadioItems(
            id='x-axis2',
            options=[{'value': x, 'label': x} for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData', 'NumOfAtt',
                                                        'FRR_trn', 'FRRConf_trn', 'NumOfUnlocks_trn',
                                                        'FRR_tst', 'FRRConf_tst', 'NumOfUnlocks_tst',
                                                        'FAR', 'NumOfAcceptTL', 'NumOfAcceptS', 'NumOfAcceptG']],
            value='FAR',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='plot2')
    ])

    @app.callback(
        [Output('plot1', 'figure'),
         Output('plot2', 'figure')],
        [Input('case1', 'value'),
         Input('screen1', 'value'),
         Input('x-axis1', 'value'),
         Input('case2', 'value'),
         Input('screen2', 'value'),
         Input('x-axis2', 'value')])
    def generate_chart(c1, s1, x1, c2, s2, x2):

        temp = ['FRR_trn', 'FRRConf_trn', 'FRR_tst', 'FRRConf_tst', 'FAR']

        results_path1 = os.path.join('cases', c1, s1, 'results.csv')
        results1 = pd.read_csv(results_path1)
        fig1 = px.bar(results1, x=x1, y='OriginalUser', color='Module', orientation='h', barmode="group")
        if x1 in temp:
            fig1.update_xaxes(range=[0, 1])

        results_path2 = os.path.join('cases', c2, s2, 'results.csv')
        results2 = pd.read_csv(results_path2)
        fig2 = px.bar(results2, x=x2, y='OriginalUser', color='Module', orientation='h', barmode="group")
        if x2 in temp:
            fig2.update_xaxes(range=[0, 1])

        return fig1, fig2

    # Run
    app.run_server(debug=True, port=8051)
