import random
from collections import Counter

from old.predictors.p_autots import AutoTSPredictor
from old.predictors.p_linear_regression import LinearRegressionPredictor
from old.predictors.p_prophet import ProphetPredictor
from old.predictors.predictor import Predictor
from old.services.datasets import Stock
from old.services.strategy import Strategy, ActionType


class DemocratPredictor(Predictor):
    voters_predictors_cls = [
        ProphetPredictor,
        ProphetPredictor,
        ProphetPredictor,
        LinearRegressionPredictor,
        AutoTSPredictor,
        AutoTSPredictor,
        # RandomPlanPredictor
    ]

    @classmethod
    def name(cls):
        return "Democrat"

    def __init__(self, stock: Stock):
        super(DemocratPredictor, self).__init__(stock)
        self._predictors = []
        for predictor in self.voters_predictors_cls:
            self._predictors.append(predictor(stock))

    def predict(self, length: int) -> list[float]:
        pass

    def plan(self, length: int) -> Strategy:
        plans = [predictor.plan(length) for predictor in self._predictors]
        skips = [plan for plan in plans if plan == Strategy.skip]
        buys = [plan for plan in plans if plan != Strategy.skip]

        if len(skips) >= len(plans) / 2:
            return Strategy(action=ActionType.SKIP)

        sell_days = [buy.sell for buy in buys]
        most_common_value, most_common_occurrences = Counter(sell_days).most_common(1)[
            0
        ]
        if most_common_occurrences == 1:
            return Strategy(action=ActionType.SKIP)
        random_plan_with_most_common = random.choice(
            [plan for plan in plans if plan.sell == most_common_value]
        )
        return random_plan_with_most_common
