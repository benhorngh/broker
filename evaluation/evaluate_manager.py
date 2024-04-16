from prettytable import PrettyTable

import evaluate
from data_import import stocks_data
from managers.m_predictor import PredictorManager
from managers.m_top import TopPredictorManager
from predictors.p_democrat import DemocratPredictor
from predictors.p_ideal import IdealPredictor
from predictors.p_prophet import ProphetPredictor
from services import utils
from settings import settings

_ = (IdealPredictor, ProphetPredictor, DemocratPredictor)


def evaluate_manager():
    utils.setup_logs()
    cutoff = 5
    stocks = stocks_data.get_stocks(cutoff)
    symbol_to_stock = {stock.symbol: stock for stock in stocks}
    managers = [
        TopPredictorManager(IdealPredictor),
        TopPredictorManager(DemocratPredictor),
        TopPredictorManager(ProphetPredictor),
        # PredictorManager(ProphetPredictor),
        # PredictorManager(DemocratPredictor),
    ]

    manager_name_to_results = {}
    for manager in managers:
        symbol_to_plan = manager.handle(stocks, settings.consts.forecast_length)
        results = [
            evaluate.apply_plan(symbol_to_stock[symbol], plan)
            for symbol, plan in symbol_to_plan.items()
        ]
        manager_name_to_results[manager.name()] = results

    table = PrettyTable()
    table.field_names = ["Manager", "spent", "gross", "loss", "profit", "percent"]
    for manager_name, results in manager_name_to_results.items():
        table.add_row(
            [
                manager_name,
                evaluate.InvestResult.calc_spent(results),
                evaluate.InvestResult.calc_gross_profit(results),
                evaluate.InvestResult.calc_loss(results),
                evaluate.InvestResult.calc_profit(results),
                evaluate.InvestResult.calc_profit_percent(results),
            ]
        )
    print(table)


if __name__ == "__main__":
    evaluate_manager()
