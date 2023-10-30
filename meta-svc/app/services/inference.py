
import numpy as np
import torch
from fastapi import status

from app.schemas.inference import InferenceInput
from app.services import AppService
from app.services.image import ImageCRUD
from app.utils.repsonse.result import ResultResponse
from extensions.minio import MinioConnector


class InferenceService(AppService):
    def __init__ (self, config, storage: MinioConnector, vector_search, db):
        self.config = config
        self.storage = storage
        self.vector_search = vector_search
        self.db = db

    def get_result(self, input: InferenceInput, k: int = 5) -> ResultResponse:
        path_image = input.path_image
        colors = input.colors
        category = input.category
        attribute = input.attribute
        results = []

        if path_image:
            vector_image = self.get_vector_prediction(path_image)["vector"]
            dist = torch.pow(self.vector_search - vector_image, 2).sum(dim=2)
            dist_shape = dist.shape

            query_old = 0
            query_new = k
            while len(results) < 5:
                _, i = torch.topk(dist.flatten(), query_new, largest=False)
                topk_positions = np.array(np.unravel_index(i.numpy(), dist.shape)).T
                for num_1, num_2 in topk_positions[:-(query_new - query_old)]:
                    full_index = num_1 * dist_shape[1] + num_2
                    index_label = full_index // dist_shape[0]
                    index_image_in_label = full_index % dist_shape[0]
                    query_result = ImageCRUD(self.db).get_by_index(
                        index_label=index_label, 
                        index_image_in_label=index_image_in_label,
                        cate=category,
                        attr=attribute,
                        color=colors,
                    )
                    path_image, cate_image, attr_image, color_image = query_result
                    common_cate = set(category["top 5"]).intersection(cate_image["top 5"])
                    common_attr = set(attribute["top 10"]).intersection(attr_image["top 10"])
                    common_color = set(colors).intersection(color_image)
                    if len(common_cate) > 0 and len(common_attr) > 0 and len(common_color) > 0:
                        results.append(path_image)
                query_old += query_new
                query_new += (k - len(results))
        else:
            images = ImageCRUD(self.db).query_by_cate_attr_color(
                cate=category,
                attr=attribute,
                color=colors,
                k=k,
            )
            results = [image["path"] for image in images]

        return ResultResponse((None, status.HTTP_200_OK, results))

    def get_vector_prediction(self, path_image: str):
        url = "/inference/v1/meta-inference"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return data
