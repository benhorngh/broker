import abc

from old.services import strategy
from old.services.datasets import Stock
from old.services.strategy import Strategy


class Predictor(abc.ABC):
    def __init__(self, stock: Stock):
        self._stock = stock

    def predict(self, length: int) -> list[float]:
        raise NotImplementedError()

    def plan(self, length: int) -> Strategy:
        prediction = self.predict(length)
        if not prediction:
            raise ValueError("Can't predict the future")
        return strategy.naive_strategy(self._stock, prediction)

    @classmethod
    def name(cls):
        raise NotImplementedError()
