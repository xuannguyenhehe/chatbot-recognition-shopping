import json

import requests
from fastapi import status

from app.schemas.inference import InferenceInput, IntentInput
from app.utils.repsonse.result import ResultResponse
from rasa.core.agent import Agent
from rasa.core.channels import UserMessage


class InferenceService():
    def __init__ (self, config):
        self.model = Agent.load(config['CHECKPOINT_PATH'])
        # self.model = None

    async def get_answer(self, input: InferenceInput) -> ResultResponse:
        user_message = UserMessage(sender_id=input.sender, text=input.message)
        message = await self.model.handle_message(user_message)
        # url = "http://192.168.1.217:5005/webhooks/rest/webhook"
        # payload = json.dumps({
        #     "sender": input.sender,
        #     "message": input.message,
        # })
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        return ResultResponse((None, status.HTTP_200_OK, message))
    
    async def get_intent(self, message: IntentInput) -> ResultResponse:
        message = await self.model.parse_message(message.message)
        # url = "http://192.168.1.217:5005/model/parse"
        # payload = json.dumps({
        #     "text": input.message,
        # })
        # headers = {
        #     'Content-Type': 'application/json'
        # }
        # response = requests.request("POST", url, headers=headers, data=payload)
        return ResultResponse((None, status.HTTP_200_OK, message))
