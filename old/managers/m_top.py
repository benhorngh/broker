from typing import Type

from old.managers.manager import Manager
from old.predictors.predictor import Predictor
from old.services.datasets import Stock
from old.services.strategy import Strategy, ActionType


class TopPredictorManager(Manager):
    """
    Use one predictor to invest in the top 5 profitable stocks
    """

    TOP_STOCKS_NUMBER = 5

    def __init__(self, predictor_cls: Type[Predictor]):
        self._predictor_cls = predictor_cls
        super(TopPredictorManager, self).__init__()

    def name(self):
        return f"Top Predictor {self._predictor_cls.name()} Manager"

    def handle(self, stocks: list[Stock], length: int) -> dict[str, Strategy]:
        strategies: dict[str, Strategy] = {}

        for stock in stocks:
            predictor = self._predictor_cls(stock)
            strategy = predictor.plan(length)
            strategies[stock.symbol] = strategy
        most_profitable = sorted(
            strategies.items(), key=lambda x: x[1].expected_profit, reverse=True
        )
        most_profitable_stocks = [
            s[0] for s in most_profitable[: self.TOP_STOCKS_NUMBER]
        ]
        for stock in strategies:
            if stock not in most_profitable_stocks:
                strategies[stock] = Strategy(action=ActionType.SKIP)

        return strategies
