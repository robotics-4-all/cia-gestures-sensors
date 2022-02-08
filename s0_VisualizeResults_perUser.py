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


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    cases = list(dict_cases)
    cases.sort()
    screens = ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']
    metrics = ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData', 'NumOfAtt',
               'FRR_trn', 'FRRConf_trn', 'NumOfUnlocks_trn',
               'FRR_tst', 'FRRConf_tst', 'NumOfUnlocks_tst',
               'FAR', 'NumOfAcceptTL', 'NumOfAcceptS', 'NumOfAcceptG']

    # Init app
    app = dash.Dash(__name__)
    app.title = 'Results per Users'
    app.layout = html.Div([

        html.H1('Results per User'),

        html.Div([
            html.H2('Overall Parameters'),
            html.P('Screen:'),
            dcc.RadioItems(
                id='screen', options=[{'value': x, 'label': x} for x in screens], value='Mathisis',
                labelStyle={'display': 'inline-block'}),
        ], style={'display': 'block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

        html.Div([
            html.H2('Figure 1'),
            html.P('Case:'),
            dcc.Dropdown(
                id='case1', options=[{'value': x, 'label': x} for x in cases], value=cases[0]),
            html.P('DropUsers:'),
            dcc.RadioItems(
                id='users1', options=[{'value': x, 'label': x} for x in ['Yes', 'No']], value='No',
                labelStyle={'display': 'inline-block'}),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric1', options=[{'value': x, 'label': x} for x in metrics], value='FRRConf_tst'),
            html.P('Size Parameter:'),
            dcc.Slider(
                id='slider1', min=300, max=1500, step=300, value=600,
                tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='plot1')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

        html.Div([
            html.H2('Figure 2'),
            html.P('Case:'),
            dcc.Dropdown(
                id='case2', options=[{'value': x, 'label': x} for x in cases], value=cases[0]),
            html.P('DropUsers:'),
            dcc.RadioItems(
                id='users2', options=[{'value': x, 'label': x} for x in ['Yes', 'No']], value='No',
                labelStyle={'display': 'inline-block'}),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric2', options=[{'value': x, 'label': x} for x in metrics], value='NumOfAcceptTL'),
            html.P('Size Parameter:'),
            dcc.Slider(
                id='slider2', min=300, max=1500, step=300, value=600,
                tooltip={"placement": "bottom", "always_visible": True}),
            dcc.Graph(id='plot2')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),
    ])

    @app.callback(
        [Output('plot1', 'figure'),
         Output('plot2', 'figure')],
        [Input('screen', 'value'),
         Input('case1', 'value'),
         Input('users1', 'value'),
         Input('metric1', 'value'),
         Input('slider1', 'value'),
         Input('case2', 'value'),
         Input('users2', 'value'),
         Input('metric2', 'value'),
         Input('slider2', 'value')])
    def generate_chart(s, c1, u1, m1, s1, c2, u2, m2, s2):

        results_name1 = 'results.csv' if u1 == 'No' else 'results_1.csv'
        results_path1 = os.path.join('cases', c1, s, results_name1)
        results1 = pd.read_csv(results_path1)
        fig1 = px.bar(results1, x=m1, y='OriginalUser', color='Module', orientation='h', barmode="group")
        numb_of_users1 = len(list(set(results1['OriginalUser'].to_list())))
        fig1.update_layout(title_text='BarPlots - ' + m1 + ' - ' + str(numb_of_users1) + ' Users')
        fig1.update_layout(width=1000, height=s1)
        fig1.update_yaxes(categoryorder='category descending')

        results_name2 = 'results.csv' if u2 == 'No' else 'results_1.csv'
        results_path2 = os.path.join('cases', c2, s, results_name2)
        results2 = pd.read_csv(results_path2)
        fig2 = px.bar(results2, x=m2, y='OriginalUser', color='Module', orientation='h', barmode="group")
        numb_of_users2 = len(list(set(results2['OriginalUser'].to_list())))
        fig2.update_layout(title_text='BarPlots - ' + m2 + ' - ' + str(numb_of_users2) + ' Users')
        fig2.update_layout(width=1000, height=s2)
        fig2.update_yaxes(categoryorder='category descending')

        return fig1, fig2

    # Run
    app.run_server(debug=True, port=8051)
