from typing import List

import pymongo
from fastapi import status

from app.models.rasa import RasaCheckpoint
from app.schemas.rasa import RasaValid
from app.services.qa import QACRUD
from app.services import AppCRUD, AppService
from app.utils.repsonse.exceptions import ExceptionResponse
from app.utils.repsonse.result import ResultResponse


class RasaModelService(AppService):
    def get(self, username: str) -> ResultResponse:
        chats = RasaModelCRUD(self.db).get(username=username)
        return ResultResponse((None, status.HTTP_200_OK, chats))

    def create(self, username: str) -> ResultResponse:
        exist_rasa_ckpt = RasaModelCRUD(self.db).get(
            username=username,
        )
        if exist_rasa_ckpt:
            return ResultResponse(ExceptionResponse.ExistedError({
                "Rasa Checkpoint": username,
            }))
        
        qa_input = QACRUD(self.db).get(username)
        # training model and save in S3, then return path
        path_model = None
        message, status_code = RasaModelCRUD(self.db).create(username, path_model)
        return ResultResponse((message, status_code))


class RasaModelCRUD(AppCRUD):
    def create(self, username: str, path_model: str):
        rasa_model = RasaCheckpoint(username=username, path=path_model)
        message, status_code = self.insert("RasaCheckpoint", self.serialize(rasa_model))
        return message, status_code
    
    def get(self, username: str) -> RasaValid:
        query = {
            username: username,
        }
        no_query = {
            "_id": False,
            "is_active": False,
            "created_date": False,
            "updated_date": False,
        }
        qa_output = list(self.db.RasaModel.find(query, no_query))[0]
        return qa_output
