import uuid
from typing import Type

from managers.manager import Manager
from predictors.predictor import Predictor
from services.datasets import Stock
from services.firestore_db import Action, ActionType, ActionStatus


class PredictorManager(Manager):
    def __init__(self, predictor_cls: Type[Predictor]):
        self._predictor_cls = predictor_cls
        super(PredictorManager, self).__init__()

    def name(self):
        return f"Predictor {self._predictor_cls.name()} Manager"

    def handle(self, stocks: list[Stock], length: int) -> list[Action]:
        actions = []

        for stock in stocks:
            predictor = self._predictor_cls(stock)
            strategy = predictor.plan(length)
            if strategy.action == ActionType.BUY:
                buy = Action(
                    action_id=str(uuid.uuid4()),
                    symbol=stock.symbol,
                    action_type=ActionType.BUY,
                    when=strategy.buy,
                    how_many_stocks=1,
                    manager=self.name(),
                    status=ActionStatus.PENDING,
                )
                sell = Action(
                    action_id=str(uuid.uuid4()),
                    symbol=stock.symbol,
                    action_type=ActionType.SELL,
                    when=strategy.sell,
                    manager=self.name(),
                    how_many_stocks=1,
                    status=ActionStatus.PENDING,
                )
                actions += [buy, sell]
        return actions
