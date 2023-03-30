import pymongo, re
import numpy as np
from unidecode import unidecode
from backend.process.size_consulting.regex import pt_height, pt_weight, pt_weight_6, pt_weight_7, regex_lst
client = pymongo.MongoClient("mongodb://admin:admin@chatbot-mongo-1:27017/admin")

def get_measure_from_message(message,measure):
    measure_dict = {
        key: ''
        for key in measure.keys()
    }
    height=''
    weight=''
    for key in measure_dict.keys():
        if key == 'height':
            height = normalize_height(message)
            measure_dict['height'] =  height
        elif key == 'weight':
            weight = normalize_weight(message)
            measure_dict['weight'] =  weight
        else:
            ent = re.findall(regex_lst[key], message)
            measure_dict[key] = ent[0] if ent else ''
    if height and weight:
        height, weight = normalize_height_weight(message, int(height), int(weight))
        measure_dict['height'] =  height
        measure_dict['weight'] =  weight
    
    print(f"Height: {height}")
    print(f"Weight: {weight}")
    return measure_dict
    # return height, weight

def preprocess_sentence(text):
    text = text.lower()
    text = re.sub(r'khách\s\d+:', '', text)
    text = unidecode(text)
    text = re.sub(r'\'', '', text)
    text = re.sub(r'[^\w\d\.,]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'^\s+|\s+$', '', text)
    return text

def recognizer(sentence, pattern):
    sent = preprocess_sentence(sentence)
    match_lst = []
    k = 0
    while True:
        p = re.search(pattern, sent)
        if p is None: break
        idx = p.span()
        # print(p)
        match_lst += [sent[idx[0]:idx[1]]]
        k = k + idx[1]
        sent = sent[k:]
    return match_lst

def preprocess(word):
    ### đổi rưỡi + một sang số để normalize
    word = re.sub(r'ruoi', '50', word)
    word = re.sub(r'mot', '1', word)
    word = re.sub(r'\D', ' ', word)
    word = re.sub(r'\s+', ' ', word)
    word = re.sub(r'^\s|\s$', '', word)
    return word

def normalize_height(sent, check_height=False):
    match_lst = []    
    if check_height:
        match_lst = recognizer(sent, r'\b\d\d\d\b')
    if not match_lst:
        match_lst = recognizer(sent, pt_height)
    if match_lst:
        match_lst = [preprocess(match) for match in match_lst]
        match_lst = [match.split(' ')[-1] for match in match_lst]
        match_lst = [int(match) for match in match_lst]
        match_lst = [100+m*10 if m<9 else m for m in match_lst]
        match_lst = [100+m if m<99 else m for m in match_lst]
        
        if len(match_lst) == 1:
            return str(match_lst[0])
        else:
            return str(np.max(match_lst))
    else:
        return ''

def normalize_weight(sent, check_weight=False):
    match_lst = recognizer(sent, pt_weight)    
    # case: Cao 1m 60 45, chỉ thực hiện khi catch đc height nhưng không catch đc weight
    if not match_lst and recognizer(sent, pt_height):
        ### sử dụng regex cho riêng case này: pt_weight_6
        match_lst = recognizer(sent, pt_weight_6)        
        for match_h in recognizer(sent, pt_height):
            match_lst = [re.sub(match_h+' ', '', match_w) for match_w in match_lst]
        match_lst = [preprocess(match) for match in match_lst]
    elif not match_lst and check_weight:
        match_lst = recognizer(sent, r'\b\d\d\b')
    else:
        match_lst = [preprocess(match) for match in match_lst]    
    final = -1
    for match in match_lst:
        temp = match.split(' ')
        temp = [int(tmp) for tmp in temp]
        ### case 42.5 kg => 43kg
        ### đổi max(temp) thành temp[-1] vì case: Cao 1m 60 45kg sẽ catch 60 45kg => max sẽ lấy 60
        # temp = (temp[0]+1) if (len(temp)==2 and temp[1]==5) else int(temp[-1])
        temp = temp[0]+1 if (len(temp)==2 and len(str(temp[1]))==1) else int(temp[-1])
        final = temp if temp > final else final
    if final == - 1:
        return ''
    return str(final)

def normalize_height_weight(sent, height, weight):
    new_height = height
    new_weight = weight

    if not weight:
        if not height:
            # in case 155, 40
            number_lst = re.search(r'\b(\d\d\d\s*,\s*\d\d|\d\d\s*,\s*\d\d\d)\b', sent)
            if not number_lst:
                number_lst = re.search(r'\b(\d\d\d\s*\d\d|\d\d\s*\d\d\d)\b', sent)
            if number_lst:
                print(number_lst)
                number_lst = re.sub(',', ' ', number_lst.group())
                number_lst = preprocess_sentence(number_lst)
                number_lst = number_lst.split(' ')
                print(number_lst)
                for number in number_lst:
                    number = preprocess(number)
                    print(number)                
                    if len(number) == 3:
                        new_height = int(number)
                    else:
                        new_weight = int(number)
        else:
            match_lst = recognizer(sent, pt_weight_7)
            print(match_lst)
            for match_h in recognizer(sent, pt_height):
                match_lst = [re.sub(match_h+' ', '', match_w) for match_w in match_lst]
            match_lst = [preprocess(match) for match in match_lst]
            print(match_lst)
            final = -1
            for match in match_lst:
                temp = match.split(' ')
                temp = [int(tmp) for tmp in temp]
                temp = temp[0]+1 if (len(temp)==2 and len(str(temp[1]))==1) else int(temp[-1])
                final = temp if temp > final else final
            new_weight = final if final != -1 else ''    

    return str(new_height), str(new_weight)

def get_size(measure):
    for key in measure.keys():
        if measure[key]:
            measure[key] = int(measure[key])
        # if weight:
        #     weight = int(weight)
    # my_db = client['chatbot_quangminhtien']
    # my_col = my_db['size_consulting']
    # document = my_col.find({}, {"_id":0})
    # size = ''
    # weight_list = []
    # for item in document:
    #     print("lalalalala", item)
    #     for key, value in item.items():
    #         weight_list.append(value['weight']['min_weight'])
    #         weight_list.append(value['weight']['max_weight'])
    #         if measure['weight'] >= value['weight']['min_weight'] and measure['weight'] <= value['weight']['max_weight']: 
    #             size = key
    # if not size:
    #     if measure['weight'] > max(weight_list):
    #         size = "L"
    #     elif measure['weight'] < min(weight_list):
    #         size = "XS"
    # return size
    my_db = client['chatbot_quangminhtien']
    my_col = my_db['size_consulting']
    document = my_col.find({}, {"_id":0})
    size = ''
    weight_list = []
    for item in document:
        for key, value in item.items():
            if all(measure[attr] >= value[attr]['min'] and measure[attr] <= value[attr]['max'] for attr in measure.keys()): 
                size = key
    if not size:
        size = 'none'
    print(f"Size: {size}")
    return size