from extensions.milvus.connector import MilvusConnector


async def create_milvus_connector(config):
    global storage
    storage = MilvusConnector(config=config)
    return storage
