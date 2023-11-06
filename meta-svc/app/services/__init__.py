import json
from urllib.parse import urlencode

import requests
from fastapi import status
from loguru import logger
from requests.exceptions import RequestException

from app.utils.api.call import API


class DBSessionContext(object):
    def __init__(self):
        pass


class AppService(DBSessionContext):
    @staticmethod
    def call_api(url: str, payload: dict = {}, method="post") -> dict:
        try:
            method = method.upper()
            if method == "POST":
                result, status_code = API.post(url, data=payload)
            elif method == "GET":
                result, status_code = API.get(url + "?" + urlencode(payload))
            else:
                raise ValueError(f"Unknown method {method}")

            if status_code != requests.codes.ok:
                logger.error(
                    f"[API {method}: {url} failed with status {status_code}]")  # noqa E501
                return {}, status_code
            if result == None or result["data"] == None:
                logger.error(
                    f"[API {method}: {url} failed, response data is empty, {result}"  # noqa E501
                )
                return {}, requests.codes.bad

            return result["data"], requests.codes.ok

        except RequestException as e:
            logger.error(f"[API {method}: {url} failed], {e}")  # noqa E501
            return {}, requests.codes.server_error


class AppCRUD(DBSessionContext):
    def insert(self, collection_name, data):
        try:
            if isinstance(data, list):
                self.db[collection_name].insert_many(data)
            else:
                self.db[collection_name].insert_one(data)
        except Exception as e:
            logger.error(e)
            return "Fail to insert to Database, rolled back",\
                status.HTTP_406_NOT_ACCEPTABLE
        return "Success to insert to Database", status.HTTP_200_OK

    def update(self, collection_name, query_data, update_data):
        try:
            self.db[collection_name].update_many(
                query_data,
                {
                    "$set": update_data,
                }
            )
        except Exception as e:
            logger.error(e)
            return "Fail to update to Database", status.HTTP_406_NOT_ACCEPTABLE
        return "Success to update to Database", status.HTTP_200_OK

    def delete(self, collection_name, data):
        try:
            self.db[collection_name].delete_many(data)
        except Exception as e:
            logger.error(e)
            return "Fail to delete to Database", status.HTTP_406_NOT_ACCEPTABLE
        return "Success to delete to Database", status.HTTP_200_OK

    @staticmethod
    def serialize(data) -> dict:
        return json.loads(data.json())

    def serialize_list(self, data) -> list:
        return [self.serialize(m) for m in data]
