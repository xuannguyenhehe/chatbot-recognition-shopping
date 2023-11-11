from extensions.minio.connector import MinioConnector
from settings import config


async def create_minio_connector():
    storage = MinioConnector(config=config)
    return storage
