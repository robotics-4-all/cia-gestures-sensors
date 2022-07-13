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
    app.title = 'Results'
    app.layout = html.Div([

        html.H1('Results'),

        html.Div([
            html.H2('Overall Parameters'),
            html.P('Screen:'),
            dcc.RadioItems(
                id='screen', options=[{'value': x, 'label': x} for x in screens], value='Mathisis',
                labelStyle={'display': 'inline-block'}),
            html.P('Additional Info:'),
            dcc.RadioItems(
                id='info',
                options=[{'value': x, 'label': x} for x in ['None', 'Mean', 'Mean + Std']], value='Mean + Std',
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
                id='metric1', options=[{'value': x, 'label': x} for x in metrics], value='FAR'),
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
                id='metric2', options=[{'value': x, 'label': x} for x in metrics], value='FRR_tst'),
            dcc.Graph(id='plot2')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '3vw'}),

    ])

    add_info_dict = {
        'None': False,
        'Mean': True,
        'Mean + Std': 'sd'
    }

    @app.callback(
        [Output('plot1', 'figure'),
         Output('plot2', 'figure')],
        [Input('screen', 'value'),
         Input('info', 'value'),
         Input('case1', 'value'),
         Input('users1', 'value'),
         Input('metric1', 'value'),
         Input('case2', 'value'),
         Input('users2', 'value'),
         Input('metric2', 'value')])
    def generate_chart(s, i, c1, u1, m1, c2, u2, m2):
        import plotly.graph_objects as go

        temp = ['FRR_trn', 'FRRConf_trn', 'FRR_tst', 'FRRConf_tst', 'FAR']

        results_name1 = 'results.csv' if u1 == 'No' else 'results_1.csv'
        results_path1 = os.path.join('cases', c1, s, results_name1)
        results1 = pd.read_csv(results_path1)
        results1 = results1.dropna(subset=['FRR_tst', 'FAR'])

        # fig1 = go.Figure()
        # for met in m1:
        #     data = results1[met]
        #     # data = data.dropna()
        #     fig1.add_trace(go.Box(x=data, y=results1['Module'], name=met))
        # fig1.update_layout(boxmode='group')
        # fig1.update_traces(orientation='h', boxmean=add_info_dict[i], boxpoints=False)

        fig1 = px.box(results1, x=m1, y='Module', color='Module')
        fig1.update_traces(boxmean=add_info_dict[i], boxpoints=False)
        # if m1 in temp:
        #     fig1.update_xaxes(range=[0, 1])
        numb_of_users1 = len(list(set(results1['OriginalUser'].to_list())))
        # fig1.update_layout(title_text='BarPlots - ' + m1 + ' - ' + str(numb_of_users1) + ' Users')
        fig1.update_layout(width=500, height=500)
        fig1.update_traces(showlegend=False)

        results_name2 = 'results.csv' if u2 == 'No' else 'results_1.csv'
        results_path2 = os.path.join('cases', c2, s, results_name2)
        results2 = pd.read_csv(results_path2)
        results2 = results2.dropna(subset=['FRR_tst', 'FAR'])

        fig2 = px.box(results2, x=m2, y='Module', color='Module')
        fig2.update_traces(boxmean=add_info_dict[i], boxpoints=False)
        if m2 in temp:
            fig2.update_xaxes(range=[0, 1])
        numb_of_users2 = len(list(set(results2['OriginalUser'].to_list())))
        # fig2.update_layout(title_text='BarPlots - ' + m2 + ' - ' + str(numb_of_users2) + ' Users')
        fig2.update_layout(width=800, height=400)

        return fig1, fig2

    # Run
    app.run_server(debug=True, port=8051)
