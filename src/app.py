import seaborn as sns
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly_express as px

tips = sns.load_dataset("tips")

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div(children='Hello World! What\'s up?'),
    html.Hr(),
    dcc.RadioItems(options=["sex", "smoker", "time", "day", "size"], value="time", id="my-radio-buttons"),
    dash_table.DataTable(data=tips.head().to_dict('records')),
    dcc.Graph(figure={}, id="my-graph")
])

@callback(
    Output(component_id="my-graph", component_property="figure"),
    Input(component_id="my-radio-buttons", component_property="value")
)
def update_graph(color_attribute):
    return px.scatter(tips, x="total_bill", y="tip", color=color_attribute, width=500, template="simple_white")

if __name__ == '__main__':
    app.run(debug=True)