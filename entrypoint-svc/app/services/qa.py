from typing import List

import pymongo
from fastapi import status

from app.models.qa import QA as QAModel
from app.schemas.qa import QAValid, QAValids
from app.services import AppCRUD, AppService
from app.utils.repsonse.exceptions import ExceptionResponse
from app.utils.repsonse.result import ResultResponse


class QAService(AppService):
    def get(self, username: str) -> ResultResponse:
        chats = QACRUD(self.db).get(username=username)
        return ResultResponse((None, status.HTTP_200_OK, chats))

    def create(self, username: str, qa_inputs: QAValids) -> ResultResponse:
        message, status_code = QACRUD(self.db).create(username, qa_inputs)
        return ResultResponse((message, status_code))


class QACRUD(AppCRUD):
    def create(self, username: str, qa_inputs: QAValids):
        qa_model = [QAModel(username=username, **qa_input.dict()) for qa_input in qa_inputs.intents]
        self.db.QA.delete_many({'username': username})
        message, status_code = self.insert("QA", self.serialize_list(qa_model))
        return message, status_code

    def get(self, username: str) -> QAValid:
        query = {
            'username': username,
        }
        no_query = {
            "_id": False,
            "is_active": False,
            "created_date": False,
            "updated_date": False,
        }
        qa_output = list(self.db.QA.find(query, no_query))
        return qa_output
