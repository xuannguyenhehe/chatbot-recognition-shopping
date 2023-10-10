from extensions.minio.connector import MinioConnector


async def create_minio_connector(config):
    storage = MinioConnector(config=config)
    return storage
