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

'''
results = {
    'Mathisis': {
        'acc': ['x', 'y', 'magnitude'],
        'gyr': ['x', 'y', 'z', 'magnitude']
    },

    'Focus': {
        'acc': ['x', 'y', 'magnitude'],
        'gyr': ['x', 'y', 'z', 'magnitude']
    },

    'Reacton': {
        'acc': ['x', 'y', 'magnitude'],
        'gyr': ['x', 'y', 'z', 'magnitude']
    },

    'Memoria': {
        'acc': ['x', 'y', 'magnitude'],
        'gyr': ['x', 'y', 'z', 'magnitude']
    },
    'Speedy': {
        'acc': ['x', 'y', 'magnitude'],
        'gyr': ['x', 'y', 'z', 'magnitude']
    }
}

conclusion:
['x', 'y', 'magnitude']
'''


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Load data
    case = 'case2'
    screen = 'Speedy'
    sns = 'gyr'

    sns_ftr_lvl_0 = ['x', 'y', 'z', 'magnitude', 'combine_angle']

    data_path = os.path.join('cases', case, screen, 'df_' + sns + '.csv')
    df_data = pd.read_csv(data_path)
    users = list(set(df_data['user']))

    # Select data

    # option 1
    # df_data
    # corr = df_data[sns_ftr_lvl_0].corr()

    # option 2
    # user = users[0]
    # user_data = df_data.loc[df_data['user'] == user][sns_ftr_lvl_0]
    # corr = user_data.corr()

    # option 3
    corr = df_data.loc[df_data['user'] == users[0]][sns_ftr_lvl_0].corr()
    for user in users[1:]:
        user_data = df_data.loc[df_data['user'] == user][sns_ftr_lvl_0]
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
