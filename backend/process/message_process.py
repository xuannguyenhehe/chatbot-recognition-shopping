# import imp
# import pymongo
from backend.config.constant import PATH_FILE_PATTERNS
from backend.utils.spell_corrector import correct_sent
from backend.process.utils_message.infer_tags import infer_tags
from backend.process.utils_message.reset_state import check_reset_state
from backend.process.get_information import get_product_name_from_message
from backend.process.PretrainedModel import PretrainedModel
from backend.utils.utils import is_list

models = PretrainedModel()

import random
import json
from datetime import datetime
from backend.process.product_handler import check_condition

###
def get_response_from_json(ints, intents_json):

    # tag = ints[0]["intent"]
    tag = ints
    list_of_intents = intents_json["intents"]
    result = ""
    for i in list_of_intents:
        if i["tag"] == tag:
            if i["responses"]:
                result = random.choice(i["responses"])
                break
            else:
                result = ""
    return result

def get_response(data):
    my_db = models.client['chatbot_quangminhtien']
    my_col = my_db['conversation']
    
    with open('./model/quangminhtien_intents.json', encoding='utf-8') as fh:
        intents = json.load(fh)
    # get time start
    time = datetime.now()
    time = time.strftime("%Y-%m-%d %H:%M:%S")

    print("-"*10,data['text'])
    if isinstance(data['text'],list):
        msg = data['text'][0].lower()
    else:
        msg = data['text'].lower()
    print("\t\t+++++++++ SPELLING MISTAKE +++++++++")
    print("RAW MESSAGE:", msg)
    msg = correct_sent(msg)
    print("CORRECTED MESSAGE:", msg)
    print("\t\t++++++++++++++++++++++++++++++++++++")
    sender_id = data['sender_id']
    print("Sender_ID", sender_id)

    
    # -----Get information from last message of a sender_id-----
    # -----If first message of a sender_id => insert-----
    query = {"sender_id": sender_id}
    conversation_info = my_col.find_one({"sender_id": sender_id}, {"_id": 0})
    print(f"Conversation_info: {conversation_info}")
    if not conversation_info:
        lst_entity = intents['list_entities']
        conversation_info = {
            "sender_id":sender_id,
            "information": lst_entity,
            "pre_tag":"greetings",
            "time": time
        }
        my_col.insert_one(conversation_info)
    else:
        lst_entity = conversation_info['information']

    if not "time" in conversation_info:            
        conversation_info["time"] = time
    
    print('++++++++++++++ RESET CONVERSATION +++++++++++++++')
    time_latest = conversation_info['time']
    pre_tag = conversation_info['pre_tag']

    flag_restart = check_reset_state(time, time_latest, pre_tag)
    if flag_restart["end"] or flag_restart["in_process"]:
        lst_entity = intents['list_entities']
    
    print('flag restart', flag_restart)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++')

    conversation_info, mention, oos_product, na_product = \
        get_product_name_from_message(msg, 
                                      flag_restart["multiproduct"], 
                                      intents, 
                                      lst_entity)
    # ----- Remove product name before classify -----
    print("\n++++++++++++ order detail in conversation_info ++++++++++++")
    print(f"Conversation_info updated: {conversation_info}")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    
    print("\n++++++++++++ product mention, oos_product, na_product ++++++++++++")
    print("mention:", mention)
    print("oos_product:", oos_product)
    print("na_product:", na_product)

    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    if mention:
        if is_list(mention):
            for product_ele in mention:
                msg = msg.replace(product_ele,'')
        else:
            msg = msg.replace(mention,'')

    # ints = predict_class(msg)
    tag = infer_tags(msg,PATH_FILE_PATTERNS)
    print('intent==========',tag)
    res = get_response_from_json(tag, intents)

    if tag == "other":
        tag_arg = pre_tag
    elif not res:
        tag_arg = tag
    else:
        tag_arg = None
    
    if tag_arg:
        res, tag, lst_entity, flag_restart["multiproduct"] = check_condition(
            tag_arg, tag, intents, msg, lst_entity, flag_restart["multiproduct"], 
            conversation_info, mention, oos_product, na_product)
   
    query = {"sender_id": sender_id}
    if any(flag_restart[i] for i in flag_restart.keys()):
        my_col.update_one(query, {'$rename': {
            'information':'old_information'
        }})

    my_col.update_one(query, {"$set": {
        "sender_id": sender_id,
        "information": lst_entity,
        "pre_tag": tag,
        "time_latest": time
    }})
    return res
