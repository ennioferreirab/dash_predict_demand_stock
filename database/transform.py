import sqlite3 as sql
import pandas as pd

sales = pd.read_csv('../raw_data/sales_train.csv')
sales = sales[sales['item_cnt_day'] != -1]
sales['date'] = pd.to_datetime(sales['date'], dayfirst=True)
sales['year'] = sales['date'].dt.year
sales['month'] = sales['date'].dt.month
sales['date_year_month'] = sales['date'].dt.strftime('%Y-%m')

# select shop
select_shop_id = 31  # top observations
sales = sales[sales['shop_id'] == select_shop_id]


if __name__ == '__main__':
    conn = sql.connect('dbsqlite.db')
    sales.to_sql('sales', conn)