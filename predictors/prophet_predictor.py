import pandas as pd

from common import utils
from common.models import PredictionRequest, PredictionResponse, Value
from predictors.base_predictor import BasePredictor
from prophet import Prophet


class ProphetPredictor(BasePredictor):
    @classmethod
    def name(cls):
        return "Prophet"

    @staticmethod
    def predict(request: PredictionRequest) -> PredictionResponse:
        dataset = pd.DataFrame(
            [(value.day, value.price) for value in request.stock.values], columns=["ds", "y"]
        )
        model = Prophet(daily_seasonality=True)
        model.fit(dataset)

        trading_days = utils.get_trading_dates(request.stock.get_last_value().day, request.predict_until)
        future = pd.DataFrame(trading_days, columns=["ds"])
        forecast = model.predict(future)

        forecast = forecast.tail(len(trading_days))
        values = [Value(day=dt, price=y) for dt, y in forecast[["ds", "yhat"]].values]
        return PredictionResponse(values=values, request=request)
