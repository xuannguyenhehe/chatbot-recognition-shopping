import json
import pickle
from backend.process.message_process import get_response
from backend.utils.error_handler import error_handler
def send_message(data):
    # ---------------- 4.BOT ---------------- #
    print("\t\t+++++++++++++++ Start API send-message +++++++++++++++\n\n")

    ls_param = ['sender_id', 'recipient_id', 'mid', 'text', 'name']
    print("\t\t+++++++++++++++ Check and add missing params of request +++++++++++++++")
    for ele in ls_param:
        if ele not in data or not data[ele]:
            # THROW ERROR because of not enough param
            return {
                'suggest_reply': 'ERROR NOT ENOUGH PARAM', 
                'id_job': '', 
                'check_end': True
            }

    # Add values to each of params - Dictionary
    input_data = {ele: data[ele] for ele in ls_param}
    data = input_data

    print("\t\t+++++++++++ 3.BOT +++++++++++")
    chatbot = '5'
    if chatbot == '':
        return {
            'suggest_reply': 'Please create the bot first ',
            'id_job': '',
            'check_end': True
        }
    try:
        response = get_response(data)
    except Exception as e:
        print("IndexError")
        error_type = error_handler(e)
        error_message = f"Hệ thống đang gặp lỗi ({error_type})"
        return {
            'rep_intent': '',
            'suggest_reply': error_message,
            'id_job': 456363,
            'check_end':False
        }

    result = {
        'rep_intent': '',
        'suggest_reply': response,
        'id_job': 456363,
        'check_end':False
    }
    # models.producer.send(config_app['kafka']['topic'], json.dumps(result).encode('utf-8'))

    print("\t\t++++++++++++++++++++++++++++++\n\n")
    # ------------------------------------------- #
    print("data", data)
    print('result',result)
    return result
