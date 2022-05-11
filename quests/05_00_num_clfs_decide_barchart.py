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

    cases = ['case10', 'case19']
    screens = ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']
    metrics = ['FRR_tst', 'FRRConf_tst', 'FAR', 'NumOfAcceptTL']

    # Parameters
    title = 'Number of Classifiers Make the Decision - BarChart'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title),

        html.Div([
            html.H2('Overall Parameters'),
            html.P('Case:'),
            dcc.Dropdown(
                id='case', options=[{'value': x, 'label': x} for x in cases], value=cases[0]),
            html.P('Screen:'),
            dcc.RadioItems(
                id='screen', options=[{'value': x, 'label': x} for x in screens], value='Mathisis',
                labelStyle={'display': 'inline-block'})
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'}),

        html.Br(),

        html.Div([
            html.H2('Figure 1'),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric1', options=[{'value': x, 'label': x} for x in metrics], value='FRR_tst'),
            dcc.Graph(id='plot1')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '2vw'}),

        html.Div([
            html.H2('Figure 2'),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric2', options=[{'value': x, 'label': x} for x in metrics], value='FAR'),
            dcc.Graph(id='plot2')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '2vw'})

    ])

    @app.callback(
        [Output('plot1', 'figure'),
         Output('plot2', 'figure')],
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('metric1', 'value'),
         Input('metric2', 'value')]
    )
    def generate_chart(c, s, met1, met2):

        results_path = os.path.join('cases', c, s, 'results.csv')
        results = pd.read_csv(results_path)
        results = results.dropna()

        fig1 = px.histogram(results, x='Module', y=met1, color='num_of_clf_that_decide',
                            barmode='group', histfunc='avg')
        fig1.update_layout(title_text=met1[:3], width=1000, height=500)
        # fig1.update_layout(title_text='BarPlots - ' + met1 + ' - ' + s, width=1000, height=500)
        fig1.update_xaxes()
        # if met1 != 'NumOfAcceptTL':
        #     fig1.update_yaxes(range=[0, 1])

        fig2 = px.histogram(results, x='Module', y=met2, color='num_of_clf_that_decide',
                            barmode='group', histfunc='avg')
        fig2.update_layout(title_text=met2[:3], width=1000, height=500)
        # fig2.update_layout(title_text='BarPlots - ' + met2 + ' - ' + s, width=1000, height=500)
        # if met2 != 'NumOfAcceptTL':
        #     fig2.update_yaxes(range=[0, 1])

        return fig1, fig2

    # Run
    app.run_server(debug=True)
