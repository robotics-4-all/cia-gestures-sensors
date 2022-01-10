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

    # Parameters
    title = 'Sensors Window & Overlap Selection - BoxPlots'

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
                     for x in ['case4', 'case5', 'case8']],
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
        html.P('Sensor:'),
        dcc.RadioItems(
            id='sns1',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Parameter:'),
        dcc.RadioItems(
            id='par1',
            options=[{'value': x, 'label': x}
                     for x in ['Window', 'Overlap']],
            value='Window',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Metrics:'),
        dcc.RadioItems(
            id='x-axis1',
            options=[{'value': x, 'label': x}
                     for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData', 'NumOfAtt',
                               'FRR_trn', 'FRR_tst', 'FAR']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='box-plot1'),

        html.H2('Figure 2'),
        html.P('Case:'),
        dcc.RadioItems(
            id='case2',
            options=[{'value': x, 'label': x}
                     for x in ['case4', 'case5', 'case8']],
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
        html.P('Sensor:'),
        dcc.RadioItems(
            id='sns2',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Parameter:'),
        dcc.RadioItems(
            id='par2',
            options=[{'value': x, 'label': x}
                     for x in ['Window', 'Overlap']],
            value='Window',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Metrics:'),
        dcc.RadioItems(
            id='x-axis2',
            options=[{'value': x, 'label': x}
                     for x in ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData', 'NumOfAtt',
                               'FRR_trn', 'FRR_tst', 'FAR']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='box-plot2')
    ])

    @app.callback(
        [Output('box-plot1', 'figure'),
         Output('box-plot2', 'figure')],
        [Input('case1', 'value'),
         Input('screen1', 'value'),
         Input('sns1', 'value'),
         Input('par1', 'value'),
         Input('x-axis1', 'value'),
         Input('case2', 'value'),
         Input('screen2', 'value'),
         Input('sns2', 'value'),
         Input('par2', 'value'),
         Input('x-axis2', 'value')]
    )
    def generate_chart(c1, s1, sn1, p1, x1, c2, s2, sn2, p2, x2):

        temp = ['FRR_trn', 'FRRConf_trn', 'FRR_tst', 'FRRConf_tst', 'FAR']

        results_path1 = os.path.join('cases', c1, s1, 'results.csv')
        results1 = pd.read_csv(results_path1)
        results1 = results1.loc[results1['Module'] == sn1]
        fig1 = px.box(results1, x=x1, y='Module', color=p1)
        fig1.update_traces(boxmean='sd', boxpoints=False)
        if x1 in temp:
            fig1.update_xaxes(range=[0, 1])

        results_path2 = os.path.join('cases', c2, s2, 'results.csv')
        results2 = pd.read_csv(results_path2)
        results2 = results2.loc[results2['Module'] == sn2]
        fig2 = px.box(results2, x=x2, y='Module', color=p2)
        fig2.update_traces(boxmean='sd', boxpoints=False)
        if x2 in temp:
            fig2.update_xaxes(range=[0, 1])

        return fig1, fig2

    # Run
    app.run_server(debug=True)
