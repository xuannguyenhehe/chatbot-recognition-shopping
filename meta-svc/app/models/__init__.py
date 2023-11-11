import pymongo
from loguru import logger

from .meta_clothes import MetaClothes


async def create_mongo_client(config):
    MONGO_DATABASE_URI = \
        f"mongodb://{config['MONGO_ROOT_USERNAME']}:{config['MONGO_ROOT_PASSWORD']}@{config['MONGO_HOST']}:{config['MONGO_PORT']}/?authSource=admin&readPreference=secondary&directConnection=true&ssl=false'"
    mongo_client = pymongo.MongoClient(MONGO_DATABASE_URI)
    try:
        is_live = mongo_client.admin.command('ping')
        if is_live:
            logger.info("Pinged your deployment. You successfully connected to MongoDB!")
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
        logger.error(e)
    return db




mongo_dbname = "chatbot"
__all__ = ["MetaClothes"]
