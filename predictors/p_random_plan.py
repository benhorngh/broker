import random

from predictors.predictor import Predictor
from services import utils
from services.datasets import Stock
from services.firestore_db import ActionType
from services.strategy import Strategy


class RandomPlanPredictor(Predictor):
    def __init__(self, stock: Stock):
        super(RandomPlanPredictor, self).__init__(stock)

    @classmethod
    def name(cls):
        return "Random Plan"

    def predict(self, length: int) -> list[float]:
        dataset = self._stock.prices
        min_price, max_price = min(dataset), max(dataset)
        random_numbers = [random.uniform(min_price, max_price) for _ in range(length)]
        return utils.round_list(random_numbers)

    def plan(self, length: int) -> Strategy:
        skip = -1
        next_days = utils.get_next_trading_dates(self._stock.last_day, length)
        next_day, rest_days = next_days[0], next_days[1:]
        random_date = random.choice([skip, *rest_days])
        if random_date == skip:
            return Strategy(action=ActionType.SKIP)
        return Strategy(buy=next_day, sell=random_date, action=ActionType.BUY)
