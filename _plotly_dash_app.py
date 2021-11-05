"""
This script was created at 05-Nov-21
author: eachrist

"""
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

app.layout = html.Div([
    html.P("x-axis:"),
    dcc.RadioItems(
        id='x-axis',
        options=[{'value': x, 'label': x}
                 for x in ['NumOfOrgUserTstData', 'FRR', 'FAR', 'NumOfUnlocks', 'FRR_Conf', 'NumOfAcceptTL']],
        value='FRR_Conf',
        labelStyle={'display': 'inline-block'}
    ),
    html.P("y-axis:"),
    dcc.RadioItems(
        id='y-axis',
        options=[{'value': x, 'label': x}
                 for x in ['Module', 'OriginalUser', 'Fold']],
        value='Module',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id="box-plot"),
])

results = pd.read_csv('cases/case1/Mathisis/results.csv')


@app.callback(
    Output("box-plot", "figure"),
    [Input("x-axis", "value"),
     Input("y-axis", "value")])
def generate_chart(x, y):
    fig = px.box(results, x=x, y=y)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
