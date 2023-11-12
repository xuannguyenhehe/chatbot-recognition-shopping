import sys

import requests
from loguru import logger
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)


class MilvusConnector:
    def __init__(self, config=None):
        try:
            self.collection = None
            self.config = config
            self.collection_name = "clothes"
            connections.connect(host=config['MILVUS_HOST'], port=config['MILVUS_PORT'])
            self.load_connection(self.collection_name)
            logger.debug(f"Successfully connect to Milvus with IP:{config['MILVUS_HOST']} and PORT:{config['MILVUS_PORT']}")
        except Exception as e:
            logger.error(f"Failed to connect Milvus: {e}")
            sys.exit(1)

    def load_connection(self, collection_name):
        if not self.has_collection(collection_name):
            self.create_collection(collection_name)
            self.create_index(collection_name)

        self.set_collection(collection_name)
        self.collection.load()

    def set_collection(self, collection_name):
        try:
            self.collection = Collection(name=collection_name)
        except Exception as e:
            logger.error(f"Failed to set collection in Milvus: {e}")
            sys.exit(1)

    def has_collection(self, collection_name):
        # Return if Milvus has the collection
        try:
            return utility.has_collection(collection_name)
        except Exception as e:
            logger.error(f"Failed to get collection info to Milvus: {e}")
            sys.exit(1)

    def create_collection(self, collection_name):
        # Create milvus collection if not exists
        try:
            id = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True)
            path = FieldSchema(name="path", dtype=DataType.VARCHAR, max_length=500)
            name = FieldSchema(name="name", dtype=DataType.VARCHAR, max_length=200)
            height = FieldSchema(name="height", dtype=DataType.INT32)
            width = FieldSchema(name="width", dtype=DataType.INT32)
            volume = FieldSchema(name="volume", dtype=DataType.INT32)
            username = FieldSchema(name="username", dtype=DataType.VARCHAR, max_length=200)
            label = FieldSchema(name="label", dtype=DataType.VARCHAR, max_length=200)
            vector = FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=64)
            pseudo_cate = FieldSchema(name="pseudo_cate", dtype=DataType.JSON)
            pseudo_attr = FieldSchema(name="pseudo_attr", dtype=DataType.JSON)
            pseudo_color = FieldSchema(name="pseudo_color", dtype=DataType.JSON)
            is_active = FieldSchema(name="is_active", dtype=DataType.BOOL)
            created_date = FieldSchema(name="created_date", dtype=DataType.VARCHAR, max_length=200)
            updated_date = FieldSchema(name="updated_date", dtype=DataType.VARCHAR, max_length=200)

            schema = CollectionSchema(
                fields=[
                    id, 
                    path, 
                    name, 
                    height, 
                    width, 
                    volume,
                    username, 
                    label,
                    vector,
                    pseudo_cate,
                    pseudo_attr,
                    pseudo_color,
                    is_active,
                    created_date,
                    updated_date
                ], 
                description="Vector Image Schema",
                enable_dynamic_field=True,
            )
            self.collection = Collection(name=collection_name, schema=schema)
            logger.debug(f"Create Milvus collection: {collection_name}")
            return "OK"
        except Exception as e:
            logger.error(f"Failed create collection in Milvus: {e}")
            sys.exit(1)

    def insert(self, data):
        # Batch insert vectors to milvus collection
        try:
            self.collection.insert(data)
            self.collection.flush()
            mes = f"Insert vectors to Milvus in collection: {self.collection_name} with {len(data)} rows"
            status_code = requests.codes.ok
            return mes, status_code
        except Exception as e:
            mes = logger.error(f"Failed to insert data to Milvus: {e}")
            status_code = requests.codes.bad
        return mes, status_code

    def create_index(self, collection_name):
        # Create IVF_FLAT index on milvus collection
        try:
            # self.set_collection(collection_name)
            default_index = {
                "metric_type": self.config['METRIC_TYPE'], 
                "index_type": "AUTOINDEX", 
                "params": {},
            }
            status = self.collection.create_index(field_name="vector", index_params=default_index)
            if not status.code:
                logger.debug(
                    f"Successfully create index in collection:{collection_name} with param:{default_index}")
                return status
            else:
                raise Exception(status.message)
        except Exception as e:
            logger.error(f"Failed to create index: {e}")
            sys.exit(1)

    def delete_collection(self, collection_name):
        # Delete Milvus collection
        try:
            self.set_collection(collection_name)
            self.collection.drop()
            logger.debug("Successfully drop collection!")
            return "ok"
        except Exception as e:
            logger.error(f"Failed to drop collection: {e}")
            sys.exit(1)

    def search_vectors(self, vectors, top_k):
        # Search vector in milvus collection
        try:
            search_params = {
                "metric_type": self.config['METRIC_TYPE'], 
                "params": {"nprobe": 16},
            }
            res = self.collection.search(vectors, anns_field="embedding", param=search_params, limit=top_k)
            logger.debug(f"Successfully search in collection: {res}")
            return res
        except Exception as e:
            logger.error(f"Failed to search vectors in Milvus: {e}")
            sys.exit(1)

    def get_images(self, username):
        res = self.collection.query(
            expr = f"username == '{username}'",
            offset = 0,
            limit = 10, 
            output_fields = ["id", "path", "label"],
        )
        return res
    
    def delete_all_images(self, username):
        results = self.collection.query(
            expr = f"username == '{username}'",
            offset = 0,
            output_fields = ["id", "path", "label"],
        )
        ids = [result['id'] for result in results]
        self.collection.delete(f"id in {ids}")

    def delete_images(self, ids):
        results = self.collection.query(
            expr = f"id in {ids}",
            offset = 0,
            output_fields = ["path", "label"],
        )
        exist_ids = [result['id'] for result in results]
        different_ids = list(set(ids) - set(exist_ids))
        self.collection.delete(f"id in {ids}")

        return different_ids
    
    def query_images(
            self, 
            username: str,
            pseudo_attribute: dict, 
            pseudo_category: dict, 
            pseudo_colors: dict, 
            vector: list = None,
        ):
        expr = f"username == '{username}'"
        if pseudo_attribute:
            expr += f" and json_contains_any(pseudo_attr['top 5'], {pseudo_attribute})"
        if pseudo_category:
            expr += f" and json_contains_any(pseudo_cate['top 5'], {pseudo_category})"
        if pseudo_colors:
            expr += f" and json_contains_any(pseudo_colors['top 3'], {pseudo_colors})"
        if vector:
            results = self.collection.search(
                data=[vector],
                anns_field="vector",
                param={"metric_type": "L2", "params": {"nprobe": 10}},
                limit=5,
                expr=expr,
                output_fields=["path"],
            )
            results = [hit.entity.get('path') for result in results for hit in result]
        else:
            results = self.collection.query(
                expr=expr, 
                output_fields=['path'],
            )
            results = [result["path"] for result in results]
        return results

    def count(self, collection_name):
        # Get the number of milvus collection
        try:
            self.set_collection(collection_name)
            self.collection.flush()
            num = self.collection.num_entities
            logger.debug(f"Successfully get the num:{num} of the collection:{collection_name}")
            return num
        except Exception as e:
            logger.error(f"Failed to count vectors in Milvus: {e}")
            sys.exit(1)
