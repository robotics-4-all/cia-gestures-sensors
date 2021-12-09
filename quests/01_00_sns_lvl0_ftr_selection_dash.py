"""
This script was created at 14-Nov-21
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

    # Parameters
    title = 'SensorsFeatureSelection Level 0'

    # Init app
    app = dash.Dash(__name__)

    app.title = title

    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.P('Case:'),
        dcc.Dropdown(
            id='case',
            options=[{'value': x, 'label': x}
                     for x in list(dict_cases)],
            value='case1'
        ),

        html.P('Screen:'),
        dcc.RadioItems(
            id='screen',
            options=[{'value': x, 'label': x}
                     for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}
        ),

        html.P('Data:'),
        dcc.RadioItems(
            id='data',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),

        html.P('X Axis:'),
        dcc.RadioItems(
            id='x-axis',
            options=[{'value': x, 'label': x}
                     for x in ['x', 'y', 'z', 'magnitude', 'combine_angle']],
            value='magnitude',
            labelStyle={'display': 'inline-block'}
        ),

        html.P('Y Axis:'),
        dcc.RadioItems(
            id='y-axis',
            options=[{'value': x, 'label': x}
                     for x in ['None', 'user']],
            value='None',
            labelStyle={'display': 'inline-block'}
        ),

        html.P('Additional Info:'),
        dcc.RadioItems(
            id='add_info',
            options=[{'value': x, 'label': x}
                     for x in ['None', 'Mean', 'Mean + Std']],
            value='Mean',
            labelStyle={'display': 'inline-block'}
        ),

        html.P("Figure Height"),
        dcc.Slider(id='height', min=500, max=5000, step=500, value=500),

        dcc.Graph(id='box-plot'),
    ])

    add_info_dict = {
        'None': False,
        'Mean': True,
        'Mean + Std': 'sd'
    }

    @app.callback(
        Output('box-plot', 'figure'),
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('data', 'value'),
         Input('x-axis', 'value'),
         Input('y-axis', 'value'),
         Input('height', 'value'),
         Input('add_info', 'value')])
    def generate_chart(case, screen, data, x, y, height, add_info):

        data_path = os.path.join('cases', case, screen, 'df_' + data + '.csv')
        df_data = pd.read_csv(data_path)

        if y == 'None':
            y = None
        fig = px.box(df_data, x=x, y=y, height=height)
        fig.update_traces(boxmean=add_info_dict[add_info])
        return fig

    # Run
    app.run_server(debug=True)
