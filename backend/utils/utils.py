import re
import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input
from numpy.linalg import norm
global dictionary
dictionary = {}


def split(delimiters, string, maxsplit=0):
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def preprocess_before_classify(ID_product, alias, message):
    if ID_product:
        if isinstance(ID_product,list):
            for product_ele in ID_product:
                message = message.replace(product_ele,'')
        else:
            message = message.replace(ID_product,'')
    if alias:
        if isinstance(alias,list):
            for alias_ele in alias:
                message = message.replace(alias_ele,'')
        else:
            message = message.replace(alias,'')
    return message

def split(delimiters, string, maxsplit=0):
    # regexPattern = '|'.join(map(re.escape, delimiters))
    regexPattern = '|'.join(delimiters)
    return re.split(regexPattern, string, maxsplit)

# Preprocessing message
def preprocess_message(message):
    message = re.sub(
        '[\:\_=\#\@\$\%\$\\(\)\~\@\;\'\|\<\>\]\[\"\–“”…*]', ' ', message)

    message = message.lower()
    message = message.replace(',', ' , ')
    message = message.replace('.', ' . ')
    message = message.replace('!', ' ! ')
    message = message.replace('&', ' & ')
    message = message.replace('?', ' ? ')
    message = message.replace('(', ' ( ')
    message = message.replace(')', ' ) ')
    message = message.replace('+', ' + ')
    message = compound2unicode(message)
    list_token = message.split(' ')
    # ---------------------- Chuẩn hóa một số từ sai chính tả đặc thù
    list_token = ['đầm' if ele in ['dầm'] else ele for ele in list_token]   
    while '' in list_token:
        list_token.remove('')
    message = ' '.join(list_token)
    return message

def text_cleaner(text, deep_clean=True):
    """Clean text for dcnn model

    Args:
        text (String): Input text
        deep_clean (bool, optional): Remove punctuations. Defaults to True.

    Returns:
        [String]: Clean text
    """
    rules = [
        {r'>\s+': u'>'},  # remove spaces after a tag opens or closes
        {r'\s+': u' '},  # replace consecutive spaces
        {r'\s*<br\s*/?>\s*': u'\n'},  # newline after a <br>
        {r'</(div)\s*>\s*': u'\n'},  # newline after </p> and </div> and <h1/>...
        {r'</(p|h\d)\s*>\s*': u'\n\n'},  # newline after </p> and </div> and <h1/>...
        {r'<head>.*<\s*(/head|body)[^>]*>': u''},  # remove <head> to </head>
        {r'<a\s+href="([^"]+)"[^>]*>.*</a>': r'\1'},  # show links instead of texts
        {r'[ \t]*<[^<]*?/?>': u''},  # remove remaining tags
        {r'^\s+': u''}  # remove spaces at the beginning

    ]

    if deep_clean:
        text = text.replace(".", "")
        text = text.replace("[", " ")
        text = text.replace(",", " ")
        text = text.replace("]", " ")
        text = text.replace("(", " ")
        text = text.replace(")", " ")
        text = text.replace("\"", "")
        text = text.replace("-", " ")
        text = text.replace("=", " ")
        text = text.replace("?", " ")
        text = text.replace("!", " ")

        for rule in rules:
            for (k, v) in rule.items():
                regex = re.compile(k)
                text = regex.sub(v, text)
            text = text.rstrip()
            text = text.strip()
        text = text.replace('+', ' ').replace('.', ' ').replace(',', ' ').replace(':', ' ')
        text = re.sub("(^|\W)\d+($|\W)", " ", text)
        
    else:
        for rule in rules:
            for (k, v) in rule.items():
                regex = re.compile(k)
                text = regex.sub(v, text)
            text = text.rstrip()
            text = text.strip()
    return text.lower()

