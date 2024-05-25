from old.data_import import yfinance_stocks


def get_stocks(cutoff: int):
    return yfinance_stocks.get_stocks(cutoff)
