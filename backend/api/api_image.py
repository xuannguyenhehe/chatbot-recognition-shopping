import base64
import io
import json
import pickle
from urllib import response
from backend.config.constant import (DICT_FULLNAME, LS_PRODUCT)
import numpy as np
import tensorflow
from PIL import Image
import cv2
from backend.utils.utils import dictionary
from backend.utils.utils import extract_features

from backend.process.message_process import get_response
from backend.utils import image_handler

def send_image(data):
    print("\t\t+++++++++++++++ Start API send-image +++++++++++++++\n\n")
    ls_param = ['sender_id', 'recipient_id', 'mid', 'image[]', 'name']

    print("\t\t+++++++++++++++ Check and add missing params of request +++++++++++++++")
    for ele in ls_param:
        if ele not in data or not data[ele]:
            return {'suggest_reply': 'ERROR NOT ENOUGH PARAM', 'id_job': '', 'check_end': True}
        
    input_data = {
        ele: data[ele]
        for ele in ls_param
    }
    input_data['text'] = data['text'] if 'text' in data and data['text'] else ''
    data = input_data

    print("\t\t+++++++++++ 3.BOT +++++++++++")
    print("\t\t+++++++++++++++ 1.Read Mongo databases and convert image to base64 +++++++++++++++")

    list_msg = data['image[]'].split(",")
    # print("999", list_msg))
    # list_msg = data['image[]'][0]
    # list_msg = list_msg.split(",")
    list_image = []
    # print("0"*10, list_msg)
    print("1"*10, len(list_msg))
    for msg in list_msg:
        im_bytes = base64.b64decode(msg)
        im_arr = np.frombuffer(im_bytes, dtype=np.uint8)  
        img = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
        # Reduce four to three channel (if png image)
        img = img[:,:,0:3]
        list_image.append(img)
    print("\t\t++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    # -------------------- 3. Use the Model to predict product_ID -------------------- #
    print("\t\t+++++++++++++++ 3. Use the Model to predict product_ID +++++++++++++++")

    result = detect_image(list_image, data)
    return result

def detect_image(list_image, data):
    list_image_1 = []
    np.set_printoptions(suppress=True)
    # Load the model
    if tensorflow.test.gpu_device_name():
        print('GPU found')
    else:
        print("No GPU found")
    
    list_product_ID = []
    confident_image = 1
    for image in list_image:
        image = np.array(image)
        product_ID_predict, confident_image = image_handler.predict(image,0.9)
        print('**********************',product_ID_predict, confident_image,'**********************')
        if product_ID_predict!='Out of stock': 
            product_ID = DICT_FULLNAME[product_ID_predict]
            list_product_ID.append(product_ID)
    list_product_ID = list(set(list_product_ID))
    print('++++++')
    print(f"confident_image:{confident_image}")
    print(f"list_product_ID:{list_product_ID}")
    print("\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    # ---------------------------------------------------------------------------- #

    # -------------------- 4.Suggestion Reply -------------------- #
    print("\t\t+++++++++++++++ 4.Suggestion Reply +++++++++++++++")
    result = {}
    suggest_reply, body_send_message = "", {}
    # if not product_ID:
    
    if not list_product_ID:
        result["dont_have_product"] = None
        suggest_reply = "Cảm ơn chị đã quan tâm đến shop, chị cho shop hỏi chị cần tư vấn sản phẩm nào ạ"
        body_send_message= suggest_reply
    else:
        list_product_name = []
        for product_ID in list_product_ID:
            product_name = LS_PRODUCT[product_ID]
            list_product_name.append(product_name)

        print('------------- IMAGE TO TEXT --------------')
        print(list_product_name)
        print('------------------------------------------')
        if 'text' in data and len(data['text']) > 0 and data['text'][0]:
            final_str = ''
            for product_name in list_product_name:
                final_str += product_name + r" "
            final_str += data['text'][0]
        else:
            final_str = ''
            for product_name in list_product_name:
                final_str += product_name + r" "
            # final_str += ' còn không ? _image'
            final_str += 'giá bao nhiêu'
        my_obj = {'sender_id': data['sender_id'], 'recipient_id': data['recipient_id'],
                'mid': data['mid'], 'text': [final_str]}
        body_send_message = get_response(my_obj)
        
    print("\t\t+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n\n")
    if data['name'][0] not in dictionary:
        dictionary[data['name'][0]] = {}
    if data['sender_id'][0] not in dictionary[data['name'][0]]:
        dictionary[data['name'][0]][data['sender_id'][0]] = len(dictionary[data['name'][0]]) + 1
    message_id = []
    message_id.append(data['mid'][0])
    result = {'suggest_reply': body_send_message,
              'id_job': dictionary[data['name'][0]][data['sender_id'][0]], 
              'check_end': False, 
              'recipient_id': data['sender_id'][0], 
              'sender_id': data['recipient_id'][0], 
              'message_ids': message_id
    }
    
    return result
