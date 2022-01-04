"""
This script was created at 29-Dec-21
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
from s0_cases_dictionaries import dict_cases


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Parameters
    title = 'Level 1 Feature Selection - Pearson Correlation'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.P('Case:'),
        dcc.Dropdown(
            id='case',
            options=[{'value': x, 'label': x}
                     for x in ['case6']],
            value='case6'
        ),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen',
            options=[{'value': x, 'label': x}
                     for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],  # 'Memoria', 'Speedy' have only taps
            value='Mathisis',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Module:'),
        dcc.RadioItems(
            id='module',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr', 'swp']],  # taps only has duration
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='graph')
    ])

    @app.callback(
        Output('graph', 'figure'),
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('module', 'value')]
    )
    def generate_chart(case, screen, module):

        features_dict = {
            'acc': ['Window', 'Mean', 'STD', 'Max', 'Min', 'Range',
                    'Percentile25', 'Percentile50', 'Percentile75',
                    'Entropy', 'Kurtosis', 'Skewness',
                    'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency'],

            'gyr': ['Window', 'Mean', 'STD', 'Max', 'Min', 'Range',
                    'Percentile25', 'Percentile50', 'Percentile75',
                    'Entropy', 'Kurtosis', 'Skewness',
                    'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency'],

            'swp': ['Duration', 'MeanX', 'MeanY',
                    'TraceLength', 'StartStopLength', 'TraceProjection', 'ScreenPercentage',
                    'StartVelocity', 'StopVelocity', 'AccelerationHor', 'AccelerationVer',
                    'Slope', 'MeanSquareError', 'MeanAbsError', 'MedianAbsError', 'CoefDetermination']
        }

        features = features_dict[module]
        if module == 'swp':
            module = 'ges'
        data_path = os.path.join('cases', case, screen, 'ftr_' + module + '.csv')
        data = pd.read_csv(data_path)
        if module == 'ges':
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
                    hovertext[-1].append('f1: {}<br />f2: {}<br />corr: {}'.format(yy, xx, corr.at[yy, xx]))
                elif yi < xi:
                    hovertext[-1].append('')

        # Make figure

        fig = go.Figure(data=go.Heatmap(z=corr, x=corr.columns, y=corr.columns,
                                        zmin=-1, zmax=1, xgap=1, ygap=1, colorscale='Viridis',
                                        hoverinfo='text', text=hovertext))
        fig.update_layout(
            title_text='Corrplot',
            yaxis_autorange='reversed', width=800, height=800,
            xaxis_showgrid=False, yaxis_showgrid=False,
        )

        return fig

    # Run
    app.run_server(debug=True)
