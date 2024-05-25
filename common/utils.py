import datetime
from datetime import date

import pandas_market_calendars as mcal

US_STOCK_MARKET = "XNYS"


def get_trading_dates(
    start_date: date, end_date: date, include_start: bool = False
) -> list[date]:
    nyse = mcal.get_calendar(US_STOCK_MARKET)
    if not include_start:
        start_date = start_date + datetime.timedelta(days=1)
    schedule = nyse.schedule(
        start_date,
        end_date,
    )
    trading_days = schedule.index.date.tolist()
    return trading_days


def round_results(func):
    def inner(*args, **kwargs):
        results = func(*args, **kwargs)
        if isinstance(results, float):
            results = rnd(func(*args, **kwargs))
        return results

    return inner


def rnd(value: float) -> float:
    return round(value, 2)
