import json
import pickle
import pymongo
import nltk
import re
nltk.download('punkt')

from os import path
from sentence_transformers import SentenceTransformer
from tensorflow.keras.models import load_model

from backend.config.config import get_config
# from backend.utils import image_handler
from backend.utils.prepare_address import preparation
config_app = get_config()

class PretrainedModel:
    _instance = None
    def __new__(cls, cfg=None, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(PretrainedModel, cls).__new__(cls, *args, **kwargs)

            print("aloha", cfg)
            # 2. Model load text
            # cls.tfidfconverter = pickle.load(open(cfg['model_load_text']['tfidf_model'], 'rb'))            
            cls.dcnn_model = load_model(cfg['model_load_text']['dcnn_model'])
            cls.tokenizer = pickle.load(open(cfg['model_load_text']['tokenizer'],'rb'))
            cls.classes = pickle.load(open(cfg['model_load_text']['classes'],'rb'))

            #3. Load monggodb
            cls.client = pymongo.MongoClient(config_app['mongodb']['link_db_server'])

            #4. Load model image
            # cls.model_resnet = ResNet50( weights="imagenet",include_top=False,input_shape=(224, 224, 3))
            # cls.image_model = image_handler
            # cls.filenames = pickle.load(open(cfg['model_load_image']['filenames'], 'rb'))
            # feature_list = pickle.load(open(cfg['model_load_image']['feature_list'], 'rb'))
            # cls.neighbors = NearestNeighbors(n_neighbors=10,algorithm='brute',metric='euclidean').fit(feature_list)

            #5 . Load model size
            # cls.model_size = pickle.load(open(config_app['create_chatbot_api']['hume_chatbot']['model_size_consult'], 'rb'))

            #6 . Load code product
            # json_product = open(path.join(config_app['data']['label_entity_data'], 'map_to_code_v1.json'), 'r')
            # cls.code_product = json.loads(json_product.read())

            #7. Address preparation
            cls.address_inp = preparation(folder=config_app['create_chatbot_api']['general_chatbot']['address_prepare'])
            
            #8. Spell Corection
            eng_file = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['eng_file'], 'r')
            cls.eng_dic = json.load(eng_file)

            short_word_file = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['short_word_file'], encoding='utf-8')
            cls.short_word_dic = json.load(short_word_file)

            teencode_re_file = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['teencode_regex'], encoding='utf-8')
            cls.teencode_re_dic = json.load(teencode_re_file)

            single_word_dic = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['single_word_dic'], 'r', encoding='utf-8')
            single_word_dic_line = single_word_dic.readlines()
            cls.single_word_dic = [re.sub('\n', '', s) for s in single_word_dic_line]

            vowel_file = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['vowel'], encoding='utf-8')
            cls.vowel_dic = json.load(vowel_file)

            fi = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['telex_fault'], encoding='utf-8')
            cls.complex_telex = json.load(fi)

            f2 = open(config_app['create_chatbot_api']['general_chatbot']['spell_corection']['tudien_don'], 'r', encoding='utf-8')
            cls.dictionary = json.load(f2)
            
            #9 Load model pattern similarity
            cls.pattern_model = SentenceTransformer(cfg['model_load_text']['pretrained_pattern_model'])

        return cls._instance
