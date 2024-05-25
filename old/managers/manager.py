import abc

from old.services.datasets import Stock
from old.services.strategy import Strategy


class Manager(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    def handle(self, stocks: list[Stock], length: int) -> dict[str, Strategy]:
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()
