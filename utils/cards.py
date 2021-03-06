from utils.models import select_model
from utils.functions import calculate_security_stock, unlist
import numpy as np
import scipy
import dash_bootstrap_components as dbc
import dash_html_components as html


def design_cards_reais(x, txt):
    return dbc.Card([
        html.P(txt, style={'background-color': '#E9ECEF', 'height': '3rem',
                           'margin-bottom': '0px',
                           'display': 'flex',
                           'align-items': 'center',
                           'justify-content': 'center', }),
        dbc.CardBody(
            html.P(f'R$ {x}', className='card-text'))
    ], style={'box-shadow': '3px 2px 7px lightgrey'})

def design_cards_number(x, txt):
    return dbc.Card([
        html.P(txt, style={'background-color': '#E9ECEF', 'height': '3rem',
                           'margin-bottom': '0px',
                           'display': 'flex',
                           'align-items': 'center',
                           'justify-content': 'center', }),
        dbc.CardBody(
            html.P(f'{x}', className='card-text'))
    ], style={'box-shadow': '3px 2px 7px lightgrey'})


def make_cards(sales, item_id, selected_model, max_price, max_profit):
    max_price, max_profit, est_demand, security_stock, minimum_stock, max_stock = \
        calcule_stock_stats(sales, item_id, selected_model,
                            max_price, max_profit)
    max_price_card = design_cards_reais(max_price, "Preço ótimo"),
    max_profit_card = design_cards_reais(
        int(round(np.float32(max_profit))), 'Lucro estimado'),
    est_demand_card = design_cards_number(
        int(unlist(np.round(est_demand))[0]), "Demanda estimada"),
    security_stock_card = design_cards_number(
        int(unlist(np.round(security_stock))[0]), "Estoq. de segurança"),
    minimum_stock_card = design_cards_number(
        int(unlist(np.round(minimum_stock))[0]), "Estoque mínimo"),
    max_stock_card = design_cards_number(
        int(unlist(np.round(max_stock))[0]), "Estoque máximo")

    return dbc.Row(
        [dbc.Col(max_price_card, md=2, style={'padding-left': '0px'}),
         dbc.Col(max_profit_card, md=2),
         dbc.Col(est_demand_card, md=2),
         dbc.Col(security_stock_card, md=2),
         dbc.Col(minimum_stock_card, md=2),
         dbc.Col(max_stock_card, md=2, style={'padding-right': '0px'})], 
            style={'text-align': 'center', 'width': '100%','margin-left': '10px','margin-right': '0px'})


def calcule_stock_stats(sales, item_id, selected_model, max_price, max_profit):
    stock_tolerance = 0.6
    confidence_tolerance = 0.95
    mean_lead_time = 70  # 0.5 * 30 = 15 days
    std_lean_time = 10  # 0.2 * 30 = 6 days
    # product variables
    sales_agg = sales[sales['item_id'] == item_id]
    sales_agg = sales_agg.groupby('date_year_month').agg(
        {'item_cnt_day': ['sum'], 'item_price': ['mean']})
    sales_agg.columns = ["_".join(x) for x in sales_agg.columns]

    estimate_demand_obj = select_model(
        sales_agg, x='item_price_mean', y='item_cnt_day_sum', model=selected_model)
    est_demand = estimate_demand_obj['model'].predict(
        np.array(int(max_price)).reshape(1, -1))
    std_demand = sales_agg['item_cnt_day_sum'].var()

    security_stock = calculate_security_stock(
        stock_tolerance, mean_lead_time, std_lean_time, est_demand, std_demand)

    # scipy.stats.poisson.ppf([1-confidence_tolerance, confidence_tolerance], mean_demand)
    minimum_stock, max_stock = scipy.stats.t.interval(confidence_tolerance, len(
        sales_agg), loc=est_demand, scale=np.sqrt(std_demand)+2)
    if minimum_stock < 1:
        minimum_stock = [1]
    return max_price, max_profit, est_demand, security_stock, minimum_stock, max_stock
