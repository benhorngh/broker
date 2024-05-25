from old.predictors.predictor import Predictor
from old.services.datasets import Stock


class IdealPredictor(Predictor):
    def __init__(self, stock: Stock):
        super(IdealPredictor, self).__init__(stock)

    @classmethod
    def name(cls):
        return "Ideal"

    def predict(self, length: int) -> list[float]:
        return self._stock.actual_future_prices[:length]
