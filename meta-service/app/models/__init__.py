import pymongo
from config import config

async def create_mongo_client(mongo_dbname):
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
        return db
    except Exception as e:
        print(e)
        return None

from .image import Image

__all__ = ["Image"]