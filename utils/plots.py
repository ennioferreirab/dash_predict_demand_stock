import pandas as pd
from utils.models import select_model
from utils.functions import set_price_range, create_cost, profit
import plotly.graph_objects as go
import plotly.express as px
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

def plot_demand(json_sales_df, selected_model):
    sales_df = pd.read_json(json_sales_df, orient='split')

    estimate_demand_obj = select_model(
        sales_df, x='item_price_mean', y='item_cnt_day_sum', model= selected_model)
    fig = go.Figure([
        go.Scatter(x=sales_df['item_price_mean'],
                   y=sales_df['item_cnt_day_sum'], mode='markers', name='Dados observados'),
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

def plot_profit_curve(json_sales_df, selected_model):
    sales_df = pd.read_json(json_sales_df, orient='split')

    estimate_demand_obj = select_model(
        sales_df, x='item_price_mean', y='item_cnt_day_sum', model= selected_model)
    mean_price = sales_df['item_price_mean'].mean()
    Price_range = set_price_range(sales_df['item_price_mean'])
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

def plot_time_sell(json_sales_df):
    sales_df = pd.read_json(json_sales_df, orient='split')
    sales_df['sold_month'] = sales_df.index
    min_plot_date = sales_df.sold_month.min()
    max_plot_date = sales_df.sold_month.max()
    sales_df['sold_month'] = sales_df['sold_month'].dt.strftime('%Y-%m')
    full_period = pd.period_range(start=min_plot_date, end=max_plot_date, freq='M').to_series().astype(str)
    full_period = pd.DataFrame(full_period, columns=['full_period'])
    df_plot = full_period.merge(sales_df, left_on='full_period', right_on='sold_month',how='left')
    
    fig = px.area(df_plot, x="full_period", y="item_cnt_day_sum")
    fig.update_layout(layout)
    fig.update_layout(
            title="Vendas durante o período analisado, agregado pelo mês",
            xaxis_title="Data",
            yaxis_title="Quantidade de vendas",
        )
    return fig