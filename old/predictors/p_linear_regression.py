import numpy as np
from sklearn.linear_model import LinearRegression

from old.predictors.predictor import Predictor
from old.services import utils
from old.services.datasets import Stock


class LinearRegressionPredictor(Predictor):
    def __init__(self, stock: Stock):
        super(LinearRegressionPredictor, self).__init__(stock)
        self._dataset = stock.prices
        X = np.arange(len(self._dataset)).reshape(-1, 1)
        y = self._dataset
        self._model = LinearRegression()
        self._model.fit(X, y)

    @classmethod
    def name(cls):
        return "Linear Regression"

    def predict(self, length: int) -> list[float]:
        dataset_len = len(self._dataset)
        future_x = np.arange(dataset_len, dataset_len + length).reshape(-1, 1)
        forecast = self._model.predict(future_x)
        return utils.round_list(forecast)
