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


#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    # Parameters
    case_name = 'case1'
    screen_name = 'Mathisis'
    title = case_name + ' ' + screen_name + ' Results'

    results_path = os.path.join('cases', case_name, screen_name, 'results.csv')
    results = pd.read_csv(results_path)

    # Init app
    app = dash.Dash(__name__)

    app.title = title

    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.P('Metrics:'),
        dcc.RadioItems(
            id='x-axis',
            options=[{'value': x, 'label': x}
                     for x in ['NumOfOrgUserTstData', 'FRR', 'FAR', 'NumOfUnlocks', 'FRR_Conf', 'NumOfAcceptTL']],
            value='FRR_Conf',
            labelStyle={'display': 'inline-block'}
        ),

        html.P("Y Axis:"),
        dcc.RadioItems(
            id='y-axis',
            options=[{'value': x, 'label': x}
                     for x in ['Module', 'OriginalUser', 'Fold']],
            value='Module',
            labelStyle={'display': 'inline-block'}
        ),

        html.P("Figure Height"),
        dcc.Slider(id='height', min=250, max=2000, step=250, value=500),

        dcc.Graph(id="box-plot"),
    ])


    @app.callback(
        Output("box-plot", "figure"),
        [Input("x-axis", "value"),
         Input("y-axis", "value"),
         Input('height', 'value')])
    def generate_chart(x, y, height):
        fig = px.box(results, x=x, y=y, color='Module', height=height)
        fig.update_traces(boxmean=True)
        # fig.update_traces(boxmean='sd')
        return fig

    # Run
    app.run_server(debug=True)
