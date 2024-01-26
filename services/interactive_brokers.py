import logging
import random

from services.firestore_db import Action


def trade(action: Action):
    logging.info(
        f"Trading: {action.action_type} {action.symbol} for {action.how_many_stocks}"
    )
    return random.randint(1, 100)
