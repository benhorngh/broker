from datetime import date
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from common.utils import round_results


class Value(BaseModel):
    price: float
    day: date


class Stock(BaseModel):
    symbol: str
    values: list[Value]

    def get_last_value(self) -> Value:
        return self.values[-1]

    def get_by_day(self, day: date) -> Value:
        return [value for value in self.values if value.day == day][0]


class PredictionRequest(BaseModel):
    stock: Stock
    predict_until: date


class PredictionResponse(BaseModel):
    values: list[Value]
    request: PredictionRequest


class Action(str, Enum):
    BUY = "BUY"
    SKIP = "SKIP"


class Transaction(BaseModel):
    stock: Stock
    buy: Optional[date] = None
    sell: Optional[date] = None
    expected_sell_price: Optional[float] = None
    actual_sell_price: Optional[float] = None
    action: Action

    def skip(self):
        self.action = Action.SKIP
        self.buy = None
        self.sell = None
        self.expected_sell_price = None
        self.actual_sell_price = None

    @property
    def expected_profit(self):
        return self.expected_sell_price - self.buy_price

    @property
    def actual_profit(self):
        if self.actual_sell_price is None:
            return None
        return self.actual_sell_price - self.buy_price

    @property
    def buy_price(self):
        return self.stock.get_by_day(self.buy).price

    @property
    @round_results
    def expected_profit_percent(self) -> float:
        if self.action == Action.SKIP:
            return 0
        return self.expected_profit / self.buy_price * 100


class ManageRequest(BaseModel):
    stocks: list[Stock]
    predict_until: date


class ManageResponse(BaseModel):
    name: str
    transactions: list[Transaction]

    @property
    def buy_transactions(self) -> list[Transaction]:
        return [t for t in self.transactions if t.action == Action.BUY]

    @property
    @round_results
    def spent(self) -> float:
        return sum([t.buy_price for t in self.buy_transactions])

    @property
    @round_results
    def expected_profit(self) -> float:
        return sum([t.expected_profit for t in self.buy_transactions])

    @property
    @round_results
    def actual_profit(self) -> Optional[float]:
        if self.buy_transactions[0].actual_profit is not None:
            return sum([t.actual_profit for t in self.buy_transactions])

    @property
    @round_results
    def profit_percent(self) -> float:
        if self.actual_profit is not None:
            return self.actual_profit / self.spent * 100

    @property
    def number_of_stocks(self) -> float:
        return len(self.buy_transactions)

    @property
    def ibkr_fee(self) -> float:
        return len(self.buy_transactions) * 2
