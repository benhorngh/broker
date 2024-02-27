import datetime
import sys
from datetime import date

import pandas_market_calendars as mcal

US_STOCK_MARKET = "XNYS"


def setup_logs():
    import logging

    logging.getLogger("prophet").setLevel(logging.WARNING)

    logger = logging.getLogger("cmdstanpy")
    logger.addHandler(logging.NullHandler())
    logger.propagate = False
    logger.setLevel(logging.CRITICAL)

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def get_next_trading_dates(start_date: date, num_dates: int = 5) -> list[date]:
    nyse = mcal.get_calendar(US_STOCK_MARKET)

    schedule = nyse.schedule(
        start_date + datetime.timedelta(days=1),
        start_date + datetime.timedelta(days=365),
    )
    trading_days = schedule.index.date.tolist()
    next_trading_dates = trading_days[:num_dates]
    return next_trading_dates


def round_list(output: list[float]) -> list[float]:
    return [rnd(o) for o in output]


def rnd(value: float) -> float:
    return round(value, 2)
