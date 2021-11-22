"""
This script was created at 14-Nov-21
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
import plotly.graph_objects as go

from _cases_dictionaries import dict_cases

'''
results = {
    'acc': ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75', 
            'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2'],
    
    'gyr': ['Mean', 'STD', 'Max', 'Min', 'Percentile25', 'Percentile50', 'Percentile75', 
            'Kurtosis', 'Skewness', 'Amplitude2', 'Frequency2']
    
    'ges': ['Duration', 'MeanX', 'MeanY', 'StartStopLength', 'ScreenPercentage',
            'TraceProjection', 'StartVelocity', 'StopVelocity',
            'AccelerationHor', 'AccelerationVer', 'Slope', 'MeanSquareError', 'CoefDetermination']
'''


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Load data
    case = 'case1'
    screen = 'Reacton'
    sns = 'ges'

    sns_ftr_lvl_1 = ['Mean', 'STD', 'Max', 'Min', 'Range', 'Percentile25', 'Percentile50', 'Percentile75',
                     'Kurtosis', 'Skewness', 'Entropy', 'Amplitude1', 'Amplitude2', 'Frequency2', 'MeanFrequency']

    ges_ftr_lvl_1 = ['Duration', 'MeanX', 'MeanY', 'TraceLength', 'StartStopLength', 'ScreenPercentage',
                     'TraceProjection', 'Ratio', 'Deviation', 'Leaning', 'StartVelocity', 'StopVelocity',
                     'AccelerationHor', 'AccelerationVer', 'Slope', 'MeanSquareError', 'MeanAbsError',
                     'MedianAbsError', 'CoefDetermination']

    snss = {
        'acc': sns_ftr_lvl_1,
        'gyr': sns_ftr_lvl_1,
        'ges': ges_ftr_lvl_1,
    }

    data_path = os.path.join('cases', case, screen, 'features_' + sns + '.csv')
    features = pd.read_csv(data_path)
    users = list(set(features['User']))

    # Select data

    # option 1
    # df_data
    # corr = features[sns_ftr_lvl_1].corr()

    # option 2
    # user = users[0]
    # user_data = df_data.loc[df_data['user'] == user][sns_ftr_lvl_0]
    # corr = user_data.corr()

    # option 3
    corr = features.loc[features['User'] == users[0]][snss[sns]].corr()
    for user in users[1:]:
        user_data = features.loc[features['User'] == user][snss[sns]]
        user_corr = user_data.corr()
        corr += user_corr
    corr /= len(users)

    # Make figure
    mask = np.triu(np.ones_like(corr, dtype=bool))
    fig = go.Figure(data=go.Heatmap(z=corr.mask(mask), x=corr.columns, y=corr.columns,
                                    zmin=-1, zmax=1, xgap=1, ygap=1))

    fig.update_layout(
        title_text='Corrplot',
        yaxis_autorange='reversed',
        width=600,
        height=600,
        xaxis_showgrid=False,
        yaxis_showgrid=False,
    )

    app = dash.Dash(__name__)

    app.layout = html.Div([
        dcc.Graph(id="graph", figure=fig),
    ])

    app.run_server(debug=True)

    print('\n')
