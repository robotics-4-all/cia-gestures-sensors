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
    screens = ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']
    modules = ['acc', 'gyr']
    features = ['x', 'y', 'z', 'magnitude', 'combine_angle']

    # Parameters
    title = 'Sensors Level 0 Feature Selection - Box Plots'

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
            html.P('Y Axis:'),
            dcc.RadioItems(
                id='y', options=[{'value': x, 'label': x} for x in ['None', 'user']], value='user',
                labelStyle={'display': 'inline-block'}),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'}),

        html.Br(),

        html.Div([
            html.H2('Figure 1'),
            html.P('Feature:'),
            dcc.Dropdown(
                id='feature1', options=[{'value': x, 'label': x} for x in features], value='magnitude',),
            dcc.Graph(id='plot1'),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '2vw'}),

        html.Div([
            html.H2('Figure 2'),
            html.P('Feature:'),
            dcc.Dropdown(
                id='feature2', options=[{'value': x, 'label': x} for x in features], value='y'),
            dcc.Graph(id='plot2'),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw', 'margin-top': '2vw'})

    ])

    @app.callback(
        [Output('plot1', 'figure'),
         Output('plot2', 'figure')],
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

        fig1 = px.box(df_data, x=y, y=f1, color=y)
        fig1.update_traces(boxmean='sd', boxpoints=False)
        # fig1.update_layout(title_text='BoxPlots - ' + s + ' - ' + m + ' - ' + f1, width=500, height=500)
        # fig1.update_layout(title_text=s + ' - ' + m + ' - ' + f1)
        fig1.update_layout(width=450, height=300)
        # fig1.update_yaxes(visible=False, showticklabels=False)
        fig1.update_traces(showlegend=False)

        fig2 = px.box(df_data, x=f2, y=y, color=y)
        fig2.update_traces(boxmean='sd', boxpoints=False)
        fig2.update_layout(title_text='BoxPlots - ' + s + ' - ' + m + ' - ' + f2, width=500, height=500)

        return fig1, fig2

    # Run
    app.run_server(debug=True)
