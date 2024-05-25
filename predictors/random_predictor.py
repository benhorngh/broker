import random

from common import utils
from common.models import PredictionRequest, PredictionResponse
from predictors.base_predictor import BasePredictor
from predictors.utils import combine_values


class RandomPredictor(BasePredictor):
    @classmethod
    def name(cls):
        return "Random"

    @staticmethod
    def predict(request: PredictionRequest) -> PredictionResponse:
        prices = [value.price for value in request.stock.values]
        dates = utils.get_trading_dates(
            request.stock.get_last_value().day, request.predict_until
        )
        prediction = random.choices(prices, k=len(dates))
        return PredictionResponse(
            values=combine_values(dates, prediction), request=request
        )
