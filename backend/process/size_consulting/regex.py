# COMMON PATTERN
product_pt = r'\b([á|a]o|qu[a|ầ]n|v[a|á]y|đầm|[d|đ]am|t[ú|u]i|n[ó|o]n|m[u|ũ]|kho[a|á]c|s[é|e]t)\b'
dd = r'(\d\d|\d)'
ss = r'(\s|\'|)'
dot = r'(\s*\.\s*|\s*,\s*|\')'
kilo = r'(k(g|y|ý|i|í|j|)|c[a|â]n|kilo|kilogam)'
nang = r'((can|)(nang|nag))'
met = r'(m|met)'
net = r'(\s*-\s*|\s*|\s*,\s*)'

# WEIGHT
pt_weight_1 = r'\b\d\d{}{}'.format(ss, kilo)  # case 43
pt_weight_2 = r'\d\d{}\d({}\d\d{}\d|{}\d\d|){}{}'.format(dot, net, dot, net, ss, kilo)  # case 43.5
pt_weight_3 = r'{}{}\d\d(\s{}|\.\d|,\d|)({}\d\d(\s\d|\.\d|,\d|)|)({}|)'.format(nang, ss, dd, net,
                                                                               kilo)  # nang 53 5, nang 50-55
pt_weight_4 = r'\d\d{}k{}cao+'.format(ss, ss)
pt_weight_5 = r'\b\d\d{}(\d\d\s*|\d\d(\s\d|\.\d|,\d|)\s*){}'.format(net, kilo)
pt_weight = r'\b((?<!(eo ))({}|{}|{}|{}|{}))\b'.format(pt_weight_1, pt_weight_2, pt_weight_3, pt_weight_4, pt_weight_5)

# HEIGHT
# 150cm, 150 cm
pt_height_1 = r'(cao+|)1\d\d{}(cm|{})'.format(ss, met)
# 1m5, 1m50, 1 m 5, 1 m 50
pt_height_2 = r'(cao+|)1{}{}{}{}'.format(ss, met, ss, dd)
# 1.5m, 1 . 5m, 1.50m, 1 . 50m
pt_height_3 = r'(cao+|)1{}{}{}{}m'.format(ss, dot, ss, dd)
# 1.50 1,5 1 . 50 1 , 5 (not kg)
pt_height_4 = r'(\b|cao+)1{}{}{}{}(?!{}{})\b'.format(ss, dot, ss, dd, ss, kilo)
# m50, m5, m 50
pt_height_5 = r'(\b|cao+){}{}{}(?!(\s*({}|cai|{})))\b'.format(met, ss, dd, product_pt, kilo)
# cao 150, 150 (nặng ...), 150 (45kg)
pt_height_6 = r'cao+{}1\d\d|1\s?\d\d\s(?=({}|{}))'.format(ss, nang, pt_weight)
# Case mot met ruoi, 1m ruoi, 1 met ruoi...
pt_height_7 = r'(mot|1|){}{}{}ruoi'.format(ss, met, ss)

pt_height = r'({}|{}|{}|{}|{}|{}|{})'.format(pt_height_1, pt_height_2,
                                             pt_height_3, pt_height_4, pt_height_5, pt_height_6, pt_height_7)

# case 1m 60 45
pt_weight_6 = r'{}\s*(\d\d){}({}|)'.format(pt_height, ss, kilo)
pt_weight_7 = r'{}\s*({})?(\d\d){}({}|)'.format(pt_height, dot, ss, kilo)
# -------------------------------------------
pt_weight_V2 = r'\b(\d\d\s*{0}\s*,\s*\d\d|\d\d\s*,\s*\d\d{0})\b'.format(kilo)

pt_height_V2_1 = r'\b(\d\d\d\s*,\s*\d\d(?!\s*{0})|\d\d\s*(?!\s*{0})\s*,\s*\d\d\d)\b'.format(kilo)
pt_height_V2_2 = r'\b(\d\d\d\s*\d\d(?!\s*{0})|\d\d(?!\s*{0})s*\d\d\d)\b'.format(kilo)

regex_lst = {
    'co_tay': '\d{2}'
}