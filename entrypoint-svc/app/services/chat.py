from typing import List

import pymongo
from fastapi import status

from app.models.chat import Chat as ChatModel
from app.schemas.chat import Chat, NewChat
from app.services import AppCRUD, AppService
from app.utils.repsonse.exceptions import ExceptionResponse
from app.utils.repsonse.result import ResultResponse


class ChatService(AppService):
    def get(self, username: str, is_get_last_message: bool = True) -> ResultResponse:
        chats = ChatCRUD(self.db).get(username=username, is_get_last_message=is_get_last_message)
        return ResultResponse((None, status.HTTP_200_OK, chats))

    def create(self, chat: NewChat, sender: str) -> ResultResponse:
        exist_chat = ChatCRUD(self.db).get(
            username=sender, 
            username2=chat.username,
        )
        if exist_chat:
            return ResultResponse(ExceptionResponse.ExistedError({
                "chat": chat.username,
            }))
        message, status_code = ChatCRUD(self.db).create(chat, sender)
        return ResultResponse((message, status_code))


class ChatCRUD(AppCRUD):
    def create(self, chat: NewChat, sender: str) -> Chat:
        chat_id = self.db.Chat.count_documents({}) + 1
        chat = ChatModel(receiver=chat.username, sender=sender, id=chat_id)
        message, status_code = self.insert("Chat", self.serialize(chat))
        return message, status_code

    def get(
            self, 
            username: str = None, 
            username2: str = None, 
            name: str = None, 
            id: int = None, 
            is_get_last_message: bool = True,
        ) -> List[Chat]:
        query = {}
        if username:
            query.update({
                "$or": [{"sender": username}, {"receiver": username}],
                "is_active": True,
            })
        if username and username2:
            query.update({
                "$or": [
                    {"sender": username, "receiver": username2}, 
                    {"receiver": username, "sender": username2}, 
                ],
                "is_active": True,
            })
        if name: 
            query.update({
                "name": name,
            })
        if id: 
            query.update({
                "id": id,
            })
        no_query = {
            "_id": False,
            "is_active": False,
            "created_date": False,
            "updated_date": False,
        }
        chats = list(self.db.Chat.find(query, no_query))

        if is_get_last_message:
            for chat in chats:
                query = {
                    "chat_id": chat["id"],
                    "is_active": True,
                }
                no_query = {
                    "_id": False,
                    "is_active": False,
                }
                last_message = list(self.db.Message.find(query, no_query)\
                                            .sort('updated_date', pymongo.DESCENDING).limit(1))
                chat['last_message'] = last_message[0]["message"] if len(last_message) > 0 else None
                chat['last_message_user'] = last_message[0]["sender"] if len(last_message) > 0 else None
            
        return chats
    
    def update_current_entities(self, chat_id, username, current_entities: list = []):
        query_data = {
            "username": username,
            "id": chat_id,
        }
        update_data = {
            "current_entities": current_entities,
        }
        message, status_code = self.update("Chat", query_data, update_data)
        return message, status_code
