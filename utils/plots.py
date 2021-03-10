from utils.models import select_model
from utils.functions import set_price_range, create_cost, profit
import plotly.graph_objects as go
import numpy as np

layout = dict(
    autosize=True,
    #automargin=True,
    #margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#e9ecef",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h",x=0.5,y=-0.2 ),
)

def plot_demand(sales, item_id, selected_model):
    #demand_layout = copy.deepcopy(layout)
    sales_agg = sales[sales['item_id'] == item_id]
    sales_agg = sales_agg.groupby('date_year_month').agg(
        {'item_cnt_day': ['sum'], 'item_price': ['mean']})
    sales_agg.columns = ["_".join(x) for x in sales_agg.columns]

    estimate_demand_obj = select_model(
        sales_agg, x='item_price_mean', y='item_cnt_day_sum', model= selected_model)
    fig = go.Figure([
        go.Scatter(x=sales_agg['item_price_mean'],
                   y=sales_agg['item_cnt_day_sum'], mode='markers', name='Dados observados'),
        go.Scatter(x=estimate_demand_obj['x_range'],
                   y=estimate_demand_obj['y_range'], name='Demanda estimada'),
    ])

    fig.update_layout(layout)
    fig.update_layout(
        title="Preço X Demanda",
        xaxis_title="Preço",
        yaxis_title="Demanda",
    )

    return fig

def plot_profit_curve(sales, item_id, selected_model):
    sales_agg = sales[sales['item_id'] == item_id]
    sales_agg = sales_agg.groupby('date_year_month').agg(
        {'item_cnt_day': ['sum'], 'item_price': ['mean']})
    sales_agg.columns = ["_".join(x) for x in sales_agg.columns]

    estimate_demand_obj = select_model(
        sales_agg, x='item_price_mean', y='item_cnt_day_sum', model= selected_model)
    mean_price = sales_agg['item_price_mean'].mean()
    Price_range = set_price_range(sales_agg['item_price_mean'])
    cost = create_cost(mean_price, cost_rate=0.6)

    Profit = []
    for price_i in Price_range:
        demand = estimate_demand_obj['model'].predict(
            np.array(price_i).reshape(1, -1))
        Profit.append(profit(demand, price_i, cost))

    idx_profit_max = np.array(Profit).argmax()
    max_price = Price_range[idx_profit_max]
    max_profit = Profit[idx_profit_max]

    fig = go.Figure([
        go.Scatter(x=np.array(Price_range), y=Profit, name='Estimação'),
        go.Scatter(x=np.array(max_price), y=np.array(max_profit),
                   mode='markers', name='Maior lucro estimado')
    ])
    fig.update_layout(layout)
    fig.update_layout(
        title="Otimização preço X Lucro estimado",
        xaxis_title="Preço",
        yaxis_title="Lucro estimado",
    )
    return fig, str(max_price), str(np.max(max_profit))