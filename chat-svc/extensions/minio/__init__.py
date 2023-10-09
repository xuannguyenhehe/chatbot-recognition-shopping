from extensions.minio.connector import MinioConnector
from config import config


async def create_minio_connector():
    global storage
    storage = MinioConnector(config=config)


def get_storage():
    return storage


storage = None
__all__ = ["Message", "Image", "User", "Chat"]