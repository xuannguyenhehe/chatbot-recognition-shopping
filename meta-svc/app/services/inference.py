from fastapi import status

from app.schemas.inference import InferenceInput
from app.services import AppService
from app.utils.repsonse.result import ResultResponse
from extensions.milvus import MilvusConnector
from extensions.minio import MinioConnector


class InferenceService(AppService):
    def __init__ (self, storage: MinioConnector, vector_search: MilvusConnector):
        self.storage = storage
        self.vector_search = vector_search

    def get_result(self, input: InferenceInput, k: int = 5) -> ResultResponse:
        username = input.username
        path_image = input.path_image
        pseudo_colors: list = input.colors
        pseudo_category: list = input.category
        pseudo_attribute: list = input.attribute
        offset = input.offset
        results = []

        vector = None
        if path_image:
            vector = self.get_vector_prediction(path_image)["vector"][0]
            
        results = self.vector_search.query_images(
            username=username,
            pseudo_attribute=pseudo_attribute,
            pseudo_category=pseudo_category,
            pseudo_colors=pseudo_colors,
            vector=vector,
            offset=offset,
        )

        return ResultResponse((None, status.HTTP_200_OK, results))

    def get_vector_prediction(self, path_image: str):
        url = "/inference/v1/meta-inference"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return data
