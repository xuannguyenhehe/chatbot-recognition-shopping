import re
import collections

from backend.config.config import get_config
from backend.process.PretrainedModel import PretrainedModel
from backend.utils.utils import check_list_empty

config_app = get_config()
models = PretrainedModel()

from backend.config.regex import product_regex,phone_regex, size_regex
from backend.process.size_consulting.suggest_product import suggest_product
from backend.utils.common_address import api_address
from backend.utils.utils import cal_total_price
# from backend.process.size_consulting.get_height_weight import get_measure_from_message, get_size

def get_entity_from_message(message, current_tag, tag_message, conversation_info):
    # conversation_info, mention, oos_product = get_product_name_from_message(message, sender_id, flag_restart_multi, intents, lst_entity)
    phone_number, address = get_phone_address_from_message(message, current_tag, tag_message)
    if phone_number:
        conversation_info['phone_number'] = phone_number
    if address:
        conversation_info['address'] = address

    # entity_dict = get_measure_from_message(message,lst_entity['measure'])
    # print('hahahaha',entity_dict)
    # for ent in lst_entity['measure'].keys():
    #     if entity_dict[ent]:
    #         conversation_info['measure'][ent] = entity_dict[ent]
    # print('======================0',conversation_info)
    # if all(conversation_info['measure'][ent] for ent in conversation_info['measure']) and not conversation_info['consulting_size']: # conversation_info['height'] and conversation_info['weight']
    #     consulting_size = get_size(conversation_info['measure'])
    #     conversation_info['consulting_size'] = consulting_size

    # return conversation_info, mention, oos_product
    return conversation_info

