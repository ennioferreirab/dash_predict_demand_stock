
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

sales = pd.read_csv('raw_data/sales_train.csv')
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

NAVBAR = html.Nav(
    dbc.Row([
        dbc.Col([],md=4),
        dbc.Col([html.H4('Otimização de Estoque | Preço | Demanda')],
            md=5, style={'margin-top': '1rem'}),
        dbc.Col([
            html.H6('Apenas demonstração', style={'color': '#80808063', 'text-align': 'right'}),
            html.A(
                html.Img(src='assets/linkedin.png',style={'width':'25px', 'position': 'absolute','right': '15px'}),
                href="https://www.linkedin.com/in/ennio-bastos-41a33264/")
        ],md=3)
    ])
)

LEFT_COLUMN = dbc.Jumbotron(
    [
        html.Div([
            html.P('Selecione uma data'),
            dcc.DatePickerRange(
                id='my-date-picker-range',
                min_date_allowed=min_date,
                max_date_allowed=max_date,
                display_format='DD/MM/YYYY',
                initial_visible_month=min_date,
                start_date=min_date,
                end_date=max_date
            )],style={'margin-bottom': '1rem'}),
        html.Div([html.P('Selecione o modelo de estimação'),
            dcc.Dropdown(
                id='model-dropdown',
                options=[
                    {'label': 'Árvore de decisão', 'value': 'decision'},
                    {'label': 'Regressão linear', 'value': 'ols'},
                    {'label': 'Regressão KNN', 'value': 'knn'},
                    ],
                value='decision')],style={'margin-bottom': '1rem', 'margin-top': '1rem'}),
        html.Div([html.P('Filtrar quantidade minima vendida'),
            dcc.Slider(
                id='available-id',
                min=50,
                max=150,
                step=50,
                value=150,
                marks={str(i): str(i) for i in range(50, 200, 50)})],style={'margin-bottom': '1rem', 'margin-top': '1rem'}),
        html.Div([html.P('Selecione o item ID desejado'),
            dcc.Dropdown(
                id='available-dropdown',
                value=4181)],style={'margin-top': '1rem'}),
    ]
, style={'padding': '1rem 1rem 4rem 1rem','box-shadow': '3px 2px 7px lightgrey'})

RIGHT_COLUMN = [
    dbc.Row([
        dbc.Col(dcc.Graph(id='plot_demand',style={'padding':'0 0 0 0', 'box-shadow': '3px 2px 7px lightgrey'}),md=6),
        dbc.Col(dcc.Graph(id='plot_profit',style={'box-shadow': '3px 2px 7px lightgrey'}),md=6,style={'padding-right': '0'})])
]

app.layout = html.Div([html.H1('Teste')])


if __name__ == '__main__':
    app.run_server(debug=True)
