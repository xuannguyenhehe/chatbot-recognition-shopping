import io
import json
import sys
from enum import Enum
from typing import List
import base64

from app.models.image import Image as ImageModel
from app.models.message import Message as MessageModel
from app.schemas.message import MessageInput, MessageOutput, MessageResponse
from app.services import AppCRUD, AppService
from app.services.chat import ChatCRUD
from app.services.image import ImageCRUD
from app.services.user import UserCRUD
from app.utils.repsonse.exceptions import ExceptionResponse
from app.utils.repsonse.result import ResultResponse
from extensions.minio.connector import MinioConnector, ObjectType
from fastapi import status as sta
from PIL import Image as PILImage


class IntentType(str, Enum):
    ASK_TYPE = "ask_type"
    NO_EXIST_TYPE = "ask_no_exist_type"
    ANSWER_TYPE = "Shop gợi ý 5 mẫu có thể phù hợp với yêu cầu của bạn!"
    SORRY_TYPE = "Thật tiếc! Shop không tìm thấy mẫu phù hợp cho bạn :("
    DENY = "deny"
    GREET = "greet"
    GOODBYE = "goodbye"
    HAVE_IMAGE = "have_image"
    HAVE_NO_IMAGE = "have_no_image"
    MOOD_GREAT = "mood_great"
    MOOD_OKE = "mood_oke"
    MOOD_UNHAPPY = "mood_unhappy"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, IntentType))

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_



class MessageService(AppService):
    def create(self, storage: MinioConnector, chat_id: int, username: str, message_obj: MessageInput) -> ResultResponse:
        message_response = []
        exist_user = UserCRUD(self.db).get(username)
        if not exist_user:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "username": username,
            }))
        exist_chat = ChatCRUD(self.db).get(username, id=chat_id)
        if not exist_chat:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "chat id": chat_id,
            }))
        
        path_image = None
        if message_obj.image:
            filename = message_obj.image.filename
            base64_image = message_obj.image.data.split(',')[1]
            base64_image = base64.b64decode(base64_image)
            data = io.BytesIO(base64_image)
            path_image = storage.save_object(filename, data, ObjectType.IMAGE)
            width_image, height_image = PILImage.open(data).size
            volume_image = sys.getsizeof(base64_image)
            image = ImageModel(
                path=path_image,
                height=height_image,
                width=width_image,
                volume=volume_image,
            )
            message, status_code = ImageCRUD(self.db).create(image)
            if status_code != sta.HTTP_200_OK:
                return ResultResponse(ExceptionResponse.ErrorServer(message))
        
        message_output = MessageOutput(
            message=message_obj.message,
            path_image=path_image,
            is_from_self=message_obj.is_from_self
        )
        message_response.append(message_output.dict())
        message, status_code = MessageCRUD(self.db).create(chat_id, username, message_output)
        if status_code != sta.HTTP_200_OK:
            return ResultResponse(ExceptionResponse.ErrorServer(message))

        intent, entities = self.get_intent_entities_message(username, message_obj.message)
        if intent in IntentType.list():
            if path_image or intent == IntentType.HAVE_NO_IMAGE:
                entities = exist_chat[0]["current_entities"]
                response_recommend_images = self.get_recommend_images(entities, path_image)
                if len(response_recommend_images) > 0:
                    message_output = MessageOutput(
                        message=IntentType.ANSWER_TYPE,
                        is_from_self=False,
                    )
                    message, status_code = MessageCRUD(self.db).create(chat_id, username, message_output)
                    message_response.append(message_output.dict())
                    for path_image in response_recommend_images:
                        message_output = MessageOutput(
                            message="",
                            path_image=path_image,
                            is_from_self=False,
                        )
                        message, status_code = MessageCRUD(self.db).create(chat_id, username, message_output)
                        if status_code != sta.HTTP_200_OK:
                            return ResultResponse(ExceptionResponse.ErrorServer(message))                    
                        message_response.append(message_output.dict())
                else:
                    message_output = MessageOutput(
                        message=IntentType.SORRY_TYPE,
                        is_from_self=False,
                    )
                    message, status_code = MessageCRUD(self.db).create(chat_id, username, message_output)
                    message_response.append(message_output.dict())
            else:
                text = self.get_answer_message(
                    username=username,
                    message=message_obj.message,
                )
                if text:
                    message_output = MessageOutput(
                        message=text,
                        is_from_self=False,
                    )
                    message, status_code = MessageCRUD(self.db).create(chat_id, username, message_output)
                    if status_code != sta.HTTP_200_OK:
                        return ResultResponse(ExceptionResponse.ErrorServer(message))
                    message_response.append(message_output.dict())

                if intent == IntentType.ASK_TYPE and len(entities) > 0:
                    message, status_code = ChatCRUD(self.db).update_current_entities(chat_id, username, entities)
                elif intent == IntentType.DENY:
                    message, status_code = ChatCRUD(self.db).update_current_entities(chat_id, username, [])

            return ResultResponse((None, status_code, message_response))
        else:
            return ResultResponse(ExceptionResponse.ErrorServer(message))

    def get(self, chat_id: int, username: str) -> ResultResponse:
        exist_user = UserCRUD(self.db).get(username)
        if not exist_user:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "username": username,
            }))
        exist_chat = ChatCRUD(self.db).get(username, id=chat_id)
        if not exist_chat:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "chat id": chat_id,
            }))
        messages = MessageCRUD(self.db).get(chat_id, username)
        return ResultResponse((None, sta.HTTP_200_OK, messages))
    

    def get_intent_entities_message(self, username: str, message: str) -> str:
        url = "/api/rasa-service/v1/answer/intent"
        payload = {
            "sender": username,
            "message": message,
        }
        data, _ = self.call_api(url, payload, "post")
        intent = data["intent"]["name"]
        entities = data["entities"]
        return intent, entities
    
    def get_answer_message(self, username: str, message: str) -> str:
        url = "/api/rasa-service/v1/answer"
        payload = {
            "sender": username,
            "message": message,
        }
        data, _ = self.call_api(url, payload, "post")
        if len(data) > 0:
            text = data[0]["text"]
        else:
            text = None
        return text
    
    def get_recommend_images(self, entities: list, path_image: str) -> List[str]:
        url = "/api/meta-service/v1/inference"
        payload = {
            "entities": entities,
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return data


class MessageCRUD(AppCRUD):
    def create(self, chat_id: int, username: str, message: MessageOutput) -> MessageResponse:
        messages = []
        if len(message.message):
            messages.append(MessageModel(
                message=message.message, 
                chat_id=chat_id, 
                username=username,
                is_from_self=message.is_from_self,
            ))
        if message.path_image:
            messages.append(MessageModel(
                message="", 
                chat_id=chat_id, 
                username=username,
                is_from_self=message.is_from_self,
                path_image=message.path_image
            ))
        if len(messages) > 0:
            message, status_code = self.insert("Message", self.serialize_list(messages))
            return message, status_code
        else:
            return None, sta.HTTP_200_OK

    def get(self, chat_id: int, username: str) -> List[MessageResponse]:
        query = {
            "username": username,
            "chat_id": chat_id,
            "is_active": True,
        }
        no_query = {
            "_id": False,
            "is_active": False,
        }
        messages = list(self.db.Message.find(query, no_query))
        return messages