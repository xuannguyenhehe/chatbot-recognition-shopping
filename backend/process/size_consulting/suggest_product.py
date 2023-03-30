
import pymongo

client = pymongo.MongoClient("mongodb://admin:admin@chatbot-mongo-1:27017/admin")
def suggest_product(name, size, amount, check_size=False):
    '''
        Get product info from database base on name, size, amount
        output: dictionary of product detail and list of size available
    '''
    new_detail =  []
    myquery = { 'name': name }
    # mydb = models.myclient["hume_livestream"]
    mydb = client["chatbot_quangminhtien"]
    if check_size:
        data={'full_size':True}
    else:
        data = {}
        
    mycol = mydb["products"]
    myresult = mycol.find_one(myquery, {'_id':0})
    if not myresult:
        return [], ''
    detail = myresult.pop('detail')
    for key, values in detail.items():
        # for k in values.keys():
        temp = {}
        # print(k)
        # temp['color'] = key
        temp['size'] = key
        if values == 0:
            data['full_size']=False
        temp['amount'] = values
        temp["price"] = myresult['price']
        temp["product_code"] = myresult['code']
        temp["product_name"] = myresult['name']
        new_detail.append(temp)

    process_detail = []
    if size:
        for i in range(len(new_detail)):
            new_detail_item = new_detail[i]
            if 'size' in new_detail_item and new_detail_item['size']==size:
                process_detail.append(new_detail_item)

        new_detail = process_detail.copy()
    process_detail = []

    if amount:
        amount = int(amount)
        for i in range(len(new_detail)):
            new_detail_item = new_detail[i]
            if 'amount' in new_detail_item and new_detail_item['amount']>=amount:
                process_detail.append(new_detail_item)
                
        new_detail = process_detail.copy()

    data['detail'] = new_detail
    size_list = []
    for detail in new_detail:
        size_list.append(detail['size'])
    size_list = ", ".join(size_list)
    
    return data, size_list