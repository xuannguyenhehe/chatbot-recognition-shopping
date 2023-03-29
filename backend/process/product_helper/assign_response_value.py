def assign_response_value(conversation_info, res, check_loop=False, product_idx=None, sentence=None):
    # change name here
    for key, value in conversation_info.items():
        if isinstance(value, dict):
            continue
        if not check_loop:
            temp_res = res
            entity_string = value if isinstance(value, str) else (value[0] if value else '')
            res = res.replace("{"+key+"}", entity_string)
            if res == temp_res and key in res:
                entity_string = ", ".join(list(set(value)))
                res = res.replace("{" + key + "_list}", entity_string)                
        else:
            res = res.replace('(loop)', '')
            if sentence and key in sentence:
                # if key == "product_name":
                    # entity_string = conversation_info["product_name"][0]
                    # for product in conversation_info["product_name"][1:]:
                        # entity_string += ", "+product
                # else:
                entity_string = value if isinstance(value, str) else (value[product_idx] if value else '')
                res = res.replace("{"+key+"}", entity_string)
            elif key in res:
                res = res.replace("{"+key+"}", value[product_idx])
    return res