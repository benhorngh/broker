import os
from datetime import datetime, timedelta

import pandas as pd
import yfinance as yf

from services.datasets import Stock, Day
from data_import.symbols import SYMBOLS

CACHE_FILE_PATH = os.path.join(
    os.path.dirname(__file__), ".cache/yfinance_stocks_data.json"
)


def save_stocks(stocks_symbols: list[str]):
    today = datetime.today()
    last_year = today - timedelta(days=365)
    data = yf.download(
        stocks_symbols, start=str(last_year.date()), end=str(today.date())
    )

    closing_data: pd.DataFrame = data["Adj Close"]
    closing_data.to_csv(CACHE_FILE_PATH)


def get_stocks(cutoff: int):
    data = pd.read_csv(CACHE_FILE_PATH)
    date_col = "Date"
    stocks = []
    for symbol in data.columns:
        if symbol == date_col:
            continue
        d = data[[date_col, symbol]]
        days = []
        for index, row in d.iterrows():
            days.append(Day(day=row[date_col], price=row[symbol]))
        days.sort(key=lambda x: x.day)
        stocks.append(Stock(raw_data=days, symbol=symbol, cutoff=cutoff))
    return stocks


if __name__ == "__main__":
    # save_stocks(SYMBOLS)
    print(get_stocks(5))
