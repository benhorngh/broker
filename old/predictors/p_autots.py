import pandas as pd
from autots import AutoTS

from old.predictors.predictor import Predictor
from old.services.datasets import Stock
from settings import settings


class AutoTSPredictor(Predictor):
    @classmethod
    def name(cls):
        return "Auth TS"

    def __init__(self, stock: Stock):
        super(AutoTSPredictor, self).__init__(stock)
        model = AutoTS(
            forecast_length=settings.consts.forecast_length,
            frequency="infer",
            prediction_interval=0.9,
            ensemble="auto",
            model_list="superfast",  # "superfast", "default", "fast_parallel"
            transformer_list="superfast",  # "superfast",
            drop_most_recent=0,
            max_generations=4,
            num_validations=2,
            validation_method="backwards",
        )

        date_and_prices = [(d.day, d.price) for d in stock.train]
        df = pd.DataFrame(date_and_prices, columns=["date", "price"])

        model = model.fit(
            df,
            date_col="date",
            value_col="price",
            id_col=None,
        )

        self._model = model

    def predict(self, length) -> list[float]:
        prediction = self._model.predict()
        return list(prediction.forecast["price"])
