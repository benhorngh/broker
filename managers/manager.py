import abc

from services.datasets import Stock
from services.strategy import Strategy


class Manager(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    def handle(self, stocks: list[Stock], length: int) -> dict[str, Strategy]:
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()
