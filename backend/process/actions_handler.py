import re
from backend.config.regex import agree, disagree

def get_action(msg, block):
    '''
        All pre-define actions of chatbot
        action is a process that chatbot will do in a specific tag
    '''
    print("\t\t++++++++++++++CHECK ACTION+++++++++++++++++")
    check_action = {}
    if 'actions' in block and block['actions']:
        for action in block['actions']:
            check_regex = ''
            if action == "check_agree":
                check_regex = re.search(agree, msg)
            elif action == "check_disagree":
                check_regex = re.search(disagree, msg)

            if check_regex:
                check_action[action] = 1
            else:
                check_action[action] = 0
    print(check_action)
    print("\t\t+++++++++++++++++++++++++++++++++++++++++++")
    return check_action