from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
import numpy as np
from utils.functions import unlist

def ols_model():
    "basic estimate demand function using OLS"
    return LinearRegression()

def decision_model():
    "basic estimate demand function using Decision Tree Regressor"
    return DecisionTreeRegressor()

def knn_model():
    "basic estimate demand function using KNN Regressor"
    return KNeighborsRegressor()

def select_model(df, x, y, model):
    "Select estimate model"
    def select(model):
        if model == 'ols':
            return ols_model()
        if model == 'knn':
            return knn_model()
        if model == 'decision':
            return decision_model()
    model = select(model).fit(df[x].values.reshape(-1, 1), df[y].values.reshape(-1, 1))
    x_range = np.linspace(df[x].min(), df[x].max(), 100)
    y_range = unlist(model.predict(x_range.reshape(-1, 1)))
    return {'model': model, 'x_range': x_range, 'y_range': y_range}


