import collections

from backend.utils.utils import cal_total_price

def process_mention_products(conversation_info, oos_product, na_product, mention):
    temp_list = collections.defaultdict(list)

    for product_idx, product_name in enumerate(mention):
        # Check if product available in mention
        if mention == conversation_info['product_name']:
            indices = [product_idx]
        else:
            indices = [idx for idx, prod in enumerate(conversation_info['product_name']) \
                        if prod == product_name]
        for idx in indices:
            if product_name not in oos_product.keys() and product_name not in na_product:
                temp_list = assign_value(temp_list, conversation_info, idx)
            elif product_name in oos_product.keys() and conversation_info['size'][idx]:
                temp_list = assign_value(temp_list, conversation_info, idx)
            total = str(cal_total_price(temp_list['price'], temp_list['amount']))
        
    for key in ['product_name', 'amount', 'price', 'size_list', 'size']:
        conversation_info[key] = temp_list[key]
    conversation_info['total'] = total
    
    return conversation_info

def assign_value(temp_list, conversation_info, product_idx):
    temp_list['product_name'].append(conversation_info['product_name'][product_idx])
    temp_list['amount'].append(conversation_info['amount'][product_idx])
    temp_list['price'].append(conversation_info['price'][product_idx])
    temp_list['size_list'].append(conversation_info['size_list'][product_idx])
    if conversation_info['size']:
        temp_list['size'].append(conversation_info['size'][product_idx])
    return temp_list