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

    # Parameters
    title = 'Sensors Level 0 Feature Selection - Box Plots'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title, style={'textAlign': 'center'}),

        html.H2('Figure 1'),
        html.P('Case:'),
        dcc.RadioItems(
            id='case1',
            options=[{'value': x, 'label': x}
                     for x in ['case1']],
            value='case1',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen1',
            options=[{'value': x, 'label': x}
                     for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Data:'),
        dcc.RadioItems(
            id='data1',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Feature:'),
        dcc.RadioItems(
            id='feature1',
            options=[{'value': x, 'label': x}
                     for x in ['x', 'y', 'z', 'magnitude', 'combine_angle']],
            value='magnitude',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Y Axis:'),
        dcc.RadioItems(
            id='y1',
            options=[{'value': x, 'label': x}
                     for x in ['None', 'user']],
            value='user',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='box-plot1'),

        html.H2('Figure 2'),
        html.P('Case:'),
        dcc.RadioItems(
            id='case2',
            options=[{'value': x, 'label': x}
                     for x in ['case1']],
            value='case1',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Screen:'),
        dcc.RadioItems(
            id='screen2',
            options=[{'value': x, 'label': x}
                     for x in ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']],
            value='Mathisis',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Data:'),
        dcc.RadioItems(
            id='data2',
            options=[{'value': x, 'label': x}
                     for x in ['acc', 'gyr']],
            value='acc',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Feature:'),
        dcc.RadioItems(
            id='feature2',
            options=[{'value': x, 'label': x}
                     for x in ['x', 'y', 'z', 'magnitude', 'combine_angle']],
            value='magnitude',
            labelStyle={'display': 'inline-block'}
        ),
        html.P('Y Axis:'),
        dcc.RadioItems(
            id='y2',
            options=[{'value': x, 'label': x}
                     for x in ['None', 'user']],
            value='user',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(id='box-plot2')
    ])

    @app.callback(
        [Output('box-plot1', 'figure'),
         Output('box-plot2', 'figure')],
        [Input('case1', 'value'),
         Input('case2', 'value'),
         Input('screen1', 'value'),
         Input('screen2', 'value'),
         Input('data1', 'value'),
         Input('data2', 'value'),
         Input('feature1', 'value'),
         Input('feature2', 'value'),
         Input('y1', 'value'),
         Input('y2', 'value')])
    def generate_chart(c1, c2, s1, s2, d1, d2, f1, f2, y1, y2):

        data_path1 = os.path.join('cases', c1, s1, 'df_' + d1 + '.csv')
        df_data1 = pd.read_csv(data_path1)
        if y1 == 'None':
            y1 = None
        fig1 = px.box(df_data1, x=f1, y=y1, color=y1)
        fig1.update_traces(boxmean='sd', boxpoints=False)

        data_path2 = os.path.join('cases', c2, s2, 'df_' + d2 + '.csv')
        df_data2 = pd.read_csv(data_path2)
        if y2 == 'None':
            y2 = None
        fig2 = px.box(df_data2, x=f2, y=y2, color=y2)
        fig2.update_traces(boxmean='sd', boxpoints=False)

        return fig1, fig2

    # Run
    app.run_server(debug=True)
