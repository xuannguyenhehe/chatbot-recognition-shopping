import json

from minio.error import S3Error
from fastapi import status

from app.schemas.inference import InferenceInput, IntentInput
from app.utils.repsonse.result import ResultResponse
from rasa.core.agent import Agent
from rasa.core.channels import UserMessage
import os


class InferenceService():
    def __init__ (self, config):
        self.model = Agent.load('tmp/test_shop/test_shop.tar.gz')
        self.bucket_name = 'rasa'
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

    async def approve(self, storage, username: str) -> ResultResponse:
        file_path = f'tmp/{username}/{username}.tar.gz'
        with open(file_path, "rb") as file_data:
            file_stat = os.stat(file_path)
            # Upload the .gz file
            storage.client.put_object(self.bucket_name, f'{username}.tar.gz', file_data, file_stat.st_size)
        
        s3_path = os.path.join(self.bucket_name, f'{username}.tar.gz')
        self.model = Agent.load(file_path)
        return ResultResponse((s3_path, status.HTTP_200_OK, f'Approve {username} chatbot successful'))
    
    async def get_status_train(self, username: str) -> ResultResponse:
        if os.path.exists(f'tmp/{username}/{username}.tar.gz'):
            return ResultResponse((None, status.HTTP_200_OK, 'Trained'))
        else:
            return ResultResponse((None, status.HTTP_404_NOT_FOUND, 'Not trained yet'))