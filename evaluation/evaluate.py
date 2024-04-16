from __future__ import annotations

import logging
from enum import Enum
from typing import Type, Optional

from prettytable import PrettyTable
from pydantic import BaseModel

from data_import import stocks_data
from predictors.p_ideal import IdealPredictor
from predictors.predictor import Predictor
from services import utils
from services.datasets import Stock
from services.strategy import Strategy
from services.utils import rnd
from settings import settings


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
    plan: Strategy

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
    def calc_profit_percent(cls, results: list[InvestResult]) -> float:
        return rnd(cls.calc_profit(results) / cls.calc_spent(results) * 100)

    @classmethod
    def calc_score(cls, results: list[InvestResult]) -> float:
        points = {ScoreIcon.V: 1, ScoreIcon.VX: 0.5, ScoreIcon.X: 0}
        return sum([points[r.score_icon] for r in results])

    @classmethod
    def update_scores(
        cls, ideal_results: list[InvestResult], predictor_results: list[InvestResult]
    ):
        ideal_results.sort(key=lambda x: x.symbol)
        predictor_results.sort(key=lambda x: x.symbol)
        for ideal, predictor in zip(ideal_results, predictor_results):
            if not ideal.invest:
                if not predictor.invest:
                    # skipped as should have
                    predictor.score_icon = ScoreIcon.V
                elif predictor.invest:
                    # should have skipped but invested
                    predictor.score_icon = ScoreIcon.X
            else:
                if not predictor.invest:
                    # Should invest but skipped
                    predictor.score_icon = ScoreIcon.X
                elif predictor.invest and 0 < predictor.profit == ideal.profit:
                    # Invest as should
                    predictor.score_icon = ScoreIcon.V
                elif predictor.invest and 0 < predictor.profit != ideal.profit:
                    # Invest but sell on the wrong day and earned less
                    predictor.score_icon = ScoreIcon.VX
                elif predictor.invest and predictor.profit <= 0:
                    # invest but lost
                    predictor.score_icon = ScoreIcon.X


def handle_predictor(
    predictor_cls: Type[Predictor], stock: Stock, forecast_length: int
) -> InvestResult:
    predictor = predictor_cls(stock)
    predictor_plan = predictor.plan(forecast_length)
    return apply_plan(stock, predictor_plan)


def apply_plan(stock: Stock, plan: Strategy) -> InvestResult:
    if not plan.skip:
        buy_price = stock.actual_future_price_at(plan.buy)
        sell_price = stock.actual_future_price_at(plan.sell)
        profit = sell_price - buy_price
        return InvestResult(
            spent=buy_price,
            profit=profit,
            invest=True,
            symbol=stock.symbol,
            plan=plan,
        )
    else:
        return InvestResult(invest=False, symbol=stock.symbol, plan=plan)


def evaluate_predictor(predictor_cls: Type[Predictor], stocks):
    forecast_length = settings.consts.forecast_length
    logging.debug(f"Evaluating predictor {predictor_cls.name()}")
    ideal_results, predictor_results = [], []
    for i, stock in enumerate(stocks):
        logging.debug(f"{i}/{len(stocks)} | {stock.symbol}")
        ideal_results.append(handle_predictor(IdealPredictor, stock, forecast_length))
        predictor_results.append(
            handle_predictor(predictor_cls, stock, forecast_length)
        )
    InvestResult.update_scores(ideal_results, predictor_results)
    return predictor_results


def get_row(
    predictor: Type[Predictor],
    results: list[InvestResult],
    by_expected_profit: bool = False,
    by_score: bool = False,
):
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
    if by_score:
        vals = [res.score_icon.value for res in results]
    elif by_expected_profit:
        vals = [res.plan.expected_profit for res in results]
    else:
        vals = [res.score_icon.value for res in results]
    return [
        predictor.name(),
        *vals,
        spent,
        gross,
        loss,
        profit,
        score,
    ]


def eval_one_predictor(predictor: Type[Predictor]):
    utils.setup_logs()
    cutoff = 5
    stocks = stocks_data.get_stocks(cutoff)[:5]
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
    all_results = []
    for p in [IdealPredictor, predictor]:
        results = evaluate_predictor(p, stocks)
        results.sort(key=lambda x: x.symbol)
        all_results.append(results)
    ideal_results, predictor_results = all_results
    table.add_row(get_row(IdealPredictor, ideal_results))
    table.add_row(get_row(predictor, predictor_results, by_score=True))
    table.add_row(get_row(predictor, predictor_results, by_expected_profit=True))
    print("\n\n")
    print(table)


def compare_predictors(predictors: list[Type[Predictor]]):
    utils.setup_logs()
    cutoff = 5

    stocks = stocks_data.get_stocks(cutoff)[3:17]
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
    all_results = []
    for p in [IdealPredictor, *predictors]:
        results = evaluate_predictor(p, stocks)
        results.sort(key=lambda x: x.symbol)
        all_results.append((p, results))
    ideal_results, predictors_results = all_results[0], all_results[1:]

    table.add_row(get_row(*ideal_results))
    predictors_results.sort(key=lambda x: InvestResult.calc_score(x[1]), reverse=True)
    table.add_rows([get_row(*r) for r in predictors_results])
    print("\n\n")
    print(table)
    highest_profit = sorted(
        predictors_results, key=lambda x: InvestResult.calc_profit(x[1]), reverse=True
    )[0]
    lowest_loss = sorted(
        predictors_results, key=lambda x: InvestResult.calc_loss(x[1]), reverse=True
    )[0]
    lowest_spend = sorted(
        predictors_results, key=lambda x: InvestResult.calc_spent(x[1]), reverse=True
    )[0]
    print("Highest profit:", highest_profit[0].name())
    print("Lowest loss:", lowest_loss[0].name())
    print("Lowest spend:", lowest_spend[0].name())
