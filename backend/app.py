from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from uvicorn import Config, Server
import logging
import asyncio

from backend.config.config import get_config
from backend.process.PretrainedModel import PretrainedModel
config_app = get_config()
logging.basicConfig(filename=config_app['log']['app'],
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
models = PretrainedModel(config_app['models_chatbot'])

from backend.api.api_message import send_message
from backend.api.api_image import send_image
from backend.model.pattern_similarity.train_model import train_pattern_model
from backend.config.constant import PATH_FILE_PATTERNS

app = FastAPI()

@app.post("/api/send_message")
async def chatbot_response(request: Request):    
    json_param = await request.form()
    json_param = jsonable_encoder(json_param)
    output = send_message(json_param)
    return output

@app.post("/api/send_image")
async def image_process(request: Request):
    json_param = await request.form()
    json_param = jsonable_encoder(json_param)
    output = send_image(json_param)
    return output

@app.post("/api/train_model_pattern")
async def train_model_pattern():
    _ = train_pattern_model(PATH_FILE_PATTERNS)
    return "SUCCESSFUL TRAIN MODEL "

 
