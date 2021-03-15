
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

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,'https://use.fontawesome.com/releases/v5.8.1/css/all.css'])

conn = sql.connect('database/dbsqlite.db')
sales = pd.read_sql('SELECT * FROM sales', conn)

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
        dbc.Col(dcc.Graph(id='plot_profit',style={'box-shadow': '3px 2px 7px lightgrey'}),md=6)])
]

app.layout = html.Div([
        dbc.Container(
            [
                NAVBAR,
                dbc.Row(id='stock-stats', style={
                    'margin-left': '0px', 'margin-top': '2rem', 'margin-bottom': '2rem','font-size': '1.3rem'}),
                dbc.Row([
                    dbc.Col(LEFT_COLUMN, align="center", md=3, style={"height":"100%"}),
                    dbc.Col(RIGHT_COLUMN, md=9)
                ])
            ], style={'max-width': '95%'}),
    html.Div(id='intermediate_df_plot', style={'display': 'none'}), #store value        
    html.Div(id='max_price', style={'display': 'none'}), #store value
    html.Div(id='max_profit', style={'display': 'none'}), #store value
])


@app.callback(
    Output('available-dropdown', 'options'),
    [Input('available-id', 'value'),
     Input('my-date-picker-range', 'start_date'),
     Input('my-date-picker-range', 'end_date')])
def update_output(available_id, start_date, end_date):
    sales_filter_date = sales[((sales['date'] > start_date) &  (sales['date'] < end_date))]
    available_list = remove_low_sales(
        sales_filter_date, min_count=available_id)
    return [{'label': i, 'value': i} for i in available_list]

@app.callback(
    Output('intermediate_df_plot', 'children'),
    Input('available-dropdown', 'value'))
def make_intermediate_df(item_id):
    sales_agg = sales[sales['item_id'] == item_id]
    sales_agg = sales_agg.groupby('date_year_month').agg(
        {'item_cnt_day': ['sum'], 'item_price': ['mean']})
    sales_agg.columns = ["_".join(x) for x in sales_agg.columns]
    return sales_agg.to_json(date_format='iso', orient='split')


@ app.callback(
    Output('plot_demand', 'figure'),
    Input('intermediate_df_plot', 'children'),
    Input('model-dropdown', 'value'))
def make_plot_demand(json_sales_df, selected_model):
    return plot_demand(json_sales_df, selected_model)


@ app.callback(
    Output('plot_profit', 'figure'), Output('max_price', 'children'), Output('max_profit', 'children'),
    Input('intermediate_df_plot', 'children'),
    Input('model-dropdown', 'value'))
def make_plot_profit_curve(json_sales_df, selected_model):
    return plot_profit_curve(json_sales_df,  selected_model)


@ app.callback(
    Output('stock-stats', 'children'),
    Input('available-dropdown', 'value'),
    Input('model-dropdown', 'value'),
    Input('max_price', 'children'),
    Input('max_profit', 'children')
)
def make_cards_(item_id, selected_model, max_price, max_profit):
    return make_cards(sales, item_id, selected_model, max_price, max_profit)

server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)
