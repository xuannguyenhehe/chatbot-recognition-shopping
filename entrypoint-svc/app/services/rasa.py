from typing import List

import requests
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
        qa_inputs = QACRUD(self.db).get(username)
        # training model and save in S3, then return path
        RasaModelCRUD(self.db).create(username, None)
        status_code = self._train(username, qa_inputs)
        if status_code == requests.codes.ok:
            RasaModelCRUD(self.db).update_path(username, None, "trained")
            return ResultResponse(('Train sucessfull', status_code))
        else:
            RasaModelCRUD(self.db).update_path(username, None, "failed")
            return ResultResponse(('Train failed', status_code))
        
        
    def approve(self, username: str) -> ResultResponse:
        exist_rasa_ckpt = RasaModelCRUD(self.db).get(
            username=username,
        )
        if not exist_rasa_ckpt:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "Rasa Checkpoint": username,
            }))
        
        path = self._approve(username)
        RasaModelCRUD(self.db).update_path(username, path, "approved")
        return ResultResponse(('Approved new checkpoint', status.HTTP_200_OK))
    
    def check_status_train(self, username: str) -> ResultResponse:
        exist_rasa_ckpt = RasaModelCRUD(self.db).get(
            username=username,
        )
        if not exist_rasa_ckpt:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "Rasa Checkpoint": username,
            }))

        if exist_rasa_ckpt[0]['status'] == "approved":
            return ResultResponse(("Model is approved", requests.codes.ok, "approved"))
        
        status_code = self._check_status_train(username)
        if status_code == requests.codes.ok:
            msg = "Model trained"
            data = "trained"
            RasaModelCRUD(self.db).update_path(username, None, "trained")
        else:
            msg = "Model is training"
            data = "training"
            RasaModelCRUD(self.db).update_path(username, None, "training")
        return ResultResponse((msg, requests.codes.ok, data))
    
    def _train(self, username: str, qa_inputs: list) -> str:
        url = "/rasa/v1/train"
        payload = {
            "username": username,
            "data": {
                "intents": qa_inputs
            },
        }
        _, status_code = self.call_api(url, payload, "post")
        return status_code
    
    def _approve(self, username: str) -> str:
        url = "/rasa/v1/answer/approve"
        payload = {
            "username": username,
        }
        data, _ = self.call_api(url, payload, "post")
        return data
    
    def _check_status_train(self, username: str) -> str:
        url = "/rasa/v1/answer/status-train"
        payload = {
            "username": username,
        }
        _, status_code = self.call_api(url, payload, "get")
        return status_code


class RasaModelCRUD(AppCRUD):
    def create(self, username: str, path_model: str):
        rasa_model = RasaCheckpoint(username=username, path=path_model, status="training")
        message, status_code = self.insert("RasaCheckpoint", self.serialize(rasa_model))
        return message, status_code
    
    def get(self, username: str) -> RasaValid:
        query = {
            'username': username,
        }
        no_query = {
            "_id": False,
            "is_active": False,
            "created_date": False,
            "updated_date": False,
        }
        qa_output = list(self.db.RasaCheckpoint.find(query, no_query))
        return qa_output

    def update_path(self, username, path: str, status: str):
        query_data = {
            "username": username,
        }
        update_data = {
            "path": path,
            "status": status,
        }
        message, status_code = self.update("RasaCheckpoint", query_data, update_data)
        return message, status_code