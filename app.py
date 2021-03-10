
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

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])

sales_raw = pd.read_csv('raw_data/sales_train.csv')
sales = sales_raw.copy()
sales = sales[sales['item_cnt_day'] != -1]
sales['date'] = pd.to_datetime(sales['date'], dayfirst=True)
sales['year'] = sales['date'].dt.year
sales['month'] = sales['date'].dt.month
sales['date_year_month'] = sales['date'].dt.strftime('%Y-%m')

# select
select_shop_id = 31  # top observations
sales = sales[sales['shop_id'] == select_shop_id]

date_options = [{'label': 'Todos', 'value': '*'}]
min_date = sales.date.min()
max_date = sales.date.max()

app.layout = html.Div([html.H1('Leu')])
        

if __name__ == '__main__':
    app.run_server(debug=True)
