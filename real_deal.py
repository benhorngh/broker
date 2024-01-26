import logging
import uuid
from datetime import date, datetime

from managers.m_predictor import PredictorManager
from managers.manager import Manager
from predictors.p_prophet import ProphetPredictor
from predictors.p_random_forest import RandomForestPredictor
from settings import settings
from services import firestore_db, interactive_brokers, stock_data, utils
from services.datasets import Stock
from services.firestore_db import firebase_client


def create_future_actions(stocks: list[Stock], forecast_length: int):
    manager = PredictorManager(ProphetPredictor)
    add_future_actions(manager, forecast_length, stocks)


def do_today_actions(today_date: date):
    pending_actions = firestore_db.get_pending_actions()
    pending_actions = [
        action for action in pending_actions if action.when <= today_date
    ]
    if not pending_actions:
        logging.info("No pending actions for today")
    else:
        logging.info(f"Pending actions found. {len(pending_actions)} actions")
    for action in pending_actions:
        interactive_brokers.trade(action)
        firestore_db.mark_done(action.action_id)


def add_future_actions(manager: Manager, length: int, stocks: list[Stock]):
    calculation_id = str(uuid.uuid4())
    stocks_to_avoid = avoid_stocks()
    stocks = [stock for stock in stocks if stock.symbol not in stocks_to_avoid]
    actions = manager.handle(stocks, length)
    for action in actions:
        action.calculation_id = calculation_id
        action.created_at = datetime.utcnow()
        firestore_db.save_action(action)


def avoid_stocks():
    actions = firestore_db.get_pending_actions()
    symbols = [action.symbol for action in actions]
    return symbols


def real_deal():
    utils.setup_logs()
    settings.init()
    firebase_client.start()

    cutoff = 0
    forecast_length = 5
    stocks = stock_data.get_stocks(cutoff)
    next_day = utils.get_next_trading_dates(stocks[0].last_day, 1)[0]

    create_future_actions(stocks, forecast_length)
    # do_today_actions(next_day)


if __name__ == "__main__":
    real_deal()
