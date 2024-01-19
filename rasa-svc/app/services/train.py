import json

import requests
from fastapi import status

from app.schemas.train import TrainIntents, TrainIntent
from app.utils.repsonse.result import ResultResponse
from rasa.core.agent import Agent
from rasa.core.channels import UserMessage
from extensions.minio.connector import MinioConnector
from rasa.model_training import train
import yaml
from rasa.shared.nlu.training_data.formats.rasa_yaml import RasaYAMLReader, RasaYAMLWriter
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.training_data.message import Message
import os

class TrainService():
    def __init__ (self, config, storage: MinioConnector):

        self.rasa_cfg = config['RASA_CFG']
        self.domain_cfg = config['DOMAIN_CFG']

        with open(config['NLU_CFG'], 'r') as file:
            self.nlu_cfg = yaml.safe_load(file)
        self.synonym_cfg = config['SYNONYM_CFG']

        with open(config['RESPONSES_CFG'], 'r') as file:
            self.responses_cfg = yaml.safe_load(file)
        
        with open(config['RULES_CFG'], 'r') as file:
            self.rules_cfg = yaml.safe_load(file)
        
        self.stories_cfg = config['STORIES_CFG']

        for index in range(len(self.nlu_cfg['nlu'])):
            self.nlu_cfg['nlu'][index]['examples'] = self.nlu_cfg['nlu'][index]['examples'].split('\n- ')
            if '/n' in self.nlu_cfg['nlu'][index]['examples'][-1]:
                self.nlu_cfg['nlu'][index]['examples'][-1] = self.nlu_cfg['nlu'][index]['examples'][-1].replace('\n', '')
            self.nlu_cfg['nlu'][index]['examples'] = [{'text' : example} for example in self.nlu_cfg['nlu'][index]['examples']]

        self.storage = storage

    async def train(self, username: str, input: TrainIntents) -> ResultResponse:
        nlu_cfg = self.nlu_cfg
        for intent in input.intents:
            nlu_cfg['nlu'].append({
                'intent': intent.keyword,
                'examples': [{'text': question } for question in intent.questions],
            })

        responses_cfg = self.responses_cfg
        for intent in input.intents:
            responses_cfg['responses'][f"utter_{intent.keyword}"] = [
                {'text': intent.answer}
            ]
        
        rules_cfg = self.rules_cfg
        for intent in input.intents:
            rules_cfg['rules'].append({
                'rule': intent.keyword,
                'steps': [
                    {'intent': intent.keyword},
                    {'action': f"utter_{intent.keyword}"}
                ]
            })

        if not os.path.exists(f'tmp/{username}'):
            os.makedirs(f'tmp/{username}')
        
        RasaYAMLWriter().dump(f'./tmp/{username}/nlu.yml', RasaYAMLReader().reads(string=yaml.dump(nlu_cfg)))
        with open(f'./tmp/{username}/responses.yml', 'w') as file:
            yaml.dump(responses_cfg, file)
        with open(f'./tmp/{username}/rules.yml', 'w') as file:
            yaml.dump(rules_cfg, file)
        
        train(
            domain=self.domain_cfg,
            config=self.rasa_cfg,
            training_files=[
                self.synonym_cfg,
                f'./tmp/{username}/nlu.yml',
                f'./tmp/{username}/responses.yml',
                f'./tmp/{username}/rules.yml'
            ],
            fixed_model_name=username,
            output=f'./tmp/{username}'
        )
        return ResultResponse((None, status.HTTP_200_OK, f'Train {username} chatbot successful'))
