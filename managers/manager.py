import abc

from services.datasets import Stock
from services.firestore_db import Action


class Manager(abc.ABC):
    def __init__(self, *args, **kwargs):
        pass

    def handle(self, stocks: list[Stock], length: int) -> list[Action]:
        raise NotImplementedError()

    def name(self):
        raise NotImplementedError()
