import pymongo
client = pymongo.MongoClient("mongodb://admin:admin@chatbot-mongo-1:27017/admin")
my_db = client['chatbot_quangminhtien']
my_col = my_db['products']


document = my_col.find({}, {"_id":0})
product_list = [item['name'] for item in document]
product_regex1 = r'(' + '|'.join(product_list) + r')'
product_regex = r'((\d+)?\s*(c[áa]i|b[ộo])?\s*{}\s*(size)?\s*(x*s|m|x*l)?)'.format(product_regex1)
size_regex = r'\b(size)\s*(x*s|m|x*l)\b'
phone_regex = r'\b(08[1-9]\d{7}|09\d{8}|05[2|6|8|9]\d{7}|07[0|6|7|8|9]\d{7}|03[2-9]\d{7})\b'

address_regex = r'\b(địa\s*chỉ|dia\s*chi)\b'

agree = r'\b([o|ô|0|u]k[a-zA-Z]*|oce|[d|z][a|ạ|à][a-zA-Z]*|c[o|ó]|ola|[u|ừ|o|ù][m|h|k|a]*|[o|ờ]|v[a|â|ầ]n*g|v[' \
        r'a|â|ầ]ng*|[d|đ][u|ú]n*g|[đ|d]c|[d|đ][u|ư][ơ|o|ợ]c|r[ồ|u|ù|o|ô]i|tks|thank|thanks|c[a|ả]m\s*[o|ơ]n|đ[' \
        r'o|ồ]ng\s*[y|ý]|dr)\b'
disagree = r'\b(th[u|ô|o][i|y]*|(hix)+|kh[o|ô]ng|ko|k\s(\s)*|(hu)+|ti[e|ế|ê]c)\b'

process_dict = {
    r"phường\.": "phường",
    r"quận\.": "quận",
    r"(?<=phường\s\d)q(?=\d)": " quận ",
    r"(?<=phường\s\d\d)q(?=\d)": " quận ",
    r"thành phố\.": "thành phố",
    r"tỉnh\.": "tỉnh",
    r"t\.\s+x[ãa]\.*": "thị xã",
    r"[đd]/c": "địa chỉ",
    r"[đd]c\s*:": "địa chỉ",
    r"\st\.": " tỉnh",
    r"^t\.": " tỉnh",
    r'địa\schỉhị': "địa chỉ",
    r'buôn\s+ma\s+thuộc': "buôn mê thuộc",
    r'buon\s+ma\s+thuoc': "buôn mê thuộc",
    r'bao\snhi[eẻẹệ][uhiy]': "bao nhiêu",
    r'(?<=chất\s)v[ãa]i': "vải",
    r'v[aã]i\s(?=g[ìi])': "vải ",
    r'(?<=m[ặaạă][ct]\s)[sz]a[i]': "size",
    r'[sz]ai\s*(?=\b[lms]\b)': "size ",
    r'nhi[êe]?u v[iị]': "nhiêu vậy",
    r'bu\s[đd]i[eệ]n': "bưu điện",
    r'(?<=(bao|bây))\sh': " giờ",
    r'(?<=\d)jo': " giờ",
    r'(?<=\d)(tp)?hcm': " thành phố hồ chí minh",
    r'thị\strấn\.?\shuế': "thừa thiên huế",
    r'b[ìi]nh\sth[ạa]ch': "bình thạnh",
    r's[aà]i\s?g[òo]n': "thành phố hồ chí minh",
    r'c[aá]ch\sm[aạ]ng\sth[aá]ng\s8': "cách mạng tháng tám",
    r'ph[uư][oơớ]c\slong\sbạn': "phước long b",
    r't[aă]ng\snh[oơ]n\sph[uú]\sbạn': "tăng nhơn phú b",
    r'v[iĩ]nh\sl[oọôộ]c\sbạn': "vĩnh lộc b",
    r'b[iì]nh\sh[uư]ng\sh[oò][aà]\sbạn': "bình hưng hòa b",
    r'b[iì]nh\str[iị]\s[dđ][oô]ng\sbạn': "bình trị đông b",
    r'[dđ][oô]ng\sl[ợơo]i\sbạn': "đông lợi b",
    r'\b30/4\b': "ba mươi tháng tư",
    r'\b3/2\b': "ba tháng hai",
    r'(?<=[0-9])\s?máy': " mấy",
    r'eo(?=\d)': "eo ",
    r'nặng(?=\d)': "nặng ",
    r'cao(?=\d)': "cao ",
    r'bộ\snay': "bộ này",
    r'\b[dđ]k\s*(k|kh[oô]ng)\b': 'được không',
    r'\b[dđ]k\s*(?!(k|kh[oô]ng))\b': 'được không ',
    r"n[ếée]u\sc[òo]n": "",
    r"n[ếée]u\sc[oó]": ""
}


# Bắt regex các trường hợp báo sai thông tin khi chốt đơn hàng
special_address = r'\b(công\s*ty|(trường\s*)?(mầm\s*non|mn|tiểu\s*học|thcs|thpt|cao\s*đẳng|đại\s*học|đh|cđ)|văn\s*phòng|'\
                    r'khách\s*sạn|nhà\s*nghỉ|hotel|ktx|k[ý|í]\s*túc\s*xá|tiệm|cửa\s*hàng|quán|nhà\s*văn\s*hóa|bệnh\s*viện|'\
                    r'ngân\s*hàng|bank|bưu\s*điện|ubnd|ủy\s*ban\s*nhân\s*dân|vinhomes|chung\s*cư|tòa\s*nhà|'\
                    r'trung\s*tâm\s*thương\s*mại|tttm|vinhomes|nhà\s*văn\s*hóa|quầy\s*thuốc|trung\s*tâm\s*giải\s*trí|'\
                    r'bida|đồn\s*công\s*an|building|cafe|phòng\s*khám)\b'