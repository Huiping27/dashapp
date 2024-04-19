import plotly.graph_objects as go
import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import html, dcc, callback
from dash import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

# Define the light purple color
light_purple = '#B19CD9'

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define PostgreSQL connection parameters
POSTGRES_HOST = '35.198.95.196'
POSTGRES_PORT = '5432'
POSTGRES_USER = 'postgres'
POSTGRES_PW = 'spicedli'
DB_CLIMATE = 'climate'

# Create URL for database connection
url = f'postgresql://{POSTGRES_USER}:{POSTGRES_PW}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_CLIMATE}'

# Create SQLAlchemy engine
engine = create_engine(url)

# Write SQL query to retrieve data from the database
query = """
    SELECT date, city, moonrise_n
    FROM dbt_hli.moonrise_city
"""
# Execute the query and load data into a DataFrame
df = pd.read_sql(query, engine)

# Create table with light purple header
table = dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{"name": i, "id": i} for i in df.columns],
    style_table={'overflowY': 'scroll', 'height': '200px'},  # Smaller table
    style_header={'backgroundColor': light_purple, 'fontWeight': 'bold', 'fontFamily': 'monaco'},  # Light purple header
    style_cell={'textAlign': 'left', 'fontFamily': 'monaco'}  # Text alignment
)


# initializing the app
app =dash.Dash()

server=app.server

# Create dropdown button
dropdown_button = dcc.Dropdown(
    id='city-dropdown',
    options=[{'label': city, 'value': city} for city in df['city'].unique()],
    value=df['city'].unique()[0],  # Default value
    clearable=False  # Prevent the user from clearing the selection
)

# Create download button
download_button = html.Button("Download Data 🌙", id="btn-download-txt", className="mr-1", style={'fontFamily': 'monaco'})

# Create graphs based on selected city
@app.callback(
    Output('city-graph', 'children'),
    [Input('city-dropdown', 'value')]
)
def update_graph(selected_city):
    city_df = df[df['city'] == selected_city]
    graph = dcc.Graph(
        figure=go.Figure(data=go.Bar(x=city_df['date'], y=city_df['moonrise_n'], marker_color=light_purple),
                         layout={'title': f'Moonrise in {selected_city} by Date 🌙', 'font': {'family': 'monaco'}}),
        style={'height': '80vh'}  # Bigger graph
    )
    return graph

# Callback to handle download button clicks
@app.callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True
)
def download_table(n_clicks):
    return dcc.send_data_frame(df.to_csv, filename="moonrise_data.csv")

# Information about the author
author_info = html.Div([
    html.Hr(),
    html.P("Dashboard created by Li.", style={'font-style': 'italic', 'font-size': '12px', 'fontFamily': 'monaco'})
])

# Layout
app.layout = html.Div(children=[
    html.H1(children='Moonrise over Hamburg, Shanghai, Bali 🌙', style={'textAlign': 'center', 'color': '#636EFA', 'fontFamily': 'monaco'}),
    html.Div([
        html.Div([table, html.Div([download_button, dcc.Download(id="download-text")])], style={'width': '40%', 'display': 'inline-block'}),
        html.Div([dropdown_button, html.Div(id='city-graph', style={'textAlign': 'center'})], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'})
    ]),
    author_info
])

if __name__ == '__main__':
    app.run_server(port=8051)