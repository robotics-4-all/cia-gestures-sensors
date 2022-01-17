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
import plotly.express as px

#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    cases = ['case01']

    # Parameters
    title = 'Sensors Level 0 Feature Selection - Box Plots'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.P('Case:'),
        dcc.RadioItems(
            id='case',
            options=[{'value': x, 'label': x} for x in cases],
            value=cases[0],
            labelStyle={'display': 'inline-block'}),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen',
            options=[{'value': x, 'label': x} for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}),
        html.P('Module:'),
        dcc.RadioItems(
            id='module',
            options=[{'value': x, 'label': x} for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}),
        html.P('Y Axis:'),
        dcc.RadioItems(
            id='y',
            options=[{'value': x, 'label': x} for x in ['None', 'user']],
            value='user',
            labelStyle={'display': 'inline-block'}),

        html.H2('Figure 1'),
        html.P('Feature:'),
        dcc.RadioItems(
            id='feature1',
            options=[{'value': x, 'label': x} for x in ['x', 'y', 'z', 'magnitude', 'combine_angle']],
            value='magnitude',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='box-plot1'),

        html.H2('Figure 2'),
        html.P('Feature:'),
        dcc.RadioItems(
            id='feature2',
            options=[{'value': x, 'label': x} for x in ['x', 'y', 'z', 'magnitude', 'combine_angle']],
            value='y',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='box-plot2')
    ])

    @app.callback(
        [Output('box-plot1', 'figure'),
         Output('box-plot2', 'figure')],
        [Input('case', 'value'),
         Input('screen', 'value'),
         Input('module', 'value'),
         Input('y', 'value'),
         Input('feature1', 'value'),
         Input('feature2', 'value')])
    def generate_chart(c, s, m, y, f1, f2):

        data_path = os.path.join('cases', c, s, 'df_' + m + '.csv')
        df_data = pd.read_csv(data_path)
        if y == 'None':
            y = None

        fig1 = px.box(df_data, x=f1, y=y, color=y)
        fig1.update_traces(boxmean='sd', boxpoints=False)

        fig2 = px.box(df_data, x=f2, y=y, color=y)
        fig2.update_traces(boxmean='sd', boxpoints=False)

        return fig1, fig2

    # Run
    app.run_server(debug=True)
