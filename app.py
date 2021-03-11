
from dash_html_components.Div import Div
from utils.functions import remove_low_sales
from utils.plots import plot_demand, plot_profit_curve
from utils.cards import make_cards
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3 as sql

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])#,'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])

conn = sql.connect('database/dbsqlite.db')
sales = pd.read_sql('SELECT * FROM sales', conn)
print(sales)
date_options = [{'label': 'Todos', 'value': '*'}]
min_date = sales.date.min()
max_date = sales.date.max()

app.layout = html.Div([html.H1('Teste')])
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
