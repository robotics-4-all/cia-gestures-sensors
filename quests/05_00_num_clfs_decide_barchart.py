"""
This script was created at 17-Dec-21
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

    cases = ['case10']

    # Parameters
    title = 'Number of Classifiers Make the Decision - BarChart'

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


        html.H2('Figure 1'),
        html.P('Metric:'),
        dcc.RadioItems(
            id='metric1',
            options=[{'value': x, 'label': x} for x in ['FRR_trn', 'FRR_tst', 'FAR']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='graph1'),

        html.H2('Figure 2'),
        html.P('Metric:'),
        dcc.RadioItems(
            id='metric2',
            options=[{'value': x, 'label': x} for x in ['FRR_trn', 'FRR_tst', 'FAR']],
            value='FAR',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='graph2')
    ])

    @app.callback(
        [Output('graph1', 'figure'),
         Output('graph2', 'figure')],
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('metric1', 'value'),
         Input('metric2', 'value')]
    )
    def generate_chart(c, s, met1, met2):

        results_path = os.path.join('cases', c, s, 'results.csv')
        results = pd.read_csv(results_path)

        fig1 = px.histogram(results, x='Module', y=met1, color='num_of_clf_that_decide',
                            barmode='group', histfunc='avg')
        fig1.update_layout(title_text='BarPlot')
        fig1.update_yaxes(range=[0, 1])

        fig2 = px.histogram(results, x='Module', y=met2, color='num_of_clf_that_decide',
                            barmode='group', histfunc='avg')
        fig2.update_layout(title_text='BarPlot')
        fig2.update_yaxes(range=[0, 1])

        return fig1, fig2

    # Run
    app.run_server(debug=True)
