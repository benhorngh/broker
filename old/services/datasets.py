from datetime import date

from pydantic import BaseModel


class Day(BaseModel):
    day: date
    price: float


class Stock(BaseModel):
    symbol: str
    raw_data: list[Day]
    cutoff: int = 0

    @property
    def train(self) -> list[Day]:
        if self.cutoff == 0:
            return self.raw_data
        return self.raw_data[: -self.cutoff]

    @property
    def test(self) -> list[Day]:
        if self.cutoff == 0:
            return []
        return self.raw_data[-self.cutoff :]

    @property
    def last_day(self) -> date:
        return self.train[-1].day

    @property
    def actual_future_prices(self) -> list[float]:
        return [day.price for day in self.test]

    def actual_future_price_at(self, future_day: date) -> float:
        return [day for day in self.test if day.day == future_day][0].price

    @property
    def prices(self) -> list[float]:
        return [day.price for day in self.train]
