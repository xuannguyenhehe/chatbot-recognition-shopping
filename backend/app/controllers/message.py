from fastapi import APIRouter, Depends
from typing import List
from app.models import get_database
from app.schemas.message import MessageResponse, CreatedMessages
from app.utils.repsonse.result import handle_result
from app.services.message import MessageService
from extensions.minio import get_storage


router = APIRouter(prefix="/message")


@router.get("/", response_model = List[MessageResponse])
async def get(chat_id: int, username: str, db: get_database = Depends()):
    response = MessageService(db).get(chat_id, username)
    return handle_result(response)


@router.post("/", response_model = MessageResponse)
async def create(
    message: CreatedMessages, 
    db: get_database = Depends(),
    storage: get_storage = Depends(),
):
    response = MessageService(db).create(
        storage,
        message.chat_id, 
        message.username, 
        message.message,
    )
    return handle_result(response)


# from rasa.core.agent import Agent
# import asyncio

# rasa = Agent.load("models/20230404-140115-flat-caliper.tar.gz")
# async def read_text(query):
#     message = await rasa.handle_message(query);return message;

# asyncio.run(read_text("hi"))
# {'text': 'hi', 'intent': {'name': 'greet', 'confidence': 0.9999938011169434}, 'entities': [], 'text_tokens': [(0, 2)], 'intent_ranking': [{'name': 'greet', 'confidence': 0.9999938011169434}, {'name': 'mood_great', 'confidence': 1.7477777873864397e-06}, {'name': 'deny', 'confidence': 8.835144171825959e-07}, {'name': 'bot_challenge', 'confidence': 8.495783276885049e-07}, {'name': 'ask_no_exist_type', 'confidence': 7.311575700441608e-07}, {'name': 'affirm', 'confidence': 7.234737040562322e-07}, {'name': 'mood_unhappy', 'confidence': 6.817094799771439e-07}, {'name': 'ask_exist_type', 'confidence': 3.0835226993986e-07}, {'name': 'goodbye', 'confidence': 2.737083377724048e-07}], 'response_selector': {'all_retrieval_intents': [], 'default': {'response': {'responses': None, 'confidence': 0.0, 'intent_response_key': None, 'utter_action': 'utter_None'}, 'ranking': []}}}

# from rasa.core.channels  import UserMessage
# u = UserMessage(sender_id="a", text='hi')
# asyncio.run(read_text(u))
# [{'recipient_id': 'a', 'text': 'Chào bạn! Shop có thể giúp gì cho bạn?'}]