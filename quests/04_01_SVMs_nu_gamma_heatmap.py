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
import plotly.graph_objects as go

#  ========= #
#    Main    #
# ========== #
if __name__ == '__main__':

    cases = ['case08', 'case09', 'case17', 'case18']
    screens = ['Mathisis', 'Focus', 'Reacton', 'Memoria', 'Speedy']
    modules = ['acc', 'gyr', 'swp', 'tap']
    metrics = ['FRR_tst', 'FRRConf_tst', 'FAR', 'NumOfAcceptTL']

    # Parameters
    title = 'SVMs Nu & Gamma Selection - HeatMaps'

    # Init app
    app = dash.Dash(__name__)
    app.title = title
    app.layout = html.Div([

        html.H1(title),

        html.Div([
            html.H2('Overall Parameters'),
            html.P('Screen:'),
            dcc.RadioItems(
                id='screen', options=[{'value': x, 'label': x} for x in screens], value='Mathisis',
                labelStyle={'display': 'inline-block'}),
            html.P('Module:'),
            dcc.RadioItems(
                id='module', options=[{'value': x, 'label': x} for x in modules], value='acc',
                labelStyle={'display': 'inline-block'}),
            html.P('Size Parameter:'),
            dcc.Slider(
                id='sqr_size', min=100, max=200, step=25, value=125,
                tooltip={"placement": "bottom", "always_visible": True}),
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'}),

        html.Div([
            html.H2('Absolute Difference Between Figure1 & Figure2'),
            html.P('Set ColorBar Range:'),
            dcc.RadioItems(
                id='clr_bar3', options=[{'value': x, 'label': x} for x in ['Yes', 'No']], value='No',
                labelStyle={'display': 'inline-block'}),
            dcc.Graph(id='graph3')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'}),

        html.Br(),

        html.Div([
            html.H2('Figure 1'),
            html.P('Case:'),
            dcc.Dropdown(
                id='case1', options=[{'value': x, 'label': x} for x in cases], value=cases[0]),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric1', options=[{'value': x, 'label': x} for x in metrics], value='FRR_tst'),
            html.P('Set ColorBar Range:'),
            dcc.RadioItems(
                id='clr_bar1', options=[{'value': x, 'label': x} for x in ['Yes', 'No']], value='Yes',
                labelStyle={'display': 'inline-block'}),
            dcc.Graph(id='graph1')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'}),

        html.Div([
            html.H2('Figure 2'),
            html.P('Case:'),
            dcc.Dropdown(
                id='case2', options=[{'value': x, 'label': x} for x in cases], value=cases[0]),
            html.P('Metric:'),
            dcc.Dropdown(
                id='metric2', options=[{'value': x, 'label': x} for x in metrics], value='FAR'),
            html.P('Set ColorBar Range:'),
            dcc.RadioItems(
                id='clr_bar2', options=[{'value': x, 'label': x} for x in ['Yes', 'No']], value='Yes',
                labelStyle={'display': 'inline-block'}),
            dcc.Graph(id='graph2')
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '3vw'})

    ])

    @app.callback(
        [Output('graph1', 'figure'),
         Output('graph2', 'figure'),
         Output('graph3', 'figure')],
        [Input('sqr_size', 'value'),
         Input('screen', 'value'),
         Input('module', 'value'),
         Input('case1', 'value'),
         Input('metric1', 'value'),
         Input('clr_bar1', 'value'),
         Input('case2', 'value'),
         Input('metric2', 'value'),
         Input('clr_bar2', 'value'),
         Input('clr_bar3', 'value')]
    )
    def generate_chart(sz, s, m, c1, t1, b1, c2, t2, b2, b3):

        # 1 Fig
        results_path1 = os.path.join('cases', c1, s, 'results.csv')
        results1 = pd.read_csv(results_path1)
        nus1 = results1.loc[results1['Module'] == m]['Nu'].unique()
        gammas1 = results1.loc[results1['Module'] == m]['Gamma'].unique()
        met_means1 = pd.DataFrame(index=nus1, columns=gammas1)
        for nu in nus1:
            for gamma in gammas1:
                sr = results1.loc[(results1['Module'] == m) & (results1['Nu'] == nu) & (results1['Gamma'] == gamma)]
                met_means1.at[nu, gamma] = sr[t1].mean()
        fig1 = go.Figure(data=go.Heatmap(z=met_means1, x=gammas1, y=nus1, colorscale='Viridis',
                                         zmin=0 if b1 == 'Yes' else None,
                                         zmax=1 if b1 == 'Yes' else None))
        fig1.update_layout(title_text='Heatmap ' + t1, width=4 * sz, height=3 * sz)
        fig1.update_xaxes(title='Gamma')
        fig1.update_yaxes(title='Nu')

        # 2 Fig
        results_path2 = os.path.join('cases', c2, s, 'results.csv')
        results2 = pd.read_csv(results_path2)
        nus2 = results2.loc[results2['Module'] == m]['Nu'].unique()
        gammas2 = results2.loc[results2['Module'] == m]['Gamma'].unique()
        met_means2 = pd.DataFrame(index=nus2, columns=gammas2)
        for nu in nus2:
            for gamma in gammas2:
                sr = results2.loc[(results2['Module'] == m) & (results2['Nu'] == nu) & (results2['Gamma'] == gamma)]
                met_means2.at[nu, gamma] = sr[t2].mean()
        fig2 = go.Figure(data=go.Heatmap(z=met_means2, x=gammas2, y=nus2, colorscale='Viridis',
                                         zmin=0 if b2 == 'Yes' else None,
                                         zmax=1 if b2 == 'Yes' else None))
        fig2.update_layout(title_text='Heatmap ' + t2, width=4 * sz, height=3 * sz)
        fig2.update_xaxes(title='Gamma')
        fig2.update_yaxes(title='Nu')

        # 3 Fig
        dif_df = (met_means2 - met_means1).abs()
        fig3 = go.Figure(data=go.Heatmap(z=dif_df, x=gammas1, y=nus1, colorscale='Viridis',
                                         zmin=0 if b3 == 'Yes' else None,
                                         zmax=1 if b3 == 'Yes' else None))
        fig3.update_layout(title_text='Heatmap abs(' + t1 + ' - ' + t2 + ')',
                           width=4 * sz, height=3 * sz)
        fig3.update_xaxes(title='Gamma')
        fig3.update_yaxes(title='Nu')

        return fig1, fig2, fig3

    # Run
    app.run_server(debug=True)
