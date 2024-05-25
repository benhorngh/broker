from typing import Type

from old.managers.manager import Manager
from old.predictors.predictor import Predictor
from old.services.datasets import Stock
from old.services.strategy import Strategy


class PredictorManager(Manager):
    """
    Use one predictor to invest on all profitable stocks
    """

    def __init__(self, predictor_cls: Type[Predictor]):
        self._predictor_cls = predictor_cls
        super(PredictorManager, self).__init__()

    def name(self):
        return f"Predictor {self._predictor_cls.name()} Manager"

    def handle(self, stocks: list[Stock], length: int) -> dict[str, Strategy]:
        strategies = {}

        for stock in stocks:
            predictor = self._predictor_cls(stock)
            strategy = predictor.plan(length)
            strategies[stock.symbol] = strategy

        return strategies
