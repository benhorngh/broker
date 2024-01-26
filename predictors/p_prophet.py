import pandas as pd
from prophet import Prophet

from predictors.predictor import Predictor
from services import utils
from services.datasets import Stock
from services.utils import get_next_trading_dates


class ProphetPredictor(Predictor):
    def __init__(self, stock: Stock):
        super(ProphetPredictor, self).__init__(stock)
        df = pd.DataFrame(
            [(day.day, day.price) for day in stock.train], columns=["ds", "y"]
        )
        self._dataset = df
        model = Prophet()
        model.fit(self._dataset)
        self._model = model

    @classmethod
    def name(cls):
        return "Prophet"

    def predict(self, length: int) -> list[float]:
        dates = [d.day for d in self._stock.train] + get_next_trading_dates(
            self._stock.last_day, length
        )
        future = pd.DataFrame(dates, columns=["ds"])

        forecast = self._model.predict(future)
        forecast = forecast.tail(length)
        results = forecast["yhat"]

        return utils.round_list(results)
