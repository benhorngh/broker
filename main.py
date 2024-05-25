import logging
from datetime import date

from pydantic import BaseModel

from common import stocks_data, utils
from common.models import ManageRequest
from common.symbols import SYMBOLS
from evaluate import compare_managers
from managers.top_manager import TopManager
from predictors.ideal_predictor import IdealPredictor
from predictors.prophet_predictor import ProphetPredictor
from predictors.random_predictor import RandomPredictor


class Settings(BaseModel):
    cutoff_date: date
    predict_until: date
    symbols: list[str]


settings = Settings(
    cutoff_date=date(year=2024, month=2, day=27),
    predict_until=date(year=2024, month=3, day=5),
    symbols=SYMBOLS[:],
)

predictors = [IdealPredictor, RandomPredictor]


def run_prediction():
    print(settings.symbols)
    trading_days = utils.get_trading_dates(
        settings.cutoff_date, settings.predict_until, include_start=True
    )
    assert trading_days[0] == settings.cutoff_date
    assert trading_days[-1] == settings.predict_until

    stocks = stocks_data.get_stocks(settings.symbols, settings.cutoff_date)
    prophet_m = TopManager().manage(
        ManageRequest(stocks=stocks, predict_until=settings.predict_until),
        ProphetPredictor,
    )
    random_m = TopManager().manage(
        ManageRequest(stocks=stocks, predict_until=settings.predict_until),
        RandomPredictor,
    )
    ideal_m = TopManager().manage(
        ManageRequest(stocks=stocks, predict_until=settings.predict_until),
        IdealPredictor,
    )
    compare_managers([ideal_m, prophet_m, random_m])
    # print_plan(random_m)


def setup_logger():
    logging.getLogger("prophet").setLevel(logging.WARNING)
    logger = logging.getLogger("cmdstanpy")
    logger.addHandler(logging.NullHandler())
    logger.propagate = False
    logger.setLevel(logging.WARNING)


if __name__ == "__main__":
    setup_logger()
    run_prediction()
