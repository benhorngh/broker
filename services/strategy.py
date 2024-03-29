from datetime import date
from typing import Optional

from pydantic import BaseModel

from services import utils
from services.datasets import Stock
from services.firestore_db import ActionType
from services.utils import rnd


class Strategy(BaseModel):
    buy: Optional[date] = None
    sell: Optional[date] = None
    expected_profit: float = 0
    up_only: bool = False
    action: ActionType

    @property
    def skip(self):
        return self.action == ActionType.SKIP


def naive_strategy(stock: Stock, forecast: list[float]) -> Optional[Strategy]:
    future_dates = utils.get_next_trading_dates(stock.last_day, len(forecast))
    max_index = forecast.index(max(forecast))
    if max_index != 0:
        expected_profit = rnd(max(forecast) - forecast[0])
        up_only = forecast == sorted(forecast)
        return Strategy(
            buy=future_dates[0],
            sell=future_dates[max_index],
            action=ActionType.BUY,
            expected_profit=expected_profit,
            up_only=up_only,
        )
    return Strategy(action=ActionType.SKIP)
