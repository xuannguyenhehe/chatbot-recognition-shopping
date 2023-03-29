import torch
import json
import numpy as np

from sentence_transformers.util import cos_sim

from backend.process.PretrainedModel import PretrainedModel
from backend.config.constant import *
from backend.utils.dcnn_handler import predict_dcnn
from backend.process.utils_message.generate_mapping_table import generate_mapping_table

models = PretrainedModel()

def get_tag(sentence, model, dcnn_pred, intents, mapping_table):
    """Get tag of sentence given pattern model, dcnn predict result, intents list and mapping table

    Args:
        sentence (String): Input sentence
        model (SentenceTransformer): Pattern similarity model
        dcnn_pred (String): Predict result from dcnn model
        intents (List(Dict)): List of intents
        mapping_table (Dict): Mapping table from json file to dcnn model

    Returns:
        String: Predicted tag
    """
    tags = [intent['tag'] for intent in intents]
    try:
        map_tags = mapping_table[dcnn_pred]
        idx_lst = [tags.index(tag) for tag in map_tags]
    except:
        return "other"
    input_embedding = model.encode(sentence, show_progress_bar=False)
    tag_lst = []
    score_lst = []

    for idx in idx_lst:
        intent = intents[idx]
        patterns = intent['patterns']
        pattern_embeddings = model.encode(patterns, show_progress_bar=False)
        score = torch.mean(cos_sim(input_embedding, pattern_embeddings)).item()
        tag_lst.append(intent['tag'])
        score_lst.append(score)

    score_lst = np.array(score_lst)
    best_score = np.where(score_lst > 0.4, score_lst, 0) 
    # if not best_score:
    #     return "other"  
    tag_idx = np.argmax(best_score)
    print("BEST_SCORE", best_score)
    print("TAG_LIST", tag_lst)
    if best_score[tag_idx]==0:
        return "other"
    return tag_lst[tag_idx]

def infer_tags(sentence, json_file):
    """Inferring tags of input sentence based on given pattern file

    Args:
        sentence (String): Input sentence
        json_file (String): Path to pattern json file

    Returns:
        String: Predicted tag
    """
    print("JSON_FILE",json_file)
    with open(json_file, 'r', encoding='utf8') as intents_file:
        intents = json.load(intents_file)['intents']
    
    shop_name = json_file.split('/')[1].split('_')[0]
    mapping_filename = MAPPING_TABLE + shop_name + '.json'
    model_checkpoint = STATE_DICT +  shop_name + '.pt'
    
    try:
        with open(mapping_filename, 'r') as mapping_file:
            mapping_table = json.load(mapping_file)
    except:
        mapping_table = generate_mapping_table(json_file, mapping_filename)
    
    # load pattern similarity model weights
    # pattern_model.load_state_dict(torch.load(model_checkpoint))
    models.pattern_model.load_state_dict(
        torch.load(model_checkpoint, map_location=torch.device('cpu')))

    dcnn_pred = predict_dcnn(sentence)[0].lower()
    print("Dcnn_pred", dcnn_pred)
    if dcnn_pred == "inform_customer_info":
        return "other"
    return get_tag(sentence, models.pattern_model, dcnn_pred, intents, mapping_table)