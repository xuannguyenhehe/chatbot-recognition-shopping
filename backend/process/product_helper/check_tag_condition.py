from backend.utils.utils import check_list_empty, is_dict, is_list

def check_tag_condition(tag_block, intent_json, conversation_info, check_action):    
    def _check_entity_in_action_list(entity):
        return 'actions_list' in intent_json \
                and entity in intent_json['actions_list']
    
    def _check_entity_in_action(entity, entity_condition):
        return check_action and entity in check_action.keys() \
            and entity_condition and check_action[entity] \
            or not entity_condition and not check_action[entity]
    
    def _check_entity_condition(entity, entity_condition):
        return all(v1 and \
                    conversation_info[entity][k1] or \
                    not v1 and \
                    not conversation_info[entity][k1] \
                    for (k1, v1) in entity_condition.items()
                )
    
    def _check_exist_entity_condition(entity, entity_condition):
        return entity_condition and conversation_info[entity]
    
    def _check_exist_entity_convesation(entity):
        return conversation_info[entity] and \
            check_list_empty(conversation_info[entity])
    
    def _check_not_exist_entity_condition(entity):
        return not entity_condition and not conversation_info[entity]
    
    for next_action, action_condition in tag_block['condition'].items():
        count = 0
        for entity, entity_condition in action_condition.items():
            # temporary key/value for future use
            if is_dict(entity_condition) \
                    and _check_entity_condition(entity, entity_condition):                    
                count += 1
            elif _check_entity_in_action_list(entity) \
                    and _check_entity_in_action(entity, entity_condition):
                count += 1
            elif is_list(conversation_info[entity]):
                if _check_exist_entity_condition(entity, entity_condition) \
                        and not check_list_empty(conversation_info[entity]):      
                    count += 1
                if not entity_condition and (not conversation_info[entity] \
                                             or _check_exist_entity_convesation(entity)):
                    count += 1
            elif _check_exist_entity_condition(entity, entity_condition) \
                    or _check_not_exist_entity_condition(entity):
                if entity_condition == 'none' \
                        and conversation_info[entity] != entity_condition:    
                    continue
                count+=1
        
        if count == len(action_condition):
            for index in range(len(intent_json['intents'])):
                if intent_json['intents'][index]['tag'] == next_action:
                    tag_block = intent_json['intents'][index]
                    break
            else:
                continue
            break
        
    return tag_block