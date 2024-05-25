from datetime import date

from common.models import Value


def combine_values(dates: list[date], prices: list[float]) -> list[Value]:
    assert len(dates) == len(
        prices
    ), f"Missing or too many prices, days: {len(dates)}, prices: {len(prices)}"
    return [Value(day=day, price=price) for day, price in zip(dates, prices)]