def get_product_name_from_message(message, flag_restart_multi, intents, lst_entity):
    '''
        Get product name + size + amount by regex
        if have product, get detail of that product:
            - size available, price, material
        output: 
            - conversation_info: order information
            - mention: which product client mention in current message
            - oos_product: dict of product "NA": not available (all size are not available)
            or "OOS": out of stock (others size available)

    '''
    
    oos_product = {}
    entities_list = collections.defaultdict(list)

    my_db = models.client['chatbot_quangminhtien']
    my_col = my_db['products']
    document = my_col.find({}, {"_id":0})
    
    for item in document:
        entities_list['product_detail'].append(item)
    print(f"Conversation_info {lst_entity}")
    conversation_info = lst_entity.copy()
    # ----- Get product_name, size and amount -----
    result = re.findall(product_regex, message)
    print('\t\t+++++++++++++Get product info from message+++++++++++++++++')
    print(f"Result of group of products: {result}")
    print('\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    
    if result:
        # ----- Extract each product info from database -----
        for tup in result:
            for item in entities_list['product_detail']:
                if item['name'] == tup[3]:
                    # detail.append(item)
                    entities_list['price'].append(str(item['price']))
                    entities_list['material'].append(item['material'])
                    break

            entities_list['product_name'].append(tup[3])
            if not tup[1]:
                entities_list['amount'].append("1")
            else:
                entities_list['amount'].append(tup[1])

            for amount in entities_list['amount']:
                if amount == '':
                    amount = "1"
            if tup[5]:
                entities_list['size'].append(tup[5].upper())

        # ----- If only 1 product have size => set same size for other product -----
        if len(result) > len(entities_list['size']):
            entities_list['size'] = set_product_size(entities_list, conversation_info)
    flag_multi = False
    if entities_list['product_name'] and flag_restart_multi:
        for product in entities_list['product_name']:
            if product not in conversation_info['product_name']:
                conversation_info = intents['list_entities']
                flag_multi = True
                break

    if not flag_multi:
        flag_restart_multi = False
        
    if entities_list['product_name']:
        # ----- Update info of current order if client mention a product -----
        for i in range(len(entities_list['product_name'])):
            entities_list['mention'].append(entities_list['product_name'][i])
            conversation_info = update_conversation_info(conversation_info, 
                                                         entities_list, 
                                                         i)

    # ----- If message have only size -----
    # -----EX: Chatbot hỏi lấy size gì? => client nhắn "size S"-----
    get_size = re.findall(size_regex, message) if not result or \
        (result and not entities_list['size']) else None
        
    flag_oos, conversation_info = check_assign_size_conversation(conversation_info,
                                                                 get_size)
    if flag_oos:
        conversation_info, oos_product = process_out_of_size(conversation_info, 
                                                                get_size, 
                                                                oos_product, 
                                                                intents)
    
    # ----- If only 1 product have size => set same size for other product -----
    conversation_info['total'] = str(cal_total_price(conversation_info['price'], 
                                                     conversation_info['amount']))

    if 'size' in entities_list \
            and entities_list['size'] \
            and len(entities_list['product_name']) > len(entities_list['size']):     
        size_temp = []
        for i in range(len(entities_list['product_name'])):
            size_temp.append(entities_list['size'][0])
        conversation_info['size'] = size_temp
    # -----Check if product and size available in database-----
    if (conversation_info['size'] or entities_list['product_name']) and \
        conversation_info['product_name']:
            
        for i in range(len(conversation_info['product_name'])):
            check_size, _ = suggest_product(conversation_info['product_name'][i], 
                                            None, 
                                            conversation_info['amount'][i], 
                                            check_size=False)
            if 'detail' not in check_size or not check_size['detail']:
                entities_list['na_product'].append(conversation_info['product_name'][i])
            elif conversation_info['size'] \
                    and conversation_info['size'][i] not in conversation_info['size_list'][i]:
                product_name = conversation_info['product_name'][i]
                oos_product[product_name] = {}
                oos_product[product_name]["type_oos"] = "size"
                for k in intents["info_product"]:                    
                    if k in conversation_info and conversation_info[k]:                        
                        oos_product[product_name][k] = conversation_info[k][i]
                conversation_info['size'][i] = "" 
                
    return conversation_info, entities_list['mention'], oos_product, entities_list['na_product']

def get_phone_address_from_message(message, current_tag, tag_message):
    '''
        Get phone and address using regex
    '''
    phone = re.findall(phone_regex, message)
    if phone:
        phone = phone[0]
    else:
        phone = ''
    address = ''
    if tag_message == "other" or current_tag == "order":
        # address_inp = preparation(folder=config_app['create_chatbot_api']['general_chatbot']['address_prepare'])
        address_res = api_address(message, models.address_inp, output_amount=1)
        print('------------CHECK ADDRESS EVERYWHERE-----------')
        print(f"address exist or not in message:{message}")
        print("address result: ", address_res)
        address_res = address_res['items'][0]
        
        if 'address' in address_res:
            client_address = address_res['address']
            # client_address = tmp['address'] if int(float(tmp['score'])) > 19 else ''
            print(f"Address:{client_address}")
            client_city = address_res['cityName']
            client_district = address_res['districtName']
            client_ward = address_res['wardName']

            if client_address and client_city and client_ward and client_district:
                address = client_address

    return phone, address

def check_assign_size_conversation(conversation_info, get_size):
    if not get_size:
        return False, conversation_info

    flag_oos = True
    for i in range(len(conversation_info["product_name"])):
        if check_list_empty(conversation_info["size"]) \
                or not conversation_info['size'][i]:
            flag_oos = False
            conversation_info["size"][i] = get_size[0][1].upper()
    return flag_oos, conversation_info

def process_out_of_size(conversation_info, get_size, oos_product, intents):
    for product in conversation_info["oos_product"].keys():
        if conversation_info["oos_product"][product]["type_oos"]=="size" \
            and get_size[0][1].upper() not in conversation_info["oos_product"][product]["size_list"]:
                
            oos_product[product] = {}
            for key in intents["info_product"]:
                oos_product[product]["type_oos"] = "size"
                if key in conversation_info and conversation_info[key]:
                    oos_product[product][key] = conversation_info[key][product]
            continue 

        for key in intents["list_entities"].keys():
            if key == "size":
                conversation_info[key].append(get_size[0][1].upper())
                continue
            if key in intents["info_product"]:
                conversation_info[key].append(conversation_info["oos_product"][product][key])
    
    return conversation_info, oos_product
            
def set_product_size(entities_list, conversation_info):
    size_temp = []
    if entities_list['size']:
        for _ in range(len(entities_list['product_name'])):
            size_temp.append(entities_list['size'][0])
        entities_list['size'] = size_temp
    elif 'size' in conversation_info and conversation_info['size']:
        for _ in range(len(entities_list['product_name'])):
            size_temp.append(conversation_info['size'][0])
        entities_list['size'] = size_temp
    else:
        size_temp = entities_list['size']
        
    return size_temp

def update_conversation_info(conversation_info, entities_list, product_idx):
    if 'product_ask' in conversation_info \
            and entities_list['product_name'][product_idx] not in conversation_info['product_ask']:
        conversation_info['product_ask'].append(entities_list['product_name'][product_idx])
        
    # if entities_list['product_name'][product_idx] not in conversation_info['product_name']:
    conversation_info['product_name'].append(entities_list['product_name'][product_idx])
    conversation_info['amount'].append(entities_list['amount'][product_idx])
    conversation_info['price'].append(entities_list['price'][product_idx])
    _, size_list = suggest_product(entities_list['product_name'][product_idx], 
                                        None, 
                                        entities_list['amount'][product_idx], 
                                        check_size=False)
    conversation_info['size_list'].append(size_list)
    conversation_info['material'].append(entities_list['material'][product_idx])

    if entities_list['size']:
        conversation_info['size'].append(entities_list['size'][product_idx])
    else:
        conversation_info['size'].append("")
            
    return conversation_info