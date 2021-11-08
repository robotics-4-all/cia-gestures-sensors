"""
This script was created at 05-Nov-21
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

from _cases_dictionaries import dict_cases


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Parameters
    title = 'Results'

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
            # labelStyle={'display': 'inline-block'}
        ),

        html.P('Screen:'),
        dcc.RadioItems(
            id='screen',
            options=[{'value': x, 'label': x}
                     for x in ['Mathisis', 'Focus']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}
        ),

        html.P('Metrics:'),
        dcc.RadioItems(
            id='x-axis',
            options=[{'value': x, 'label': x}
                     for x in ['NumOfOrgUserTstData', 'FRR', 'FAR', 'NumOfUnlocks', 'FRR_Conf', 'NumOfAcceptTL']],
            value='FRR_Conf',
            labelStyle={'display': 'inline-block'}
        ),

        html.P('Y Axis:'),
        dcc.RadioItems(
            id='y-axis',
            options=[{'value': x, 'label': x}
                     for x in ['Module', 'OriginalUser']],
            value='Module',
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

        dcc.Graph(id='box-plot'),
    ])

    height_dict = {
        'Module': 500,
        'OriginalUser': 2000
    }

    add_info_dict = {
        'None': False,
        'Mean': True,
        'Mean + Std': 'sd'
    }

    @app.callback(
        Output('box-plot', 'figure'),
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('x-axis', 'value'),
         Input('y-axis', 'value'),
         Input('add_info', 'value')])
    def generate_chart(case, screen, x, y, add_info):
        results_path = os.path.join('cases', case, screen, 'results.csv')
        results = pd.read_csv(results_path)
        fig = px.box(results, x=x, y=y, color='Module', height=height_dict[y])
        fig.update_traces(boxmean=add_info_dict[add_info])
        return fig

    # Run
    app.run_server(debug=True)
