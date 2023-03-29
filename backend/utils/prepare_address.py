from unidecode import unidecode
# import numpy as np
import json
import re


### get list of dicts from json
def dicts_from_json(json_path='update_districts.json'):
    with open(json_path, 'r') as f:
        return_dicts = json.load(f)
    return return_dicts

### tags (preprocessed) to codes (list of codes)
### Province: 'Tinh|Thanh pho'
### District: 'Huyen|Thi xa|Quan|Thanh pho'
### Ward:'Xa|Phuong|Thi tran'
### Vill: 'Ap|Thon|Ban|Doi|KCB|KCN|KCX|KDC|KDT|Khoi|Khom|Khu|Lang|Buon|CC|Cum|LN|Pho|TDP|To|Xom|Khu pho'
### Street: ''
### tags (preprocessed) to codes (list of codes)
def build_enc(dicts, code, use_tag=True, prefix=None, name=None, abbrev_dict={}):
    ### if not use tag then
    ### prefix is use to remove prefix like "tinh", "thanhpho"
    return_dict = {}
    for d in dicts:
        if not use_tag:
            key = unidecode(d[name].lower())
            key = re.sub(r'\s+', ' ', key)
            key = re.sub(r'^\s|\s$', '', key)
            try: return_dict[re.sub(r'\s+', '', key)].update([d[code]])
            except: return_dict[re.sub(r'\s+', '', key)] = set([d[code]])
            for w in prefix: 
                if re.search(r'^' + w, key): key_sub = re.sub(w+r'\s', '', key)
                else: continue
                if len(key_sub.split(' ')) < 2 or \
                    (len(key_sub.split(' '))==2 and re.search(r'\d+', key_sub)): continue
                try: return_dict[re.sub(r'\s+', '', key_sub)].update([d[code]])
                except: return_dict[re.sub(r'\s+', '', key_sub)] = set([d[code]])
                if w in abbrev_dict.keys():
                    try: return_dict[abbrev_dict[w] + re.sub(r'\s+', '', key_sub)].update([d[code]])
                    except: return_dict[abbrev_dict[w] + re.sub(r'\s+', '', key_sub)] = set([d[code]])
        else:
            for tag in d['tags']:
                try: return_dict[tag].append( d[code] ) 
                except: return_dict[tag] = [ d[code] ]
    return return_dict

### code to name (full name)
def build_dec(dicts, code, name):
    return_dict = {}
    for d in dicts:
        return_dict[ d[code] ] = d[name]
    return return_dict

### return dictionary of Acode in Bcode
### for example a District is in a Province
### because take the "code" so dict is 1 key - 1 value
def AinB(dicts, Acode, Bcode):
    return_dict = {}
    for d in dicts:
        return_dict[ d[Acode] ] = d[Bcode]
    return return_dict

def preparation(folder='json'):
    print("Start preparing address inputs...")
    address_inp = {}

    ### get dictionaries from json files in folder
    province_dicts = dicts_from_json(folder + '/update_provinces.json')
    district_dicts = dicts_from_json(folder + '/update_districts.json')
    ward_dicts = dicts_from_json(folder + '/new_wards.json')
    vill_dicts = dicts_from_json(folder + '/update_villages.json')
    street_dicts = dicts_from_json(folder + '/update_streets.json')

    address_inp['province_enc'] = build_enc(province_dicts, 'ProvinceCode', 
                    use_tag=False, name='Province', prefix=['tinh', 'thanh pho'])
    address_inp['province_dec'] = build_dec(province_dicts, 'ProvinceCode', 'Province')

    address_inp['district_enc'] = build_enc(district_dicts, 'DistrictCode', 
                    use_tag=False, name='District', prefix=['huyen', 'thi xa', 'quan', 'thanh pho'])
    address_inp['district_dec'] = build_dec(district_dicts, 'DistrictCode', 'District')

    address_inp['ward_enc'] = build_enc(ward_dicts, 'WardCode',
                    use_tag=False, name='Ward', prefix=['xa','phuong','thi tran','tt','p'],
                    abbrev_dict={'p':'phuong','tt':'thitran'})
    address_inp['ward_dec'] = build_dec(ward_dicts, 'WardCode', 'Ward')

    address_inp['vill_enc'] = build_enc(vill_dicts, 'LangID',
                    use_tag=False, name='Lang', 
                    prefix=['ap','thon','ban', 'doi', 'kcb', 'kcn', 'kcx', 'kdc', 'kdt', 'khoi', 'khom', 
                        'khu', 'lang', 'buon', 'cc', 'cum','ln','pho','tdp', 'to','xom','khu pho', 'kp'], 
                    abbrev_dict={'kp':'khupho', 'kcb':'khuchebien', 'kcn':'khucongnghiep', 'kcx':'khuchexuat', 'kdc':'khudancu',
                        'kdt':'khudothi', 'cc':'chungcu', 'ln':'langnghe', 'tdp':'todanpho'})
    address_inp['vill_dec'] = build_dec(vill_dicts, 'LangID', 'Lang')

    address_inp['street_enc'] = build_enc(street_dicts, 'StreetID',
                    use_tag=False, name='StreetName', prefix=['duong'])
    address_inp['street_dec'] = build_dec(street_dicts, 'StreetID', 'StreetName')

    address_inp['street_in_district'] = AinB(street_dicts, 'StreetID', 'DistrictCode')
    address_inp['street_in_province'] = AinB(street_dicts, 'StreetID', 'ProvinceCode')
    address_inp['ward_in_district'] = AinB(ward_dicts, 'WardCode', 'DistrictCode')
    address_inp['ward_in_province'] = AinB(ward_dicts, 'WardCode', 'ProvinceCode')
    address_inp['district_in_province'] = AinB(district_dicts, 'DistrictCode', 'ProvinceCode')
    address_inp['vill_in_ward'] = AinB(vill_dicts, 'LangID', 'WardCode')
    address_inp['vill_in_district'] = AinB(vill_dicts, 'LangID', 'DistrictCode')
    address_inp['vill_in_province'] = AinB(vill_dicts, 'LangID', 'ProvinceCode')

    print("End preparing address inputs...")

    return address_inp