def clean_tweet(tweet):
    # Removing the @
    _ = re.search(r'Khách\s*\d*:',tweet)
    if _:
      tweet = tweet[_.span()[1]:]
    tweet = re.sub(r"@[A-Za-z0-9]+", ' ', tweet)
    # Removing the URL links
    tweet = re.sub(r"https?://[A-Za-z0-9./]+", ' ', tweet)
    # Keeping only letters
    # tweet = re.sub(r"[^a-zA-Z.!?']", ' ', tweet)
    # Removing additional whitespaces
    tweet = re.sub(r" +", ' ', tweet)
    tweet = tweet.lower()
    return tweet

def extract_features(img, model):
    # input_shape = (224,224,3)
    # img = image.load_img(
    #             img_path,
    #             target_size=(
    #                 input_shape[0],
    #                 input_shape[1]
    #             )
    #         )

    # img_array = image.img_to_array(img)
    # expanded_img_array = np.expand_dims(img_array, axis=0)
    # preprocessed_img = preprocess_input(expanded_img_array)

    # ----------------------------------------------------------------
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    # image = ImageOps.fit(img, size, Image.ANTIALIAS)
    image = img.resize(size)
    # turn the image into a numpy array
    img_array = np.asarray(image)

    # display the resized image
    # image.show()

    # Normalize the image
    # normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

    # Load the image into the array
    # data[0] = normalized_image_array
    # ----------------------------------------------------------------

    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)

    features = model.predict(preprocessed_img)
    flattened_features = features.flatten()
    normalized_features = flattened_features / norm(flattened_features)

    return normalized_features

def amount_to_int(amount):
    result = ['' for _ in range(len(amount))]
    for idx in range(len(amount)):
        amount_ele = re.findall(r'\d+', amount[idx])
        if not amount_ele:
            ls_count = ['một', 'hai', 'ba', 'bốn', 'năm',
                        'sáu', 'bảy', 'tám', 'chín', 'mười']
            for ele in ls_count:
                if ele in amount[idx].lower():
                    result[idx] = (ls_count.index(ele) + 1)
        else:
            result[idx] = (int(amount_ele[0]))

    return result

def cal_total_price(price, amount):
    return sum(np.array(price, dtype=int) * np.array(amount, dtype=int))

def is_dict(value):
    return isinstance(value, dict)

def is_list(value):
    return isinstance(value, list)

def check_list_empty(lst):
    """
    Check list is a empty list
    Is empty list: return True
    """
    for ele in lst:
        if ele != "":
            return False
    return True

