import json
import torch
from collections import Counter

from backend.process.PretrainedModel import PretrainedModel
from backend.config.constant import *
from backend.utils.dcnn_handler import predict_dcnn

models = PretrainedModel()

def generate_mapping_table(json_file, output_file):
    """Generate mapping table between 16 intents model and pattern similarity model

    Args:
        json_filepath (String): Json file path
        output_filepath (String): Output file path
    """
    with open(json_file, 'r', encoding='utf8') as f:
        intents = json.load(f)['intents']

    mapping_table = {}

    for intent in intents:
        if not intent['patterns']: continue
        patterns = intent['patterns']

        # get all result from dcnn model
        dcnn_results = []
        for pattern in patterns:
            tmp = predict_dcnn(pattern)[0].lower() 
            if tmp != "inform_customer_info":
                dcnn_results.append(tmp)
        # dcnn_results = [predict_dcnn(pattern)[0].lower() for pattern in patterns]
        counter = Counter(dcnn_results)

        # key of pattern will be dcnn most frequent intent
        label = max(dcnn_results, key=counter.get)
        if label not in mapping_table:
            mapping_table[label] = [intent['tag']]
        else:
            mapping_table[label] = mapping_table[label] + [intent['tag']]
    
    with open(output_file, 'w') as map_file:
        json.dump(mapping_table, map_file)
    
    return mapping_table