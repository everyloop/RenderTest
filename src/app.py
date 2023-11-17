from dash import Dash, dash_table, html, dcc, callback, Output, Input, State, ctx
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

server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Stock Market Dashboard",
                    className='text-center text-primary mb-4 mt-3'),
            dcc.DatePickerRange(id='date_picker', className='mx-auto mb-4'),
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
        ], width={'size': 5, 'offset': 1}),
        dbc.Col([
            html.Br(),
            html.Br(),
            dbc.DropdownMenu([
                dbc.DropdownMenuItem("Download as CSV", id='download_csv'),
                dbc.DropdownMenuItem("Download as JSON", id='download_json'),
                dbc.DropdownMenuItem("Download as XML", id='download_xml'),
            ], label=html.Span([
                html.I(className='fa fa-download fa-bounce me-2'),
                "Download data "
            ]), direction="down"),
            dcc.Download(id='downloader')
        ], width={'size': 5, 'offset': 0}, style={'text-align': 'right'})
    ], justify='start'),

    dbc.Row([
        dbc.Col([
            dash_table.DataTable(id="data_table", page_size=15)
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
    fig = px.line(df, x=df.index, y="Volume")
    data = df.reset_index().drop(columns=["Symbols"]).to_dict('records')
    
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

@callback(
    Output("downloader", "data"),
    Input("download_csv", "n_clicks"),
    Input("download_json", "n_clicks"),
    Input("download_xml", "n_clicks"),
    State("date_picker", "start_date"),
    State("date_picker", "end_date"),
    State("single_dropdown", "value"),
    prevent_initial_call=True
)
def download_button_clicked(n1, n2, n3, start, end, symbol):
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    df = stocks.query("Symbols==@symbol").loc[start:end]
    data = df.reset_index().drop(columns=["Symbols"])
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

    if trigger_id=="download_csv":
        content = data.to_csv(index=False)
        extension = 'csv'
    elif trigger_id=="download_json":
        content = data.to_json(orient='records')
        extension = 'json'
    else:
        content = data.to_xml(index=False)
        extension = 'xml'
    
    if start is None: start = data.iloc[0, 0]
    if end is None: end = data.iloc[-1, 0]

    return {
        'content': content,
        'filename': f'{symbol}_{start}_to_{end}.{extension}'
    }

if __name__ == '__main__':
    app.run(debug=True)