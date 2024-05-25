from datetime import date

from pydantic import BaseModel

from common import stocks_data, utils
from common.models import ManageRequest
from common.symbols import SYMBOLS
from evaluate import compare_managers
from managers.top_manager import TopManager
from predictors.ideal_predictor import IdealPredictor
from predictors.random_predictor import RandomPredictor


class Settings(BaseModel):
    cutoff_date: date
    predict_until: date
    symbols: list[str]


settings = Settings(
    cutoff_date=date(year=2024, month=5, day=8),
    predict_until=date(year=2024, month=5, day=15),
    symbols=SYMBOLS[:3],
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
    random_m = TopManager().manage(
        ManageRequest(stocks=stocks, predict_until=settings.predict_until),
        RandomPredictor,
    )
    ideal_m = TopManager().manage(
        ManageRequest(stocks=stocks, predict_until=settings.predict_until),
        IdealPredictor,
    )
    compare_managers([ideal_m, random_m])
    # print_plan(random_m)


if __name__ == "__main__":
    run_prediction()
