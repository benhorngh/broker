import logging
import tempfile
from datetime import date, datetime
from enum import Enum
from typing import Optional

import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1 import FieldFilter
from pydantic import BaseModel

from settings import settings


class FirestoreCollections(str, Enum):
    INVESTOR = "investor"


# class ActionType(str, Enum):
#     BUY = "buy"
#     SKIP = "skip"


# class ActionStatus(str, Enum):
#     PENDING = "pending"
#     DONE = "done"
#
#
# class Action(BaseModel):
#     created_at: Optional[datetime] = None
#     done_at: Optional[datetime] = None
#     calculation_id: Optional[str] = None
#     actual_price: Optional[float] = None
#     action_id: str
#     manager: str
#     action_type: ActionType
#     symbol: str
#     when: date
#     how_many_stocks: float
#     status: ActionStatus
#
#
# class FirebaseClient:
#     _client = None
#
#     @classmethod
#     def start(cls, credentials_json: str = None):
#         credentials_json = credentials_json or settings.config.GCP__CREDENTIALS_JSON
#         if FirebaseClient._client is None:
#             tmp = tempfile.NamedTemporaryFile(mode="w", delete=False)
#
#             with open(tmp.name, "w") as f:
#                 f.write(credentials_json)
#             cred = credentials.Certificate(tmp.name)
#             firebase_admin.initialize_app(cred)
#             FirebaseClient._client = firestore.client()
#
#     @property
#     def client(self):
#         if FirebaseClient._client is None:
#             raise Exception("Firestore client not started yet")
#         return FirebaseClient._client
#
#
# def get_collection(client):
#     return client.collection(FirestoreCollections.INVESTOR)
#
#
# firebase_client = FirebaseClient()
#
#
# def save_action(action: Action):
#     logging.info("Saving new action in Firestore")
#     model = action.model_dump()
#     model["when"] = str(model["when"])
#     get_collection(firebase_client.client).document(action.action_id).set(model)
#
#
# def mark_done(action_id: str):
#     logging.info("Marking action as done in Firestore")
#     get_collection(firebase_client.client).document(action_id).update(
#         {"status": ActionStatus.DONE, "done_at": datetime.utcnow()}
#     )
#
#
# def get_pending_actions() -> list[Action]:
#     logging.info("Getting pending actions from Firestore")
#     query = get_collection(firebase_client.client).where(
#         filter=FieldFilter("status", "==", ActionStatus.PENDING)
#     )
#     actions = query.stream()
#     return [Action(**a.to_dict()) for a in actions]
