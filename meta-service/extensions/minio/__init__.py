from extensions.minio.connector import MinioConnector
from config import config


async def create_minio_connector():
    global storage
    storage = MinioConnector(config=config)
    return storage