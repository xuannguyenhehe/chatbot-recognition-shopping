import base64
import io
import os
import sys
import uuid
from typing import List

import requests
from PIL import Image as PILImage

from app.models.image import ImageVector
from app.services import AppService
from app.utils.repsonse.result import ResultResponse
from extensions.milvus.connector import MilvusConnector
from extensions.minio.connector import MinioConnector, ObjectType


class ImageService(AppService):
    def __init__ (self, vector_search: MilvusConnector, storage: MinioConnector):
        self.storage = storage
        self.vector_search = vector_search

    def add_images(self, username: str, images: dict):
        image_objs = []
        for label, image_files in images.items():
            self.vector_search.delete_all_images(username)
            for image in image_files:
                base64_image, _ = self.attemp_decode(image["content"])
                filedata = io.BytesIO(base64_image)
                image_uuid = str(uuid.uuid4())
                image_name = self.make_image_name(image["filename"], image_uuid)
                image_path = self.storage.save_object(
                    file_name=image_name,
                    data=filedata,
                    object_type=ObjectType.IMAGE,
                )

                category_attribute_image = self.get_category_attribute_prediction(image_path)
                attribute_image = category_attribute_image['attr']
                category_image = category_attribute_image['cate']
                color_image = self.get_color_image(image_path)

                vector_image = self.get_vector_prediction(image_path)["vector"][0]

                image_width, image_height = PILImage.open(filedata).size
                image_obj = ImageVector(
                    path=image_path,
                    name=image_name,
                    height=image_height,
                    width=image_width,
                    volume=sys.getsizeof(base64_image),
                    username=username,
                    label=label,
                    vector=vector_image,
                    meta_data=image.get("meta_data"),
                    pseudo_cate=category_image,
                    pseudo_attr=attribute_image,
                    pseudo_color=color_image,
                ).__dict__
                image_objs.append(image_obj)

        message, status_code = self.vector_search.insert(image_objs)
        return ResultResponse((message, status_code))
    

    def get_images(self, username):
        results = {}
        images = self.vector_search.get_images(username)
        for image in images:
            if image['label'] not in results:
                results[image['label']] = [image['path']]
            else:
                results[image['label']].append(image['path'])
        
        results = [{"label": label, "urls": urls} for label, urls in results.items()]

        return ResultResponse(("Get full image urls success", requests.codes.ok, results))
        

    @staticmethod
    def make_image_name(filename, image_uuid):
        file_name, extension = os.path.splitext(filename)
        image_name = "_".join([file_name, image_uuid + extension])
        return image_name
    
    @staticmethod
    def attemp_decode(base64_string):
        """
        Attemping decode base64 string

        Args:
            - base64_string: base64 string

        Returns:
            - Tuple(base64_image, error_msg)
        """
        try:
            base64_image = base64.b64decode(base64_string)
            return base64_image, None
        except Exception as e:
            return None, str(e)
        
    def get_vector_prediction(self, path_image: str):
        url = "/inference/v1/meta-inference"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return data

    def get_category_attribute_prediction(self, path_image: str):
        url = "/inference/v1/category-attribute-inference"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return data
    
    def get_color_image(self, path_image: str) -> List[str]:
        url = "/inference/v1/color-inference"
        payload = {
            "path_image": path_image,
        }
        data, _ = self.call_api(url, payload, "post")
        return {"top 3": data}
