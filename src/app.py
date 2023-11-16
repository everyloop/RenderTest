from dash import Dash, html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import pandas as pd

load_figure_template("cyborg")

df = pd.read_csv("../data/stooq.csv")

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device_width, intial-scale=1.0'}]
           )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Stock Market Dashboard",
                        className='text-center text-primary mb-4 mt-3'),
                width=6)
    ], justify="center"),

    dbc.Row([
        dbc.Col([dcc.Dropdown(id='my_dpdn', multi=False, value="MSFT",
                             options=[{'label': x, 'value': x} for x in df["Symbols"].unique()]),
                dcc.Graph(id='line-fig', figure={}, className='mt-2')
                ], width={'size': 4, 'offset': 0, 'order': 1}),
                
        dbc.Col([dcc.Dropdown(id='my_dpdn2', multi=True, value=["MSFT", "AAPL"],
                             options=[{'label': x, 'value': x} for x in df["Symbols"].unique()]),
                dcc.Graph(id='line-fig2', figure={})
                ], width={'size': 4, 'offset': 0, 'order': 2})
    ], justify='evenly')
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)#, jupyter_mode='external')