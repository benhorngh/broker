from common import stocks_data, utils
from common.models import PredictionRequest, PredictionResponse
from predictors.base_predictor import BasePredictor


class IdealPredictor(BasePredictor):
    @classmethod
    def name(cls):
        return "Ideal"

    @staticmethod
    def predict(request: PredictionRequest) -> PredictionResponse:
        stock_real_values = stocks_data.get_stocks(
            [request.stock.symbol], request.predict_until
        )[0]
        if stock_real_values.get_last_value().day < request.predict_until:
            raise ValueError("Ideal predictor cant predict the future")
        trading_dates = utils.get_trading_dates(
            request.stock.get_last_value().day, request.predict_until
        )
        values = []
        for day in trading_dates:
            values.append(stock_real_values.get_by_day(day))

        return PredictionResponse(values=values, request=request)
