import pymongo

async def create_mongo_client(config):
    mongo_client = pymongo.MongoClient(config["MONGO_DATABASE_URI"])
    try:
        is_live = mongo_client.admin.command('ping')
        if is_live:
            print("Pinged your deployment. You successfully connected to MongoDB!")
        else:
            raise
        db = mongo_client[mongo_dbname]
        collection_list = db.list_collection_names()
        for collection in __all__:
            if collection not in collection_list:
                test_col = db[collection]
                test_dict = {"test": "test"}
                test_col.insert_one(test_dict)
                test_col.delete_one(test_dict)
    except Exception as e:
        print(e)
    return db


from .chat import Chat
from .image import Image
from .message import Message


mongo_dbname = "chatbot"
__all__ = ["Chat", "Image", "Message"]