# Replace to Unicode
def compound2unicode(text):
    # https://gist.github.com/redphx/9320735`
    text = text.replace("\u0065\u0309", "\u1EBB")  # ẻ
    text = text.replace("\u0065\u0301", "\u00E9")  # é
    text = text.replace("\u0065\u0300", "\u00E8")  # è
    text = text.replace("\u0065\u0323", "\u1EB9")  # ẹ
    text = text.replace("\u0065\u0303", "\u1EBD")  # ẽ
    text = text.replace("\u00EA\u0309", "\u1EC3")  # ể
    text = text.replace("\u00EA\u0301", "\u1EBF")  # ế
    text = text.replace("\u00EA\u0300", "\u1EC1")  # ề
    text = text.replace("\u00EA\u0323", "\u1EC7")  # ệ
    text = text.replace("\u00EA\u0303", "\u1EC5")  # ễ
    text = text.replace("\u0079\u0309", "\u1EF7")  # ỷ
    text = text.replace("\u0079\u0301", "\u00FD")  # ý
    text = text.replace("\u0079\u0300", "\u1EF3")  # ỳ
    text = text.replace("\u0079\u0323", "\u1EF5")  # ỵ
    text = text.replace("\u0079\u0303", "\u1EF9")  # ỹ
    text = text.replace("\u0075\u0309", "\u1EE7")  # ủ
    text = text.replace("\u0075\u0301", "\u00FA")  # ú
    text = text.replace("\u0075\u0300", "\u00F9")  # ù
    text = text.replace("\u0075\u0323", "\u1EE5")  # ụ
    text = text.replace("\u0075\u0303", "\u0169")  # ũ
    text = text.replace("\u01B0\u0309", "\u1EED")  # ử
    text = text.replace("\u01B0\u0301", "\u1EE9")  # ứ
    text = text.replace("\u01B0\u0300", "\u1EEB")  # ừ
    text = text.replace("\u01B0\u0323", "\u1EF1")  # ự
    text = text.replace("\u01B0\u0303", "\u1EEF")  # ữ
    text = text.replace("\u0069\u0309", "\u1EC9")  # ỉ
    text = text.replace("\u0069\u0301", "\u00ED")  # í
    text = text.replace("\u0069\u0300", "\u00EC")  # ì
    text = text.replace("\u0069\u0323", "\u1ECB")  # ị
    text = text.replace("\u0069\u0303", "\u0129")  # ĩ
    text = text.replace("\u006F\u0309", "\u1ECF")  # ỏ
    text = text.replace("\u006F\u0301", "\u00F3")  # ó
    text = text.replace("\u006F\u0300", "\u00F2")  # ò
    text = text.replace("\u006F\u0323", "\u1ECD")  # ọ
    text = text.replace("\u006F\u0303", "\u00F5")  # õ
    text = text.replace("\u01A1\u0309", "\u1EDF")  # ở
    text = text.replace("\u01A1\u0301", "\u1EDB")  # ớ
    text = text.replace("\u01A1\u0300", "\u1EDD")  # ờ
    text = text.replace("\u01A1\u0323", "\u1EE3")  # ợ
    text = text.replace("\u01A1\u0303", "\u1EE1")  # ỡ
    text = text.replace("\u00F4\u0309", "\u1ED5")  # ổ
    text = text.replace("\u00F4\u0301", "\u1ED1")  # ố
    text = text.replace("\u00F4\u0300", "\u1ED3")  # ồ
    text = text.replace("\u00F4\u0323", "\u1ED9")  # ộ
    text = text.replace("\u00F4\u0303", "\u1ED7")  # ỗ
    text = text.replace("\u0061\u0309", "\u1EA3")  # ả
    text = text.replace("\u0061\u0301", "\u00E1")  # á
    text = text.replace("\u0061\u0300", "\u00E0")  # à
    text = text.replace("\u0061\u0323", "\u1EA1")  # ạ
    text = text.replace("\u0061\u0303", "\u00E3")  # ã
    text = text.replace("\u0103\u0309", "\u1EB3")  # ẳ
    text = text.replace("\u0103\u0301", "\u1EAF")  # ắ
    text = text.replace("\u0103\u0300", "\u1EB1")  # ằ
    text = text.replace("\u0103\u0323", "\u1EB7")  # ặ
    text = text.replace("\u0103\u0303", "\u1EB5")  # ẵ
    text = text.replace("\u00E2\u0309", "\u1EA9")  # ẩ
    text = text.replace("\u00E2\u0301", "\u1EA5")  # ấ
    text = text.replace("\u00E2\u0300", "\u1EA7")  # ầ
    text = text.replace("\u00E2\u0323", "\u1EAD")  # ậ
    text = text.replace("\u00E2\u0303", "\u1EAB")  # ẫ
    text = text.replace("\u0045\u0309", "\u1EBA")  # Ẻ
    text = text.replace("\u0045\u0301", "\u00C9")  # É
    text = text.replace("\u0045\u0300", "\u00C8")  # È
    text = text.replace("\u0045\u0323", "\u1EB8")  # Ẹ
    text = text.replace("\u0045\u0303", "\u1EBC")  # Ẽ
    text = text.replace("\u00CA\u0309", "\u1EC2")  # Ể
    text = text.replace("\u00CA\u0301", "\u1EBE")  # Ế
    text = text.replace("\u00CA\u0300", "\u1EC0")  # Ề
    text = text.replace("\u00CA\u0323", "\u1EC6")  # Ệ
    text = text.replace("\u00CA\u0303", "\u1EC4")  # Ễ
    text = text.replace("\u0059\u0309", "\u1EF6")  # Ỷ
    text = text.replace("\u0059\u0301", "\u00DD")  # Ý
    text = text.replace("\u0059\u0300", "\u1EF2")  # Ỳ
    text = text.replace("\u0059\u0323", "\u1EF4")  # Ỵ
    text = text.replace("\u0059\u0303", "\u1EF8")  # Ỹ
    text = text.replace("\u0055\u0309", "\u1EE6")  # Ủ
    text = text.replace("\u0055\u0301", "\u00DA")  # Ú
    text = text.replace("\u0055\u0300", "\u00D9")  # Ù
    text = text.replace("\u0055\u0323", "\u1EE4")  # Ụ
    text = text.replace("\u0055\u0303", "\u0168")  # Ũ
    text = text.replace("\u01AF\u0309", "\u1EEC")  # Ử
    text = text.replace("\u01AF\u0301", "\u1EE8")  # Ứ
    text = text.replace("\u01AF\u0300", "\u1EEA")  # Ừ
    text = text.replace("\u01AF\u0323", "\u1EF0")  # Ự
    text = text.replace("\u01AF\u0303", "\u1EEE")  # Ữ
    text = text.replace("\u0049\u0309", "\u1EC8")  # Ỉ
    text = text.replace("\u0049\u0301", "\u00CD")  # Í
    text = text.replace("\u0049\u0300", "\u00CC")  # Ì
    text = text.replace("\u0049\u0323", "\u1ECA")  # Ị
    text = text.replace("\u0049\u0303", "\u0128")  # Ĩ
    text = text.replace("\u004F\u0309", "\u1ECE")  # Ỏ
    text = text.replace("\u004F\u0301", "\u00D3")  # Ó
    text = text.replace("\u004F\u0300", "\u00D2")  # Ò
    text = text.replace("\u004F\u0323", "\u1ECC")  # Ọ
    text = text.replace("\u004F\u0303", "\u00D5")  # Õ
    text = text.replace("\u01A0\u0309", "\u1EDE")  # Ở
    text = text.replace("\u01A0\u0301", "\u1EDA")  # Ớ
    text = text.replace("\u01A0\u0300", "\u1EDC")  # Ờ
    text = text.replace("\u01A0\u0323", "\u1EE2")  # Ợ
    text = text.replace("\u01A0\u0303", "\u1EE0")  # Ỡ
    text = text.replace("\u00D4\u0309", "\u1ED4")  # Ổ
    text = text.replace("\u00D4\u0301", "\u1ED0")  # Ố
    text = text.replace("\u00D4\u0300", "\u1ED2")  # Ồ
    text = text.replace("\u00D4\u0323", "\u1ED8")  # Ộ
    text = text.replace("\u00D4\u0303", "\u1ED6")  # Ỗ
    text = text.replace("\u0041\u0309", "\u1EA2")  # Ả
    text = text.replace("\u0041\u0301", "\u00C1")  # Á
    text = text.replace("\u0041\u0300", "\u00C0")  # À
    text = text.replace("\u0041\u0323", "\u1EA0")  # Ạ
    text = text.replace("\u0041\u0303", "\u00C3")  # Ã
    text = text.replace("\u0102\u0309", "\u1EB2")  # Ẳ
    text = text.replace("\u0102\u0301", "\u1EAE")  # Ắ
    text = text.replace("\u0102\u0300", "\u1EB0")  # Ằ
    text = text.replace("\u0102\u0323", "\u1EB6")  # Ặ
    text = text.replace("\u0102\u0303", "\u1EB4")  # Ẵ
    text = text.replace("\u00C2\u0309", "\u1EA8")  # Ẩ
    text = text.replace("\u00C2\u0301", "\u1EA4")  # Ấ
    text = text.replace("\u00C2\u0300", "\u1EA6")  # Ầ
    text = text.replace("\u00C2\u0323", "\u1EAC")  # Ậ
    text = text.replace("\u00C2\u0303", "\u1EAA")  # Ẫ
    return text