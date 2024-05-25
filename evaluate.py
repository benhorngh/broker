from datetime import date

from prettytable import PrettyTable

from common import stocks_data
from common.models import PredictionResponse, Transaction, Action, ManageResponse, Stock


def evaluate_prediction(prediction_result: PredictionResponse):
    buy = prediction_result.request.stock.get_last_value()
    sell = prediction_result.values[-1]
    expected_sell_price = prediction_result.values[-1].price
    actual_sell_price = get_actual_sell_price(prediction_result.request.stock, sell.day)
    if buy.price > expected_sell_price:
        return Transaction(action=Action.SKIP, stock=prediction_result.request.stock)
    return Transaction(
        action=Action.BUY,
        buy=buy.day,
        sell=sell.day,
        expected_sell_price=expected_sell_price,
        actual_sell_price=actual_sell_price,
        stock=prediction_result.request.stock,
    )


def get_actual_sell_price(stock: Stock, sell_day: date):
    if sell_day <= date.today():
        return (
            stocks_data.get_stocks([stock.symbol], sell_day)[0]
            .get_by_day(sell_day)
            .price
        )


def compare_managers(manage_responses: list[ManageResponse]):
    table = PrettyTable()
    table.field_names = [
        "Manager",
        "Spent",
        "Expected profit",
        "Actual profit",
        "%",
        "#",
        "fee",
    ]
    for res in manage_responses:
        table.add_row(
            [
                res.name,
                res.spent,
                res.expected_profit,
                res.actual_profit or "?",
                res.profit_percent or "?",
                res.number_of_stocks,
                res.ibkr_fee,
            ]
        )
    print(table)


def print_plan(manage_response: ManageResponse):
    table = PrettyTable()
    table.field_names = [
        "Stock",
        "Buy on",
        "Sell on",
        "Spent",
        "Expected profit",
    ]
    for transaction in manage_response.transactions:
        if transaction.action == Action.SKIP:
            continue
        table.add_row(
            [
                transaction.stock.symbol,
                transaction.buy,
                transaction.sell,
                transaction.buy_price,
                transaction.expected_profit,
            ]
        )
    print(table)
    print("Total fee:", manage_response.ibkr_fee)
