from dash import Dash, dash_table, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly_express as px
from dash_bootstrap_templates import load_figure_template
import pandas as pd
load_figure_template("flatly")

stocks = pd.read_csv("../data/stocks.csv", parse_dates=["Date"], index_col="Date")#.query("Symbols=='MSFT'")

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY, dbc.icons.FONT_AWESOME],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device_width, intial-scale=1.0'}]
           )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Stock Market Dashboard",
                    className='text-center text-primary mb-4 mt-3'),
            dcc.DatePickerRange(id='date_picker', className='mx-auto mb-4')
        ], width=12, style={'text-align': 'center'})
    ], justify="center"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='single_dropdown', multi=False, value="MSFT", searchable=False,
                options=[{'label': x, 'value': x} for x in stocks["Symbols"].unique()],
                style={'color': '#333'}
            ), 

            dcc.Graph(id='volume_graph', config={"staticPlot": True}, 
                      figure={}, className='mt-2')
        ], xs=12, sm=11, md=10, lg=5),

        dbc.Col([
            dcc.Dropdown(
                id='multi_dropdown', multi=True, value=["MSFT", "AAPL"], searchable=False,
                options=[{'label': x, 'value': x} for x in stocks["Symbols"].unique()],
                style={'color': '#333'}),
            dcc.Graph(id='closing_graph', config={"staticPlot": True}, 
                      figure={}, className='mt-2')
        ], xs=12, sm=11, md=10, lg=5)
    ], justify='evenly'),

    dbc.Row([
        dbc.Col([
            html.Br(),
            html.H2("MSFT", id="data_label",
                    className='text-start text-primary mb-4 mt-3'),
            dash_table.DataTable(id="data_table", page_size=15),
            dbc.Button([
                    html.I(className='fa fa-download fa-bounce me-2'),
                    "Download data"
                ], color="primary", className='my-4')
        ], width=10)
    ], justify='evenly')

], fluid=True)

@callback(
    Output("data_table", "data"),
    Output("volume_graph", "figure"),
    Output("data_label", "children"),
    Input("date_picker", "start_date"),
    Input("date_picker", "end_date"),
    Input("single_dropdown", "value")
)
def update_volume_graph(start, end, symbol):
    df = stocks.query("Symbols==@symbol").loc[start:end]
    data = df.reset_index().drop(columns=["Symbols"]).to_dict('records')
    fig = px.line(df, x=df.index, y="Volume")
    return data, fig, symbol

@callback(
    Output("closing_graph", "figure"),
    Input("date_picker", "start_date"),
    Input("date_picker", "end_date"),
    Input("multi_dropdown", "value")
)
def update_closing_graph(start,end, symbols):
    df = stocks[stocks["Symbols"].isin(symbols)].loc[start:end]
    return px.line(df, x=df.index, y="Close", color="Symbols")

if __name__ == '__main__':
    app.run(debug=True)