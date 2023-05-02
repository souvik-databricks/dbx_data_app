# Databricks notebook source
# MAGIC %pip install dash Jinja2==3.0.3 fastapi uvicorn nest_asyncio databricks-cli

# COMMAND ----------

import dash
from dash.dependencies import Input, Output
from dash import dcc, html

import flask
import pandas as pd
import os

from sdk.mount import DatabricksApp
dbx_app = DatabricksApp(8089)

# COMMAND ----------

server_name = 'my-dash-app'
server = flask.Flask(server_name)
server.secret_key = "somesecretkey"

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/hello-world-stock.csv')


app = dash.Dash(server_name, server=server, requests_pathname_prefix=dbx_app.dash_app_url_base_path)

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1('Stock Tickers'),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'},
            {'label': 'Coke', 'value': 'COKE'}
        ],
        value='TSLA'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dff = df[df['Stock'] == selected_dropdown_value]
    return {
        'data': [{
            'x': dff.Date,
            'y': dff.Close,
            'line': {
                'width': 3,
                'shape': 'spline'
            }
        }],
        'layout': {
            'margin': {
                'l': 30,
                'r': 20,
                'b': 30,
                't': 20
            }
        }
    }


# COMMAND ----------

dbx_app.mount_dash_app(app)

# COMMAND ----------

import nest_asyncio
nest_asyncio.apply()
dbx_app.run()

# COMMAND ----------


