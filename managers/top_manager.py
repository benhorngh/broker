from typing import Type

from common.models import PredictionRequest, ManageResponse, ManageRequest
from evaluate import evaluate_prediction
from predictors.base_predictor import BasePredictor


class TopManager:
    MAX_STOCKS = 5

    @staticmethod
    def manage(manage_request: ManageRequest, predictor: Type[BasePredictor]):
        predictions = []
        for stock in manage_request.stocks:
            predictions.append(
                predictor.predict(
                    PredictionRequest(
                        stock=stock, predict_until=manage_request.predict_until
                    )
                )
            )
        transactions = [evaluate_prediction(p) for p in predictions]
        transactions.sort(key=lambda t: t.expected_profit_percent, reverse=True)
        for t in transactions[TopManager.MAX_STOCKS :]:
            t.skip()
        return ManageResponse(name=predictor.name(), transactions=transactions)
