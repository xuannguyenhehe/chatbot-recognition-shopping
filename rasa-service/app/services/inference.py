from app.schemas.inference import InferenceInput
from app.utils.repsonse.result import ResultResponse
from fastapi import status
import requests
import json
# from rasa.core.channels import UserMessage
# from rasa.core.agent import Agent

class InferenceService():
    def __init__ (self):
        # self.model = Agent.load(checkpoint_path)
        pass

    def get_answer(self, input: InferenceInput) -> ResultResponse:
        # user_message = UserMessage(sender_id=input.sender, text=input.message)
        # message = await self.model.handle_message("user_message")
        url = "http://192.168.1.217:5005/webhooks/rest/webhook"
        payload = json.dumps({
            "sender": input.sender,
            "message": input.message,
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return ResultResponse((None, status.HTTP_200_OK, response.json()))
    
    def get_intent(self, input: InferenceInput) -> ResultResponse:
        # user_message = UserMessage(sender_id=input.sender, text=input.message)
        # message = await self.model.handle_message("user_message")
        url = "http://192.168.1.217:5005/model/parse"
        payload = json.dumps({
            "text": input.message,
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return ResultResponse((None, status.HTTP_200_OK, response.json()))