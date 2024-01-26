import json
import os

import requests

from services.datasets import Stock, Day
from settings import settings

endpoint = "https://www.alphavantage.co/query"

SYMBOLS = {
    "GE",
    "SLB",
    "KR",
    "EOG",
    "CVS",
    "ROKU",
    "SQ",
    "DOCU",
    "TWLO",
    "FIVN",
    "TTD",
    "JCI",
    "DUK",
    "DAL",
    "INTC",
    "MS",
    "BMY",
    "NEE",
}
# SYMBOLS = {'TWLO', 'FIVN', 'TTD', 'JCI', 'DUK', 'DAL', 'INTC', 'MS', 'BMY', 'NEE'}
FILE_PATH = os.path.join(os.path.dirname(__file__), "stocks_data_cache.json")


def save_stocks(symbols: list[str]):
    stocks = {}
    for symbol in symbols:
        stocks[symbol] = get_worth(symbol)

    with open(FILE_PATH, "w") as json_file:
        json.dump(stocks, json_file, indent=4)


def get_stocks(cutoff: int):
    with open(FILE_PATH, "r") as json_file:
        loaded_dict = json.load(json_file)
    stocks = []
    for stock_symbol, stock_response in loaded_dict.items():
        days = []
        for day, prices in stock_response["Time Series (Daily)"].items():
            days.append(Day(day=day, price=float(prices["4. close"])))
        days.sort(key=lambda x: x.day)
        stock = Stock(raw_data=days, symbol=stock_symbol, cutoff=cutoff)
        stocks.append(stock)
    return stocks


def get_worth(symbol: str):
    settings.init()
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": settings.config.ALPHAVANTAGE__API_KEY,
    }
    raise ValueError()
    # response = requests.get(endpoint, params=params)
    # data = response.json()
    # return data


def get_current_price(symbol: str):
    settings.init()
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": settings.config.ALPHAVANTAGE__API_KEY,
    }
    raise ValueError()
    # response = requests.get(endpoint, params=params)
    # data = response.json()
    # return data


if __name__ == "__main__":
    save_stocks(list(SYMBOLS))
    # get_stocks(5)
    # print(get_current_price(SYMBOLS.pop()))
