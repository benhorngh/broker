from datetime import date

import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor

from old.predictors.predictor import Predictor
from old.services import utils
from old.services.datasets import Stock
from old.services.utils import get_next_trading_dates


class GradientBoostingPredictor(Predictor):
    @classmethod
    def name(cls):
        return "Gradient Boosting"

    features = ["day", "month", "year", "day_of_week"]
    target = "price"

    def __init__(self, stock: Stock):
        super(GradientBoostingPredictor, self).__init__(stock)
        date_and_prices = [(d.day, d.price) for d in stock.train]
        df = self.feature_engineering(date_and_prices)
        x_train = df[self.features]
        y_train = df[self.target]

        model = GradientBoostingRegressor(
            n_estimators=100, random_state=42, min_samples_split=5
        )

        model.fit(x_train, y_train)

        self._model = model

    @staticmethod
    def feature_engineering(dataset: list[tuple[date, float]]) -> pd.DataFrame:
        df = pd.DataFrame(dataset, columns=["date", "price"])
        df["day_of_week"] = df["date"].apply(lambda x: x.weekday())
        df["pd_date"] = pd.to_datetime(df["date"])
        df["day"] = df["pd_date"].dt.day
        df["month"] = df["pd_date"].dt.month
        df["year"] = df["pd_date"].dt.year
        return df

    def predict(self, length) -> list[float]:
        df = self.feature_engineering(
            [(x, 0) for x in get_next_trading_dates(self._stock.last_day, length)]
        )
        x_test = df[self.features]
        forecast = self._model.predict(x_test)
        return utils.round_list(forecast)
