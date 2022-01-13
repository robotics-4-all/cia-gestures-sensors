"""
This script was created at 27-Dec-21
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


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    cases = ['case04', 'case07']

    # Parameters
    title = 'Sensors Window & Overlap Selection - BoxPlots'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.P('Case:'),
        dcc.RadioItems(
            id='case',
            options=[{'value': x, 'label': x} for x in cases],
            value=cases[0],
            labelStyle={'display': 'inline-block'}),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen',
            options=[{'value': x, 'label': x} for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}),
        html.P('Module:'),
        dcc.RadioItems(
            id='module',
            options=[{'value': x, 'label': x} for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}),

        html.H2('Figure 1'),
        html.P('Parameter:'),
        dcc.RadioItems(
            id='par1',
            options=[{'value': x, 'label': x} for x in ['Window', 'Overlap']],
            value='Window',
            labelStyle={'display': 'inline-block'}),
        html.P('Metrics:'),
        dcc.RadioItems(
            id='met1',
            options=[{'value': x, 'label': x} for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData',
                                                        'FRR_trn', 'FRR_tst', 'FAR']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='box-plot1'),

        html.H2('Figure 2'),
        html.P('Parameter:'),
        dcc.RadioItems(
            id='par2',
            options=[{'value': x, 'label': x} for x in ['Window', 'Overlap']],
            value='Window',
            labelStyle={'display': 'inline-block'}),
        html.P('Metrics:'),
        dcc.RadioItems(
            id='met2',
            options=[{'value': x, 'label': x} for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData',
                                                        'FRR_trn', 'FRR_tst', 'FAR']],
            value='FAR',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='box-plot2')
    ])

    @app.callback(
        [Output('box-plot1', 'figure'),
         Output('box-plot2', 'figure')],
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('module', 'value'),
         Input('par1', 'value'),
         Input('met1', 'value'),
         Input('par2', 'value'),
         Input('met2', 'value')]
    )
    def generate_chart(c, s, m, p1, met1, p2, met2):

        temp = ['FRR_trn', 'FRRConf_trn', 'FRR_tst', 'FRRConf_tst', 'FAR']

        results_path = os.path.join('cases', c, s, 'results.csv')
        results = pd.read_csv(results_path)
        results = results.loc[results['Module'] == m]

        fig1 = px.box(results, x=met1, y='Module', color=p1)
        fig1.update_traces(boxmean='sd', boxpoints=False)
        if met1 in temp:
            fig1.update_xaxes(range=[0, 1])

        fig2 = px.box(results, x=met2, y='Module', color=p2)
        fig2.update_traces(boxmean='sd', boxpoints=False)
        if met2 in temp:
            fig2.update_xaxes(range=[0, 1])

        return fig1, fig2

    # Run
    app.run_server(debug=True)
