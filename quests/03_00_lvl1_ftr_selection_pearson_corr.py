"""
This script was created at 29-Dec-21
author: eachrist

"""
#  ============ #
#    Imports    #
# ============= #
import itertools
import os
import numpy as np
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

    cases = ['case05']
    screens = ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']
    modules = ['acc', 'gyr', 'swp']

    # Parameters
    title = 'Level 1 Feature Selection - Pearson Correlation'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title),

        html.Div([
            html.H2('Parameters'),
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
            html.H2('Figure'),
            dcc.Graph(id='plot')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'})

    ])


    @app.callback(
        Output('plot', 'figure'),
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('module', 'value')]
    )
    def generate_chart(c, s, m):

        features_dict = {
            'acc': {
                'lvl0_features': dict_cases[c]['FeatureExtraction']['sns']['lvl0_ftr']['acc'],
                'lvl1_features': {
                    'unique': [],
                    'lvl0_depended': ['Mean', 'STD', 'Max', 'Min', 'Range',
                                      'Percentile25', 'Percentile50', 'Percentile75',
                                      'Kurtosis', 'Skewness',
                                      'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']},
                'final_features': []},

            'gyr': {
                'lvl0_features': dict_cases[c]['FeatureExtraction']['sns']['lvl0_ftr']['gyr'],
                'lvl1_features': {
                    'unique': [],
                    'lvl0_depended': ['Mean', 'STD', 'Max', 'Min', 'Range',
                                      'Percentile25', 'Percentile50', 'Percentile75',
                                      'Kurtosis', 'Skewness',
                                      'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']},
                'final_features': []},

            'swp': {
                'final_features': ['Duration', 'MeanX', 'MeanY',
                                   'TraceLength', 'StartStopLength', 'TraceProjection', 'ScreenPercentage',
                                   'StartVelocity', 'StopVelocity', 'AccelerationHor', 'AccelerationVer',
                                   'Slope', 'MeanSquareError', 'MeanAbsError', 'MedianAbsError', 'CoefDetermination']}}

        for md in ['acc', 'gyr']:
            temp = features_dict[md]['lvl1_features']['unique'] + \
                   ['_'.join(ftr) for ftr in itertools.product(features_dict[md]['lvl1_features']['lvl0_depended'],
                                                               features_dict[md]['lvl0_features'])]
            features_dict[md]['final_features'] = temp + ['Entropy_magnitude']

        features = features_dict[m]['final_features']
        if m == 'swp':
            m = 'ges'
        data_path = os.path.join('cases', c, s, 'ftr_' + m + '.csv')
        data = pd.read_csv(data_path)
        if m == 'ges':
            data = data.loc[data['Type'] == 'swipe']

        # Compute correlation
        users = list(set(data['User']))
        corr = data.loc[data['User'] == users[0]][features].corr()
        for user in users[1:]:
            user_data = data.loc[data['User'] == user][features]
            user_corr = user_data.corr()
            corr += user_corr
        corr /= len(users)
        mask = np.triu(np.ones_like(corr, dtype=bool))
        corr = corr.mask(mask)

        # Compute absolute sum of correlation for its feature
        abs_sums = []
        for i in range(corr.shape[0]):
            temp = 0
            for j in range(i - 1, -1, -1):
                temp += abs(corr.at[corr.index[i], corr.columns[j]])
            for j in range(i + 1, corr.shape[0]):
                temp += abs(corr.at[corr.index[j], corr.columns[i]])
            abs_sums.append(temp)

        # Create hover text
        hovertext = list()
        for yi, yy in enumerate(corr.index):
            hovertext.append(list())
            for xi, xx in enumerate(corr.columns):
                if yi == xi:
                    hovertext[-1].append('f: {}<br />abs_sum: {}'.format(yy, abs_sums[yi]))
                elif yi > xi:
                    hovertext[-1].append(
                        'f1: {} abs_sum: {}<br />f2: {} abs_sum: {}<br />corr: {}'.format(yy, abs_sums[yi],
                                                                                          xx, abs_sums[xi],
                                                                                          corr.at[yy, xx]))
                elif yi < xi:
                    hovertext[-1].append('')

        # Make figure
        fig = go.Figure(data=go.Heatmap(z=corr, x=corr.columns, y=corr.columns,
                                        zmin=-1, zmax=1, xgap=1, ygap=1, colorscale='Viridis',
                                        hoverinfo='text', text=hovertext))
        fig.update_layout(
            title_text='Corrplot - ' + m, width=1000, height=1000,
            yaxis_autorange='reversed', yaxis_showgrid=False, xaxis_showgrid=False)

        return fig

    # Run
    app.run_server(debug=True)
