import random

from predictors.predictor import Predictor
from services import utils
from services.datasets import Stock


class RandomPredictor(Predictor):
    def __init__(self, stock: Stock):
        super(RandomPredictor, self).__init__(stock)

    @classmethod
    def name(cls):
        return "Random"

    def predict(self, length: int) -> list[float]:
        dataset = self._stock.prices
        min_price, max_price = min(dataset), max(dataset)
        random_numbers = [random.uniform(min_price, max_price) for _ in range(length)]
        return utils.round_list(random_numbers)
