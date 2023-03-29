# from threading import Condition
import random
import collections

# from backend.config.regex import agree, disagree
from backend.process.get_information import get_entity_from_message
from backend.process.size_consulting.get_height_weight import get_measure_from_message, get_size
from backend.process.actions_handler import get_action
from backend.utils.utils import cal_total_price

from backend.process.product_helper.assign_response_value import assign_response_value
from backend.process.product_helper.check_tag_condition import check_tag_condition
from backend.process.product_helper.process_mention_products import process_mention_products

def check_condition(current_tag, tag_message, intent_json, msg, lst_entity, 
                    flag_restart_multi, conversation_info, mention, oos_product, 
                    na_product):
    conversation_info = get_entity_from_message(msg, 
                                                current_tag, 
                                                tag_message, 
                                                conversation_info)
    if 'config' in intent_json.keys() \
            and 'size_consulting' in intent_json['config'] \
            and intent_json['config']['size_consulting']:            
        entity_dict = get_measure_from_message(msg, lst_entity['measure'])
        for ent in lst_entity['measure'].keys():
            if entity_dict[ent]:
                conversation_info['measure'][ent] = entity_dict[ent]
        
        if all(conversation_info['measure'][ent] for ent in conversation_info['measure']) \
                and not conversation_info['consulting_size']: # conversation_info['height'] and conversation_info['weight']                
            consulting_size = get_size(conversation_info['measure'])
            conversation_info['consulting_size'] = consulting_size
            # Todo: add size of all product when have consulting_size and check database for available
            if consulting_size and consulting_size != "none":
                # for i in range(len(conversation_info['product_name'])):
                conversation_info['size'] = [consulting_size for _ in range(len(conversation_info['product_name']))]
                # for i in range(len(conversation_info['product_name'])):
                #     if conversation_info["size_list"][i] and conversation_info['size'][i] not in conversation_info["size_list"][i]:
                #         oos_product[conversation_info['product_name'][i]] = "OOS"

    temp_info = conversation_info.copy()
    res_oos = ''
    # -----Case ask multiproduct but only order 1 => process only with mention product-----
    if mention:
        conversation_info = process_mention_products(conversation_info, 
                                                     oos_product, 
                                                     na_product, 
                                                     mention)

    # -----Remove product not available or out of stock-----
    res_oos = ""
    res_na = ""
    if oos_product:
        for key_product in oos_product.keys():
            # -----generate reply for each product not available or out of stock-----
            res_oos += "Dạ tiếc quá, sản phẩm {product_name} hết size {size} rồi ạ. "\
                    "Sản phẩm chỉ còn size {size_list} thôi ạ*"\
                    .format(product_name=key_product, 
                            size=oos_product[key_product]["size"], 
                            size_list=oos_product[key_product]['size_list'])
    if na_product:

        # -----generate reply for each product not available or out of stock-----
        # res_oos = res_oos_temp
        for key_product in na_product:
            index_product = temp_info["product_name"].index(key_product)
            res_na += f"Dạ tiếc quá, sản phẩm {key_product} hết hàng mất rồi ạ*"
            
            del temp_info['amount'][index_product]
            del temp_info['price'][index_product]
            del temp_info['size_list'][index_product]
            del temp_info['product_name'][index_product]
            del temp_info['material'][index_product]            
            if temp_info['size']:
                del temp_info['size'][index_product]
    
        temp_info['total'] = str(cal_total_price(temp_info['price'], temp_info['amount']))

    # -----Begin check condition from current tag-----
    for intent in intent_json['intents']:
        if intent['tag'] == current_tag:
            tag_block = intent
    flag = True         # set flag to make sure it go in while loop for the first time
    
    while not tag_block['responses'] or flag:
        flag = False
        # -----Check if any actions in this tag-----
        check_action = get_action(msg, tag_block)
        # -----Check conditions in block and get the tag if all conditions match-----
        if 'condition' in tag_block and tag_block['condition']:
            tag_block = check_tag_condition(tag_block, 
                                            intent_json, 
                                            conversation_info, 
                                            check_action)

    # -----Get response from block and process before reply-----
    res = random.choice(tag_block['responses'])
    # -----If res is list => concat all message together-----
    if isinstance(res, list):
        new_res = ""
        for sentence in res:
            # -----loop a part of message have (loop) to reply multi product-----
            if "(loop)" not in sentence:                                
                new_res += assign_response_value(conversation_info, sentence)
            else:
                for product_idx in range(len(conversation_info['product_name'])):
                    res_temp = assign_response_value(conversation_info, 
                                           sentence, 
                                           check_loop=True, 
                                           product_idx=product_idx, 
                                           sentence=sentence)
                    if res_temp not in new_res:
                        new_res += "*"+res_temp
    # -----If response is a string-----
    elif "(loop)" not in res:
        # -----loop a part of message have (loop) to reply multi product-----
        new_res = assign_response_value(conversation_info, res)
    else:
        new_res = ""
        for product_idx in range(len(conversation_info['product_name'])):
            res_temp = assign_response_value(conversation_info, res, check_loop=True, product_idx=product_idx)
            new_res += res_temp + "*" 

    if not res_oos and not res_na:
        new_res = new_res.strip("*")
    elif len(conversation_info['product_name']) == 0:
        new_res = res_na + res_oos
    else:
        new_res = res_na + res_oos + new_res

    while new_res[0] == "*":
        new_res = new_res[1:]
        
    while new_res[-1] == "*":
        new_res = new_res[:-1] 

    new_res = new_res.replace("**","*")

    # -----If customer mention a product when order => order that product only-----
    # -----EX: hỏi đầm caro và set xanh => chốt set xanh thôi-----
    if not(mention and current_tag=='order'):
        conversation_info = temp_info.copy()
    
    print("\n++++++++++++ final order detail ++++++++++++")
    print(conversation_info)
    print("++++++++++++++++++++++++++++++++++++++++++++++")

    # -----if have deal in tag => update "confirmed" into DB (to check when changing product)-----
    if tag_block['tag'] == "deal":
        conversation_info["deal"] = "confirmed"
        
    for _, value in oos_product.items():
        value[value["type_oos"]] = ""

    conversation_info.update({
        "oos_product": oos_product,
        "na_product": na_product
    })
    
    return new_res.strip("*"), tag_block['tag'], conversation_info, flag_restart_multi