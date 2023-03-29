DICT_FULLNAME = {
    'Sét Xanh - S002 - Xanh, Nude, Cam - S,M,L': 'S002',
    'Set Vest nơ - D005 - Đen - S,M,L': 'D005',
    'Set vest - D006,7 - Đen, Nude - S,M,L': 'D006',
    'Sét vàng- S006 - Vàng- S,M,L': 'S006',
    'Set trắng nút - S009 - Trắng - S,M,L': 'S009',
    'Set sơ mo cổ nơ- S005- Trắng - S,M,L': 'S005',
    'Set Hồng Vest Váy Ngắn - S003 - Hồng - S,M,L': 'S003',
    'Sét Đen Sẻ - S008 - Đen - S,M,L': 'S008',
    'Set đầm sơ mi trắng-S004- Trắng- S,M,L': 'S004',
    'Set cổ xéo- DS001- Trắng- S,M,L': 'DS001',
    'Đần nude lưới- D0015- Nude - S,M,L': 'D0015',
    'Đầm xám nút - D0016': 'D0016',
    'Đầm trắng dập li - D008 - Trắng - S,M,L': 'D008',
    'Đầm trắng 2 dây - D0010 - Trắng - S,M,L': 'D0010',
    'Đầm nude xoắn - D0012 - Nude - S,M,L': 'D0012',
    'Đầm nâu nút - D0016,17 - Nâu, Xám - S,M,L': 'D0016',
    'Đầm caro - D009 - Xanh - S,M,L': 'D009',
    'Đầm caro cổ vest - D0011 - Xanh - S,M,L': 'D0011',
    'Đầm body vest-D0013 - Hồng - S,M,L': 'D0013',
    'Đầm Body Nút - Da - S,M,L': 'D0017',
    'Đầm body nude ren- D0014 - Nude - S,M,L': 'D0014',
    'Đầm body lưới - D004 - Đen - S,M,L': 'D004'
}

LS_PRODUCT = {
    'S002': 'set xanh',
    'D005': 'set vest nơ',
    'D006': 'set vest',
    'S006': 'set vàng',
    'S009': 'set trắng nút',
    'S005': 'set sơ mi cổ nơ',
    'S003': 'set hồng vest váy ngắn',
    'S008': 'set đen sẻ',
    'S004': 'set đầm sơ mi trắng',
    'DS001': 'set cổ xéo',
    'D0015': 'đầm nude lưới',
    'D008': 'đầm trắng dập li',
    'D0010': 'đầm trắng 2 dây',
    'D0012': 'đầm nude xoắn',
    'D0016': 'đầm nâu nút',
    'D009': 'đầm caro',
    'D0011': 'đầm caro cổ vest',
    'D0013': 'đầm body vest',
    'D0017': 'đầm body nút',
    'D0014': 'đầm body nude ren',
    'D004': 'đầm body lưới'
}

PATH_FILE_PATTERNS = "model/quangminhtien_intents.json"
PATH_FILE_MAPPING = "model/pattern_similarity/mapping/"
PRETRAIN_MODEL = 'model/pattern_similarity/model/pretrained_model'
STATE_DICT = 'model/pattern_similarity/state_dict/'
MAPPING_TABLE = 'model/pattern_similarity/mapping/'
API_AUGMENT_DATA = 'http://172.28.0.23:35100/augment_data'

BATCH_SIZE = 256
NUM_EPOCHS = 1


MINUTES_RESTART_MULTIPRODUCT = 2
MINUTES_RESTART_INPROCESS = 3

