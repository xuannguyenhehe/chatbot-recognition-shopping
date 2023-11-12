import base64
import io
import json
import sys
from enum import Enum
from typing import List

from fastapi import status as sta
from PIL import Image as PILImage

from app.models.image import Image as ImageModel
from app.models.message import Message as MessageModel
from app.schemas.message import MessageInput, MessageOutput, MessageResponse
from app.services import AppCRUD, AppService
from app.services.chat import ChatCRUD
from app.services.image import ImageCRUD
from app.utils.repsonse.exceptions import ExceptionResponse
from app.utils.repsonse.result import ResultResponse
from extensions.minio.connector import MinioConnector, ObjectType


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
    def create(self, storage: MinioConnector, chat_user: str, message_obj: MessageInput, sender: str) -> ResultResponse:
        message_response = []
        exist_chat = ChatCRUD(self.db).get(username=sender, username2=chat_user)
        if not exist_chat:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "chat user": chat_user,
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
            message=message_obj.content,
            path_image=path_image,
            sender=sender,
            receiver=chat_user,
        )
        message_response.append(message_output.dict())
        message, status_code = MessageCRUD(self.db).create(exist_chat[0]["id"], sender, message_output)
        if status_code != sta.HTTP_200_OK:
            return ResultResponse(ExceptionResponse.ErrorServer(message))

        intent, entities = self.get_intent_entities_message(message_obj.content)
        if intent == IntentType.GREET:
            text = self.get_answer_message(
                username=sender,
                message=message_obj.content,
            )
            options = None
        elif intent == IntentType.ASK_TYPE:
            entities = {entity["entity"]: entity["value"] for entity in entities}

            colors = None
            if "color" in entities:
                colors = [entities["color"]]
            elif path_image:
                colors = self.get_color_image(path_image)

            if path_image:
                category_attribute = self.get_category_attribute_prediction(path_image)

            category = None
            if "cate" in entities:
                category = [entities["cate"]]
            elif path_image:
                category = category_attribute['cate']['top 5']

            attribute = None
            if "attr" in entities:
                attribute = [entities["attr"]]
            elif path_image:
                attribute = category_attribute['attr']['top 5']

            images = self.get_recommend_images(chat_user, path_image, colors, category, attribute)
            if len(images) > 0:
                text = "Sản phẩm nào làm bạn thích nhất?"
                options = images
            else:
                text = "Thật tiếc chúng tôi không có sản phẩm nào giống miêu tả của bạn"
                options = None
        else:
            text = """
                Shop không hiểu yêu cầu của bạn. Bạn có thể lặp lại yêu cầu của bạn theo cú pháp sau không? 
                "Tôi cần mua/quan tâm loại áo/quần/váy có màu/loại/kiểu như này không?"
            """
            options = None
        
        message_output = MessageOutput(
            message=text,
            path_image=None,
            sender=chat_user,
            receiver=sender,
            options=options,
        )
        message_response.append(message_output.dict())
        message, status_code = MessageCRUD(self.db).create(exist_chat[0]["id"], chat_user, message_output)

        return ResultResponse((message, status_code, message_response))

    def get(self, username: str, chat_user: str) -> ResultResponse:
        exist_chat = ChatCRUD(self.db).get(username=username, username2=chat_user)
        if not exist_chat:
            return ResultResponse(ExceptionResponse.NoExistedError({
                "chat user": chat_user,
            }))
        messages = MessageCRUD(self.db).get(username=username, chat_user=chat_user)
        return ResultResponse((None, sta.HTTP_200_OK, messages))
    

    def get_intent_entities_message(self, message: str) -> str:
        url = "/rasa/v1/answer/intent"
        payload = {
            "message": message,
        }
        data, _ = self.call_api(url, payload, "post")
        intent = data["intent"]["name"]
        entities = data["entities"]
        return intent, entities
    

    def get_answer_message(self, username: str, message: str) -> str:
        url = "/rasa/v1/answer"
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
    
    
    def get_category_attribute_prediction(self, path_image: str):
        url = "/inference/v1/category-attribute-inference"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return data
    

    def get_color_image(self, path_image: str) -> List[str]:
        url = "/inference/v1/color-inference"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return data


    def get_recommend_images(self, chat_user, path_image, colors, category, attribute):
        url = "/meta/v1/inference"
        payload = {
            "username": chat_user,
            "path_image": path_image,
            "colors": colors,
            "category": category,
            "attribute": attribute,
        }
        data, _ = self.call_api(url, payload, "post")
        return data
    

class MessageCRUD(AppCRUD):
    def create(self, chat_id: int, sender: str, message: MessageOutput) -> MessageResponse:
        messages = []
        if len(message.message):
            messages.append(MessageModel(
                message=message.message, 
                chat_id=chat_id, 
                sender=sender,
                receiver=message.receiver,
                path_image=message.path_image,
                options=message.options,
                is_option_action=True if message.options else None,
            ))
        if len(messages) > 0:
            message, status_code = self.insert("Message", self.serialize_list(messages))
            return message, status_code
        else:
            return None, sta.HTTP_200_OK


    def get(self, username: str, chat_user: str) -> List[MessageResponse]:
        query = {
            "$or": [
                {"sender": chat_user, "receiver": username}, 
                {"receiver": chat_user, "sender": username}
            ],
            "is_active": True,
        }
        no_query = {
            "_id": False,
            "is_active": False,
        }
        messages = list(self.db.Message.find(query, no_query))
        return messages
