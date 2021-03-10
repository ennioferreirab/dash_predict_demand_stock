import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
import scipy

def profit(quantity, price, cost):
    return (quantity * price) - cost

def remove_low_sales(df, min_count = 50):
    "remove items with sales less than minimum"
    df_min_count = df[['item_id','date']].groupby('item_id').count()
    return df_min_count[df_min_count['date'] > min_count].index


def create_cost(mean_price,cost_rate = 0.83):
    "create randomized item cost rate"
    #np.random.seed(1)
    #item_list = df['item_id'].unique()
    #random_cost = np.random.normal(mu, sigma, len(item_list))
    #return pd.DataFrame(zip(item_list,random_cost),columns=['item_id','cost'])
    #cost_rate = np.random.randint(60,80,size=1)/100
    return (cost_rate * mean_price)

def set_price_range(x):
    minimum_price = x.min()
    maximum_price = x.max()
    return range(round(minimum_price), round(maximum_price), 10)

def calculate_security_stock(tolerance, mean_lead, std_lead, mean_demand, std_demand, deviation_multiplier=1):
    return scipy.stats.norm.ppf(tolerance) * np.sqrt(((std_lead * deviation_multiplier) * mean_lead) + ( (std_demand * deviation_multiplier) * mean_demand))
