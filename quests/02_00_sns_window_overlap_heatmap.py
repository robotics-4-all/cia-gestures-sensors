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
import plotly.graph_objects as go
from s0_cases_dictionaries import dict_cases

#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    cases = ['case04', 'case07']

    # Parameters
    title = 'Sensors Window & Overlap Selection - HeatMaps'
    screens = ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']
    modules = ['acc', 'gyr']
    metrics = ['NumOfTrnData', 'NumOfTstData', 'NumOfAttData',
               'FRR_trn', 'FRR_tst', 'FAR']

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
                labelStyle={'display': 'inline-block'}),
            html.P('Module:'),
            dcc.RadioItems(
                id='module', options=[{'value': x, 'label': x} for x in modules], value='acc',
                labelStyle={'display': 'inline-block'}),
            html.P('Set ColorBar Range:'),
            dcc.RadioItems(
                id='clr_bar', options=[{'value': x, 'label': x} for x in ['Yes', 'No']], value='No',
                labelStyle={'display': 'inline-block'})
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'}),

        html.Div([
            html.H2('Figure 1'),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric1', options=[{'value': x, 'label': x} for x in metrics], value='FRR_tst'),
            dcc.Graph(id='plot1')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'}),

        html.Div([
            html.H2('Figure 2'),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric2', options=[{'value': x, 'label': x} for x in metrics], value='FAR'),
            dcc.Graph(id='plot2')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'})
    ])

    @app.callback(
        [Output('plot1', 'figure'),
         Output('plot2', 'figure')],
        [Input('clr_bar', 'value'),
         Input('case', 'value'),
         Input('screen', 'value'),
         Input('module', 'value'),
         Input('metric1', 'value'),
         Input('metric2', 'value')]
    )
    def generate_chart(b, c, s, m, met1, met2):

        zmin, zmid, zmax = None, None, None
        if b == 'Yes':
            zmin, zmid, zmax = 0, 0.5, 1

        results_path = os.path.join('cases', c, s, 'results.csv')
        results = pd.read_csv(results_path)
        windows = ['_' + str(x) for x in dict_cases[c]['FeatureExtraction']['sns']['window']]
        overlaps = ['_' + str(x) for x in dict_cases[c]['FeatureExtraction']['sns']['overlap']]
        met_means1 = pd.DataFrame(index=windows, columns=overlaps)
        met_means2 = pd.DataFrame(index=windows, columns=overlaps)
        for window in dict_cases[c]['FeatureExtraction']['sns']['window']:
            for overlap in dict_cases[c]['FeatureExtraction']['sns']['overlap']:
                sr = results.loc[(results['Module'] == m) &
                                 (results['Window'] == window) &
                                 (results['Overlap'] == overlap)]
                met_means1.at['_' + str(window), '_' + str(overlap)] = sr[met1].mean()
                met_means2.at['_' + str(window), '_' + str(overlap)] = sr[met2].mean()

        fig1 = go.Figure(data=go.Heatmap(z=met_means1, zmin=zmin, zmid=zmid, zmax=zmax,
                                         x=overlaps, y=windows, xgap=1, ygap=1, colorscale='Viridis'))
        # fig1.update_layout(title_text='Heatmap - ' + met1 + ' - ' + s + ' - ' + m,
        #                    width=len(overlaps) * 70, height=len(windows) * 70)
        fig1.update_layout(width=len(overlaps) * 70, height=len(windows) * 70)
        fig1.update_layout(title_text=met1[0:3])
        fig1.update_xaxes(title='Overlap')
        fig1.update_yaxes(title='Window')

        fig2 = go.Figure(data=go.Heatmap(z=met_means2, zmin=zmin, zmid=zmid, zmax=zmax,
                                         x=overlaps, y=windows, xgap=1, ygap=1, colorscale='Viridis'))
        # fig2.update_layout(title_text='Heatmap - ' + met2 + ' - ' + s + ' - ' + m,
        #                    width=len(overlaps) * 70, height=len(windows) * 70)
        fig2.update_layout(width=len(overlaps) * 70, height=len(windows) * 70)
        fig2.update_layout(title_text=met2[0:3])
        fig2.update_xaxes(title='Overlap')
        fig2.update_yaxes(title='Window')

        return fig1, fig2

    # Run
    app.run_server(debug=True)
