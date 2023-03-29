import pathlib
import re
import numpy as np
from time import time
from unidecode import unidecode
import spacy
from backend.config.config import get_config
config_app = get_config()

def levenshtein(s1, s2):
    size_x = len(s1) + 1
    size_y = len(s2) + 1
    m = np.zeros ((size_x, size_y))
    for x in range(size_x): m [x, 0] = x
    for y in range(size_y): m [0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if s1[x-1] == s2[y-1]: m [x,y] = min(m[x-1, y] + 1,m[x-1, y-1],m[x, y-1] + 1)
            else: m [x,y] = min(m[x-1,y] + 1,m[x-1,y-1] + 1,m[x,y-1] + 1)
    return m[size_x - 1, size_y - 1]

def score_compute(pred, truth):
    ### preprocess truth
    truth = unidecode(truth.lower())
    truth = re.sub(r'\s', '', truth)
    reduce_fact = 1-np.log(levenshtein(pred, truth)+1)/len(truth)
    return len(pred)*round(reduce_fact, 2)

def preprocess(sent):
    sent = sent.lower()
    sent = re.sub(r'quận 9',r' thủ đức', sent)
    sent = re.sub(r'quận 2',r' thủ đức', sent)
    sent = unidecode(sent)
    sent = re.sub(r'[^\w\d/\-]|_', ' ', sent)
    sent = re.sub(r'^\s|\s$', '', sent)
    sent = re.sub(r'\s+', ' ', sent)
    return sent

def re_search(sent, enc, dec, info=None):
    result = []
    sent = re.sub('-', ' ', sent)
    words = sent.split(' ')
    ### SEGMENT WORD-LEVEL
    for l in range(1,6):
        for i in range(len(words)-l+1):
            word = ''.join(words[i:i+l])

            ### to reduce the #samples of villages
            if l==1 and info=='vill':
                digit_word = ['mot', 'hai', 'ba', 'bon', 'nam','sau', 
                             'bay', 'tam', 'chin', 'muoi', 'muoimot', 'muoihai']
                digit_str = [str(i) for i in range(1,12)]
                if re.sub(r'\s', '', word) in digit_word+digit_str:
                    continue

            # print(word)
            size = len(word) + (l)
            try:
                start_ofs = len(' '.join(words[:i]) )
                #print(start_ofs) 
                if len(' '.join(words[:i]) ) > 0: start_ofs += 1 ### plus 1 due to ' ' before the word
                end_ofs = start_ofs + size
                #print(end_ofs)
                result += [(t, (start_ofs, end_ofs ), size ) for t in enc[word] ]
                # result += [(t, (start_ofs, end_ofs ), score_compute(word, dec[t]) ) for t in enc[word] ]
            except KeyError:
                continue

    ### SEGMENT CHAR-LEVEL in WORD
    #for i in range(len(words)):
    #    word = words[i]
    #    for l in range(1,len(word)):
    #        for j in [0, len(word)-l-1]:
    #            w = word[j:j+l+1]
    #            size = len(w)
    #            try:
    #                start_ofs = len(' '.join(words[:i]) ) + j 
    #                if len(' '.join(words[:i]) ) > 0: start_ofs += 1 ### plus 1 due to ' ' before the word
    #                end_ofs = start_ofs + size
    #                result += [(t, (start_ofs, end_ofs ), size ) for t in enc[w] ]
    #            except:
    #                continue


    return list(set(result))

class SortedList():
    def __init__(self, cost_function):
        self.lst = []
        self.weights = [0]*5
        self.cost_function = cost_function
    
    def append(self, new_value):
        min_weight = np.min(self.weights)
        min_pos = np.argmin(self.weights)
        # print(min_weight)
        if new_value not in self.lst:
            new_cost = self.cost_function(new_value)
            # print(new_cost)
            if new_cost > min_weight and new_cost not in self.weights:
                self.lst = [i for i in self.lst if self.cost_function(i) > min_weight]
                self.weights[min_pos] = self.cost_function(new_value)
                self.lst.append(new_value)
                # print(self.lst)
            elif new_cost == min_weight:
                self.lst.append(new_value)
                # print(self.lst)

    def get(self, n, add_noise=True):
        result = sorted(self.lst, key = self.cost_function)
        if n <= len(result): result = result[-n:]
        # print(result)
        # if add_noise:
        #     noises = []
        #     for l in result:
        #         for i in range(len(self.lst[0])):
        #             noise = [l[j] if j!=i else ('',None,-0.1) for j in range(len(l))]
        #             if noise not in noises: noises += [noise]
        #     result += noises
        return result

### The functions ABC_lists() have similar steps:
### ### For each set of address, e.g. (w,d,p), (d,p)
### ### Check conditions, including: 
### ### ### 1/ The lower is in the larger (e.g. a ward in a district)
### ### ### 2/ The lower appear before the larger (e.g. a ward is written before a district)
### Sort the list and get the top 100 score (score is computed based on the number of characters matched)
### Add empty set in case there are no large units (e.g. no province, no district but have wards)
### Return
def dp_lists(district_ls, province_ls, address_inp):
    district_in_province = address_inp['district_in_province']

    result = SortedList(lambda x:np.sum(np.array(x, dtype=object)[:,2]))
    zipped = [(i,j) for i in district_ls for j in province_ls]
    for (d,p) in zipped:
        cond_1 = d[0]=='' or district_in_province[d[0]]==p[0] or p[0]==''
        cond_2 = d[1]==None or p[1]==None or d[1][1] <= p[1][0]
        cond_3 = d[1]==None or p[1]==None or p[1][0] - d[1][1] <= 12
        if not cond_1 or not cond_2 or not cond_3: continue

        res_d, res_p = list(d), list(p)
        if res_d[0]!='' and res_p[0]=='': res_p[0] = district_in_province[res_d[0]]
        res_d[2] = res_d[2]*1.2
        res_p[2] = res_p[2]*1.2
        result.append([res_d, res_p])
    
    return result.get(10)

### return list of (ward, district, province)
### ### condition 1->3 check whether ward in district and district in province
### ### while condition 4->5 check whether they are in good order
def wdp_lists(ward_ls, dp_lists, address_inp):
    ward_in_district = address_inp['ward_in_district']
    ward_in_province = address_inp['ward_in_province']
    district_in_province = address_inp['district_in_province']

    result = SortedList(lambda x:np.sum(np.array(x, dtype=object)[:,2]))
    zipped = [(i,j,k) for i in ward_ls for (j,k) in dp_lists]
    for (w,d,p) in zipped:
        cond_1 = True
        cond_2 = w[0]=='' or ward_in_province[w[0]]==p[0] or p[0]==''
        cond_3 = w[1]==None or d[1]==None or w[1][1] <= d[1][0]
        cond_4 = w[1]==None or p[1]==None or w[1][1] <= p[1][0]
        cond_5 = w[1]==None or d[1]==None or d[1][0] - w[1][1] <= 12
        cond_6 = w[1]==None or p[1]==None or (d[1]!=None or p[1][0] - w[1][1] <= 12)
        if not cond_1 or not cond_2 or not cond_3 \
            or not cond_4 or not cond_5 or not cond_6: continue
            
        res_w, res_d, res_p = list(w), list(d), list(p)
        if res_w[0]!='' and res_d[0]=='': res_d[0] = ward_in_district[res_w[0]]
        if res_d[0]!='' and res_p[0]=='': res_p[0] = district_in_province[res_d[0]]
        result.append([res_w, res_d, res_p])

    return result.get(10)

### return list of vill : (ward, district, province) provided
def vwdp_lists(vill_ls, wdp_ls, address_inp):
    vill_in_ward = address_inp['vill_in_ward']
    vill_in_district = address_inp['vill_in_district']
    vill_in_province = address_inp['vill_in_province']
    ward_in_district = address_inp['ward_in_district']
    district_in_province = address_inp['district_in_province']

    result = SortedList(lambda x:np.sum(np.array(x, dtype=object)[:,2]))
    sum = 0
    zipped = [(i,j) for i in vill_ls for j in wdp_ls]
    for (v, (w,d,p)) in zipped:
        # cond_1 = v[0]=='' or vill_in_ward[v[0]]==w[0] or w[0]==''
        # cond_2 = v[0]=='' or vill_in_district[v[0]]==d[0] or d[0]==''
        cond_3 = v[0]=='' or vill_in_province[v[0]]==p[0] or p[0]==''
        cond_1 = True; cond_2 = True
        cond_4 = v[1]==None or w[1]==None or v[1][1] <= w[1][0]
        cond_5 = v[1]==None or d[1]==None or v[1][1] <= d[1][0]
        cond_6 = v[1]==None or p[1]==None or v[1][1] <= p[1][0]
        cond_7 = v[1]==None or w[1]==None or w[1][0] - v[1][1] <= 12
        cond_8 = v[1]==None or d[1]==None or (w[1]!=None or d[1][0] - v[1][1] <= 12)
        cond_9 = v[1]==None or p[1]==None or (w[1]!=None or d[1]!=None or p[1][0]-v[1][1] <= 12)
        if not cond_1 or not cond_2 or not cond_3 \
            or not cond_4 or not cond_5 or not cond_6\
            or not cond_7 or not cond_8 or not cond_9: continue

        res_v, res_w, res_d, res_p = list(v), list(w), list(d), list(p)
        # print(list(v))
        if res_w[0]=='' and res_d[0]=='' and res_p[0]=='': res_p[0] = ''; res_d[0]='';res_w[0]=''; break
        if res_v[0]!='' and res_w[0]=='': res_w[0] = vill_in_ward[res_v[0]]
        if res_w[0]!='' and res_d[0]=='': res_d[0] = ward_in_district[res_w[0]]
        if res_d[0]!='' and res_p[0]=='': res_p[0] = district_in_province[res_d[0]]
        # print(res_v)
        result.append([res_v, res_w, res_d, res_p])

    # print("===========================VWDP==========================")
    # tmp = result.get(10)
    # vill_dec = address_inp['vill_dec']
    # for i in tmp:
    #     try: print(vill_dec[i[0][0]], i[0][-1], sum([j[2] for j in i]))
    #     except: pass
    # print("===========================VWDP==========================")

    return result.get(10)

def svwdp_lists(street_ls, vwdp_ls, address_inp):
    street_in_district = address_inp['street_in_district']
    street_in_province = address_inp['street_in_province']

    result = SortedList(lambda x:np.sum(np.array(x, dtype=object)[:,2]))
    sum = 0
    # start = time()
    zipped = [(i,j) for i in street_ls for j in vwdp_ls]
    # print("Zip time:", time() - start)

    # cond_time = 0
    # append_time = 0

    for (s, (v,w,d,p)) in zipped:
        # start = time()
        cond_1 = s[0]=='' or street_in_district[s[0]]==d[0] or d[0]==''
        # cond_2 = s[0]=='' or street_in_province[s[0]]==p[0] or p[0]==''
        # cond_1 = True
        cond_2 = True
        cond_3 = s[1]==None or v[1]==None or s[1][1] <= v[1][0]
        cond_4 = s[1]==None or w[1]==None or s[1][1] <= w[1][0]
        cond_5 = s[1]==None or d[1]==None or s[1][1] <= d[1][0]
        cond_6 = s[1]==None or p[1]==None or s[1][1] <= p[1][0]
        cond_7 = s[1]==None or v[1]==None or v[1][0] - s[1][1] <= 12
        cond_8 = s[1]==None or w[1]==None or (v[1]!=None or w[1][0]-s[1][1] <= 12)
        cond_9 = s[1]==None or d[1]==None or (v[1]!=None or w[1]!=None or d[1][0]-s[1][1] <= 12)
        cond_10 = s[1]==None or p[1]==None or (v[1]!=None or w[1]!=None or d[1]!=None or p[1][0]-s[1][1] <= 12)
        # cond_time += time()-start
        if not cond_1 or not cond_2 or not cond_3 \
            or not cond_4 or not cond_5 or not cond_6\
            or not cond_7 or not cond_8 or not cond_9 or not cond_10: continue
        # start = time()
        res_s, res_v, res_w, res_d, res_p = list(s), list(v), list(w), list(d), list(p)
        res_s[2] = res_s[2]*1.2
        # if res_s[0]!='' and res_d[0]=='': res_d[0] = street_in_district[res_s[0]]
        # if res_s[0]!='' and res_p[0]=='': res_p[0] = street_in_province[res_s[0]]
        result.append([res_s, res_v, res_w, res_d, res_p])
        # print(res_s, res_v, res_w, res_d, res_p)
        # result.append([list(s),list(v), list(w), list(d), list(p)])
        # append_time += time() - start

    # print("===========================SVWDP==========================")
    # tmp = result.get(10)
    # vill_dec = address_inp['vill_dec']
    # street_dec = address_inp['street_dec']
    # for i in tmp:
    #     try: print(street_dec[i[0][0]], i[0][-1], vill_dec[i[1][0]])
    #     except: pass
    # print("===========================SVWDP==========================")

    return result.get(10)

def full_address_lists(sent, svwdp_ls):
    result_list = []
    for (s,v,w,d,p,score) in svwdp_ls:
        t = [i[1][0] for i in (s,v,w,d,p) if i[1]!=None ]
        if len(t)==0: continue
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # print((s,v,w,d,p,score))
        sentence = re.sub(r'\s+$', '', sent[:t[0]])
        words = sentence.split(' ')

        house_num = ('', None, 0)
       
        if len(words) >= 2:
            # print('0')
            word = ' '.join([ words[-2], words[-1] ])
            cond_1 = re.search(r'\d+',words[-1]) is not None
            cond_2 = re.search(r'\d+',words[-2]) is not None
            cond_3 = re.search(r'^[\s\w\d/\-]+$',word) is not None
            
            if cond_1 or (cond_2 and cond_3 or words[-2] in ['lo','toa','khoi','khu', 'duong','to']): 
                if(cond_1):
                    start_ofs = len(' '.join(words[:-1]) ) 
                    if len(' '.join(words[:-1]) ) > 0: start_ofs += 1 ### plus 1 due to ' ' before the word
                    end_ofs = start_ofs + len(words[-1]) + 1
                    house_num = (words[-1], (start_ofs, end_ofs), 0)
                if(cond_2):
                    start_ofs = len(' '.join(words[:-2]) ) 
                    if len(' '.join(words[:-2]) ) > 0: start_ofs += 1 ### plus 1 due to ' ' before the word
                    end_ofs = start_ofs + len(words[-2]) + 1
                    house_num = (words[-2], (start_ofs, end_ofs), 0)
                if(cond_1 and cond_2):
                    start_ofs = len(' '.join(words[:-1]) ) 
                    if len(' '.join(words[:-1]) ) > 0: start_ofs += 1 ### plus 1 due to ' ' before the word
                    end_ofs = start_ofs + len(words[-1]) + 1
                    house_num = (words[-1], (start_ofs, end_ofs), 0)
            # result_list.append((house_num,s,v,w,d,p,score))
            # start_ofs = len(' '.join(words[:-1]) ) 
            # if len(' '.join(words[:-1]) ) > 0: start_ofs += 1 ### plus 1 due to ' ' before the word
            # end_ofs = start_ofs + len(words[-1])
            # house_num = (words[-1], (start_ofs, end_ofs), 0)
            # result_list.append((house_num,s,v,w,d,p,score))
        if len(words) >= 1 and house_num[0]=='':
            # print('3')
            cond_1 = re.search(r'\d+',words[-1]) is not None
            cond_2 = re.search(r'^[\w\d/\-]+$',words[-1]) is not None
            if cond_1 and cond_2: 
                start_ofs = len(' '.join(words[:-1]) ) 
                if len(' '.join(words[:-1]) ) > 0: start_ofs += 1 ### plus 1 due to ' ' before the word
                end_ofs = start_ofs + len(words[-1])
                house_num = (words[-1], (start_ofs, end_ofs), 0)
                result_list.append((house_num,s,v,w,d,p,score))
        # print((house_num,s,v,w,d,p,score))
        result_list.append((house_num,s,v,w,d,p,score))

    return result_list

def get_address(sent, address_inp, output_amount=5):
    street_enc = address_inp['street_enc']; street_dec = address_inp['street_dec']
    vill_enc = address_inp['vill_enc']; vill_dec = address_inp['vill_dec']
    ward_enc = address_inp['ward_enc']; ward_dec = address_inp['ward_dec']
    district_enc = address_inp['district_enc']; district_dec = address_inp['district_dec']
    province_enc = address_inp['province_enc']; province_dec = address_inp['province_dec']

    sent = preprocess(sent)
    if re.search(r'\/', sent):
        for i in range(1,len(sent)-1): 
            if sent[i]=='/' and not sent[i+1].isnumeric() \
                and not sent[i-1].isnumeric():
                sent = sent[:i] + ' ' + sent[i+1:]

    sub_sent = re.sub(r'[\-\/]', ' ', sent) ### in case long xuyen/an giang

    # start = time()
    street_ls = re_search(sent, street_enc, street_dec)
    # print("Search street ls time:", time()-start); start = time()
    vill_ls = re_search(sub_sent, vill_enc, vill_dec, 'vill')
    # print("Search vill ls time:", time()-start); start = time()
    ward_ls = re_search(sub_sent, ward_enc, ward_dec)
    # print("Search ward ls time:", time()-start); start = time()
    district_ls = re_search(sub_sent, district_enc, district_dec)
    # print("Search district ls time:", time()-start); start = time()
    province_ls = re_search(sub_sent, province_enc, province_dec)
    # print("Search province ls time:", time()-start); start = time()
    # print("LENGTH of lists:", len(street_ls), len(vill_ls), 
    #     len(ward_ls), len(district_ls), len(province_ls))

    street_ls += [('',None,0)]
    vill_ls += [('',None,0)]
    ward_ls += [('', None, 0)]
    district_ls += [('', None, 0)]
    province_ls += [('', None, 0)]

    # start = time()
    dp_ls = dp_lists(district_ls, province_ls, address_inp)
    # print("DP TIME:", time()-start); start = time()
    wdp_ls = wdp_lists(ward_ls, dp_ls, address_inp)
    # print("WDP TIME:", time()-start); start = time()
    vwdp_ls = vwdp_lists(vill_ls, wdp_ls, address_inp)
    # print("VWDP TIME:", time()-start); start = time()
    svwdp_ls = svwdp_lists(street_ls, vwdp_ls, address_inp) 
    # print("SVWDP TIME:", time()-start)
    # print(svwdp_ls)
    # start = time()
    tmp_ls = []
    for (s,v,w,d,p) in svwdp_ls:
        score = np.sum([i[2] for i in (s,v,w,d,p)])
        tmp_ls.append( [s,v,w,d,p,score] )
    tmp_sorted = sorted(tmp_ls, key = lambda x:x[5] )
    # print("SORTING TIME:", time() - start)

    # start= time()
    try: full_a_ls = full_address_lists(sent, tmp_sorted[-output_amount:])
    except: full_a_ls = full_address_lists(sent, tmp_sorted)
    # print("FULL LS TIME:", time()-start)
    
    # print(len(street_ls), len(vill_ls), len(ward_ls), len(district_ls), len(province_ls))
    # print(len(wdp_ls), len(vwdp_ls), len(svwdp_ls), len(full_a_ls))
    return full_a_ls


### result_list is a list of 
### (house_num,street,vill,ward,district,province,score)
### besides, they store Code or ID instead of Name
def expected_output(result_list, sentence, address_inp, output_amount=1):
    street_dec = address_inp['street_dec']
    vill_dec = address_inp['vill_dec']
    ward_dec = address_inp['ward_dec']
    district_dec = address_inp['district_dec']
    province_dec = address_inp['province_dec']
    company_name =('')
    nlp = spacy.load('data/third')
    doc = nlp(sentence)
    for ent in doc.ents:
        company_name = ent.text
        print(company_name)
    text = re.search(r'CÔNG TY|công ty|Công ty|Công Ty',company_name) is None
    if  text:
        company_name = ''
    sent = preprocess(sentence)
    result = {'p': sentence, 'p_normalize': sent, 'items': []}
    result['items'].append({'company_name': None})
    result['items'][-1]['company_name'] = company_name
    for address in result_list:
        result['items'].append(
            {'address': None, 'phoneNumber': None,
            'shortAddress': None, 'street': None, 'village': None, 'company_name': None,
            'wardName': None, 'wardCode': None, 'districtName': None, 
            'districtCode': None, 'cityName': None, 'cityCode': None, 
            'complete': False})
        result['items'][-1]['company_name'] = company_name
        # result['items'][-1]['score'] = str(address[-1]) 
        ### province
        if address[5][0]!='': 
            result['items'][-1]['cityCode'] = str(address[5][0])
            result['items'][-1]['cityName'] = province_dec[ address[5][0] ]

        ### district
        if address[4][0]!='':
            result['items'][-1]['districtCode'] = str(address[4][0])
            result['items'][-1]['districtName'] = district_dec[ address[4][0] ]

        ### ward
        if address[3][0]!='':
            result['items'][-1]['wardCode'] = str(address[3][0])
            result['items'][-1]['wardName'] = ward_dec[ address[3][0] ]
    
        ### village
        if address[2][0]!='':
            result['items'][-1]['village'] = str(vill_dec[ address[2][0] ])

        ### street
        if address[1][0]!='':
            result['items'][-1]['street'] = str(street_dec[ address[1][0] ])

        ### house number        
        house_num = address[0][0]

        ### Short Address
        tmp = [house_num] + [result['items'][-1][z] for z in ['street', 'village']]
        tmp = [z for z in tmp if z is not None and len(z)>0]
        if len(' '.join(tmp) ) > 1:
            result['items'][-1]['shortAddress'] = ' '.join(tmp)

        ### full address
        tmp = [result['items'][-1][z] for z in ['shortAddress', 'wardName', 'districtName', 'cityName']]
        tmp = [z for z in tmp if z is not None and len(z)>0]
        result['items'][-1]['address'] = ' '.join(tmp)
    
        # if result['items'][-1]['street'] is None \
        #     or house_num == '' or result['items'][-1]['cityName'] is None: 
        #     # print(address)
        #     result['items'] = result['items'][:-1]            

        ### Check if a complete address
        if result['items'][-1]['address'] is not None and \
                (result['items'][-1]['street'] is not None or \
                result['items'][-1]['village'] is not None) and \
                result['items'][-1]['wardName'] is not None and \
                result['items'][-1]['districtName'] is not None and \
                result['items'][-1]['cityName'] is not None and\
                house_num != '':
            result['items'][-1]['complete'] = True


    result['items'].reverse()
    # print("Len of initial result = ", len(result['items']))


    # for i in result['items'][:10]:
    #     print(i)


    result['items'] = result['items'][:output_amount]
    # print("Number of returns", len(result['items']))
    # print(result)
    return result

def api_address(sent, address_inp, output_amount=1):
    # start = time()
    result_list = get_address(sent, address_inp, output_amount=50)
    # print("Get address time:", time() - start)
    result = expected_output(result_list, sent, address_inp, output_amount)
    # print(result)
    return result
