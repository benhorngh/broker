from __future__ import annotations
import logging
from enum import Enum
from typing import Type, Optional

from pydantic import BaseModel

from predictors.p_ideal import IdealPredictor
from predictors.p_linear_regression import LinearRegressionPredictor
from predictors.p_prophet import ProphetPredictor
from predictors.p_random import RandomPredictor
from predictors.p_random_forest import RandomForestPredictor
from predictors.p_random_plan import RandomPlanPredictor
from predictors.predictor import Predictor
from services import stock_data, utils
from prettytable import PrettyTable

from services.datasets import Stock
from services.utils import rnd


class ScoreIcon(str, Enum):
    V = "V"
    VX = "~"
    X = "X"


class InvestResult(BaseModel):
    symbol: str
    invest: bool
    score_icon: Optional[ScoreIcon] = None
    spent: float = 0
    profit: float = 0

    @classmethod
    def calc_profit(cls, results: list[InvestResult]) -> float:
        return rnd(sum([res.profit for res in results]))

    @classmethod
    def calc_loss(cls, results: list[InvestResult]) -> float:
        return rnd(sum([res.profit for res in results if res.profit < 0]))

    @classmethod
    def calc_gross_profit(cls, results: list[InvestResult]) -> float:
        return rnd(sum([res.profit for res in results if res.profit > 0]))

    @classmethod
    def calc_spent(cls, results: list[InvestResult]) -> float:
        return rnd(sum([res.spent for res in results]))

    @classmethod
    def calc_score(cls, results: list[InvestResult]) -> float:
        points = {ScoreIcon.V: 1, ScoreIcon.VX: 0.5, ScoreIcon.X: 0}
        return sum([points[r.score_icon] for r in results])

    @classmethod
    def calc_percent_score(
        cls, ideal_results: list[InvestResult], predictor_results: list[InvestResult]
    ):
        ideal_results.sort(key=lambda x: x.symbol)
        predictor_results.sort(key=lambda x: x.symbol)
        for ideal, predictor in zip(ideal_results, predictor_results):
            if not ideal.invest:
                if not predictor.invest:
                    logging.debug(f"{ideal.symbol} V: skipped")
                    predictor.score_icon = ScoreIcon.V
                if predictor.invest:
                    logging.debug(
                        f"{ideal.symbol} X: Should skipped but invested. Lost {rnd(predictor.profit)}"
                    )
                    predictor.score_icon = ScoreIcon.X
            else:
                if not predictor.invest:
                    logging.debug(f"{ideal.symbol} X: Should invest but skipped")
                    predictor.score_icon = ScoreIcon.X
                if predictor.invest and 0 < predictor.profit == ideal.profit:
                    logging.debug(f"{ideal.symbol} V: Earned {predictor.profit}")
                    predictor.score_icon = ScoreIcon.V
                if predictor.invest and 0 < predictor.profit != ideal.profit:
                    logging.debug(
                        f"{ideal.symbol} VX: Earned {rnd(predictor.profit)} out of {rnd(ideal.profit)}"
                    )
                    predictor.score_icon = ScoreIcon.VX
                if predictor.invest and predictor.profit <= 0:
                    logging.debug(
                        f"{ideal.symbol} X: Lost {rnd(predictor.profit)}, could have earned {rnd(ideal.profit)}"
                    )
                    predictor.score_icon = ScoreIcon.X
        return cls.calc_profit(predictor_results) / cls.calc_profit(ideal_results) * 100


def handle_predictor(
    predictor_cls: Type[Predictor], stock: Stock, forecast_length: int
):
    predictor = predictor_cls(stock)
    predictor_plan = predictor.plan(forecast_length)
    if not predictor_plan.skip:
        buy_price = stock.actual_future_price_at(predictor_plan.buy)
        sell_price = stock.actual_future_price_at(predictor_plan.sell)
        profit = sell_price - buy_price
        return InvestResult(
            spent=buy_price, profit=profit, invest=True, symbol=stock.symbol
        )
    else:
        return InvestResult(invest=False, symbol=stock.symbol)


def evaluate(predictor_cls: Type[Predictor], stocks):
    forecast_length = 5
    logging.debug(f"Evaluating predictor {predictor_cls.name()}")
    ideal_results, predictor_results = [], []
    for stock in stocks:
        logging.debug(f"Stock {stock.symbol}:")
        ideal_results.append(handle_predictor(IdealPredictor, stock, forecast_length))
        predictor_results.append(
            handle_predictor(predictor_cls, stock, forecast_length)
        )

    logging.debug(f"\n___________")
    logging.debug(f"Ideal profit: {rnd(InvestResult.calc_profit(ideal_results))}")
    logging.debug(
        f"Predictor profit: {rnd(InvestResult.calc_profit(predictor_results))}"
    )
    logging.debug(
        f"Score {rnd(InvestResult.calc_percent_score(ideal_results, predictor_results))}%"
    )
    return predictor_results


def get_stocks(cutoff):
    return stock_data.get_stocks(cutoff)


def main():
    utils.setup_logs()
    cutoff = 8
    predictors_eval = [
        IdealPredictor,
        ProphetPredictor,
        RandomForestPredictor,
        LinearRegressionPredictor,
        # RandomPlanPredictor,
        # RandomPredictor,
    ]
    stocks = get_stocks(cutoff)[:5]
    table = PrettyTable()
    table.field_names = [
        "Predictor",
        *sorted([s.symbol for s in stocks]),
        "spent",
        "gross",
        "loss",
        "profit",
        "score",
    ]
    rows = []
    for p in predictors_eval:
        results = evaluate(p, stocks)
        results.sort(key=lambda x: x.symbol)
        rows.append((p, results))
    ideal, rest = rows[0], rows[1:]
    table.add_row(get_row(*ideal))
    rest.sort(key=lambda x: InvestResult.calc_score(x[1]), reverse=True)
    table.add_rows([get_row(*r) for r in rest])
    print(table)


def get_row(predictor: Type[Predictor], results: list[InvestResult]):
    gross = InvestResult.calc_gross_profit(results)
    loss = InvestResult.calc_loss(results)
    profit = InvestResult.calc_profit(results)
    spent = InvestResult.calc_spent(results)
    score = InvestResult.calc_score(results)

    if predictor == IdealPredictor:
        return [
            predictor.name(),
            *[rnd(res.profit) for res in results],
            spent,
            gross,
            loss,
            profit,
            score,
        ]

    return [
        predictor.name(),
        *[res.score_icon.value for res in results],
        spent,
        gross,
        loss,
        profit,
        score,
    ]


if __name__ == "__main__":
    main()
