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

    cases = ['case08', 'case09']

    # Parameters
    title = 'SVMs Nu & Gamma Selection - HeatMaps'

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
            options=[{'value': x, 'label': x} for x in ['acc', 'gyr', 'swp', 'tap']],
            value='acc',
            labelStyle={'display': 'inline-block'}),
        html.P('Set ColorBar Range:'),
        dcc.RadioItems(
            id='clr_bar',
            options=[{'value': x, 'label': x} for x in ['Yes', 'No']],
            value='Yes',
            labelStyle={'display': 'inline-block'}),

        html.H2('Figure 1'),
        html.P('Metric:'),
        dcc.RadioItems(
            id='metric1',
            options=[{'value': x, 'label': x} for x in ['FRR_trn', 'FRR_tst', 'FAR']],
            value='FRR_tst',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='graph1'),

        html.H2('Figure 2'),
        html.P('Metric:'),
        dcc.RadioItems(
            id='metric2',
            options=[{'value': x, 'label': x} for x in ['FRR_trn', 'FRR_tst', 'FAR']],
            value='FAR',
            labelStyle={'display': 'inline-block'}),
        dcc.Graph(id='graph2'),

        html.H2('Absolute Difference Between Figure1 & Figure2'),
        dcc.Graph(id='graph3')
    ])

    @app.callback(
        [Output('graph1', 'figure'),
         Output('graph2', 'figure'),
         Output('graph3', 'figure')],
        [Input('clr_bar', 'value'),
         Input('case', 'value'),
         Input('screen', 'value'),
         Input('module', 'value'),
         Input('metric1', 'value'),
         Input('metric2', 'value')]
    )
    def generate_chart(b, c, s, m, met1, met2):

        zmin, zmid, zmax = None, None, None
        if b == 'Yes':
            zmin, zmid, zmax = 0, 0.5, 1

        results_path = os.path.join('cases', c, s, 'results.csv')
        results = pd.read_csv(results_path)
        nus = results.loc[results['Module'] == m]['Nu'].unique()
        gammas = results.loc[results['Module'] == m]['Gamma'].unique()
        met_means1 = pd.DataFrame(index=nus, columns=gammas)
        met_means2 = pd.DataFrame(index=nus, columns=gammas)
        for nu in nus:
            for gamma in gammas:
                sr = results.loc[(results['Module'] == m) & (results['Nu'] == nu) & (results['Gamma'] == gamma)]
                met_means1.at[nu, gamma] = sr[met1].mean()
                met_means2.at[nu, gamma] = sr[met2].mean()

        fig1 = go.Figure(data=go.Heatmap(z=met_means1, zmin=zmin, zmid=zmid, zmax=zmax,
                                         x=gammas, y=nus, colorscale='Viridis'))
        fig1.update_layout(title_text='Corrplot', width=len(gammas) * 30, height=len(nus) * 30)
        fig1.update_xaxes(title='Gamma')
        fig1.update_yaxes(title='Nu')

        fig2 = go.Figure(data=go.Heatmap(z=met_means2, zmin=zmin, zmid=zmid, zmax=zmax,
                                         x=gammas, y=nus, colorscale='Viridis'))
        fig2.update_layout(title_text='Corrplot', width=len(gammas) * 30, height=len(nus) * 30)
        fig2.update_xaxes(title='Gamma')
        fig2.update_yaxes(title='Nu')

        dif_df = (met_means2 - met_means1).abs()
        fig3 = go.Figure(data=go.Heatmap(z=dif_df, zmin=zmin, zmid=zmid, zmax=zmax,
                                         x=gammas, y=nus, colorscale='Viridis'))
        fig3.update_layout(title_text='Corrplot', width=len(gammas) * 30, height=len(nus) * 30)
        fig3.update_xaxes(title='Gamma')
        fig3.update_yaxes(title='Nu')

        return fig1, fig2, fig3

    # Run
    app.run_server(debug=True)
