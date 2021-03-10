from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import numpy as np

def ols_model(df, x,y):
    "basic estimate demand function using OLS"
    model = LinearRegression().fit(df[x].values.reshape(-1, 1), df[y].values.reshape(-1, 1))
    x_range = np.linspace(df[x].min(), df[x].max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))
    return {'model': model, 'x_range': x_range, 'y_range': y_range}

def decision_model(df, x,y):
    "basic estimate demand function using Decision Tree Regressor"
    model = DecisionTreeRegressor().fit(df[x].values.reshape(-1, 1), df[y].values.reshape(-1, 1))
    x_range = np.linspace(df[x].min(), df[x].max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))
    print('Predict: ',y_range)
    return {'model': model, 'x_range': x_range, 'y_range': y_range}