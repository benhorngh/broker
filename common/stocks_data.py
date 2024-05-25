import os
from datetime import datetime, timedelta, date
from functools import lru_cache

import pandas as pd
import yfinance as yf

from common.models import Value, Stock
from common.symbols import SYMBOLS

_ = SYMBOLS
cache_path = ".cache/"
CACHE_FILE_PATH = os.path.join(
    os.path.dirname(__file__), cache_path, "yfinance_stocks_data.json"
)

DATE_COL = "Date"
ADJ_CLOSE_PRICE_COL = "Adj Close"
CLOSE_PRICE_COL = "Close"


def save_stocks(stocks_symbols: list[str]):
    today = datetime.today()
    last_year = today - timedelta(days=365)
    data = yf.download(
        stocks_symbols, start=str(last_year.date()), end=str(today.date())
    )

    closing_data: pd.DataFrame = data[CLOSE_PRICE_COL]
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    closing_data.to_csv(CACHE_FILE_PATH)


def get_current_price(symbol):
    ticker = yf.Ticker(symbol)
    today_data = ticker.history(period="1d")
    return today_data[CLOSE_PRICE_COL].iloc[0]


@lru_cache
def read_cache_file():
    return pd.read_csv(CACHE_FILE_PATH)


def dataframe_to_stocks(df: pd.DataFrame):
    stocks = []
    for symbol in df.columns:
        if symbol == DATE_COL:
            continue
        d = df[[DATE_COL, symbol]]
        values = []
        for index, row in d.iterrows():
            values.append(Value(day=row[DATE_COL], price=row[symbol]))
        values.sort(key=lambda x: x.day)
        stocks.append(Stock(values=values, symbol=symbol))
    return stocks


def filter_by_symbols(df: pd.DataFrame, symbols: list[str]) -> pd.DataFrame:
    return df[[DATE_COL, *symbols]]


def filter_by_date(df: pd.DataFrame, cutoff_date: date) -> pd.DataFrame:
    return df[df[DATE_COL] <= str(cutoff_date)]


def get_stocks(symbols: list[str], cutoff_date: date = None) -> list[Stock]:
    df = read_cache_file()
    df = filter_by_symbols(df, symbols)
    if cutoff_date:
        df = filter_by_date(df, cutoff_date)
    stocks = dataframe_to_stocks(df)
    return stocks


if __name__ == "__main__":
    # save_stocks(SYMBOLS)
    print(get_stocks(SYMBOLS, date(year=2024, month=4, day=30))[0].values[-1])
    print(get_stocks(SYMBOLS, date.today())[0].values[-1])
