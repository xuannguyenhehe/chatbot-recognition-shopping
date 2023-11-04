import base64
import io
import os
import pickle
import sys
import uuid
from typing import List, Tuple

import requests
import torch
from PIL import Image as PILImage

from app.models.image import Image
from app.models.vector import Vector
from app.services import AppCRUD, AppService
from app.services.vector import VectorCRUD
from app.utils.repsonse.result import ResultResponse
from extensions.minio.connector import MinioConnector, ObjectType


class ImageService(AppService):
    def __init__ (self, db, storage: MinioConnector):
        super().__init__(db=db)
        self.storage = storage

    def add_images(self, username: str, images: dict):
        image_objs = []
        vector_images = []
        for label, image_files in images.items():
            ImageCRUD(self.db).delete_by_label(label)
            for image in image_files:
                base64_image, error = self.attemp_decode(image["content"])
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

                vector_image = torch.tensor(self.get_vector_prediction(image_path)["vector"])
                vector_images.append(vector_image)

                image_width, image_height = PILImage.open(filedata).size
                image_obj = Image(
                    uuid=image_uuid,
                    path=image_path,
                    name=image_name,
                    height=image_height,
                    width=image_width,
                    volume=sys.getsizeof(base64_image),
                    username=username,
                    label=label,
                    meta_data=image.get("meta_data"),
                    pseudo_cate=category_image,
                    pseudo_attr=attribute_image,
                    pseudo_color=color_image,
                )
                image_objs.append(image_obj)

        vector_images = torch.cat(vector_images, dim=0)
        serialized_vectors = pickle.dumps(vector_images)
        vector_path = self.storage.save_object(
            file_name=f"vector_{username}.bin",
            data=io.BytesIO(serialized_vectors),
            object_type=ObjectType.VECTOR,
        )
        vector_obj = Vector(
            path=vector_path,
            username=username,
        )
        message, status_code = VectorCRUD(self.db).create(vector_obj)

        message, status_code = ImageCRUD(self.db).create(image_objs)
        return ResultResponse((message, status_code))
    

    def get_images(self, username):
        results = {}
        images = ImageCRUD(self.db).get_by_username(username)
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
        return data
        

class ImageCRUD(AppCRUD):
    def create(self, images: List[Image]) -> Tuple:
        images = [Image(**image.dict()) for image in images]
        message, status_code = self.insert("Image", self.serialize_list(images))
        return message, status_code
    
    def get_by_username(self, username: str):
        query = {
            "username": username,
        }
        no_query = {
            "_id": False,
            "is_active": False,
            "created_date": False,
            "updated_date": False,
        }
        images = list(self.db.Image.find(query, no_query))
        return images

    def delete_by_label(self, label: str):
        query = {
            "label": label,
        }
        self.db.Image.delete_many(query)


    def get_by_index(
            self, 
            index_label: int, 
            index_image_in_label: int,
            cate: str, 
            attr: str, 
            color: list, 

        ) -> str:
        query = {
            "index_label": int(index_label),
            "index_image_in_label": int(index_image_in_label),
        }
        path_image = None
        images = list(self.db.Image.find(query))
        if len(images) > 0:
            path_image = images[0]["path"]
            cate_image = images[0]["pseudo_cate"]
            attr_image = images[0]["pseudo_attr"]
            color_image = images[0]["pseudo_color"]
        return path_image, cate_image, attr_image, color_image
    
    def query_by_cate_attr_color(
            self, 
            cate: str, 
            attr: str, 
            color: list, 
            k: int,
        ) -> list:
        query_data = []
        if cate:
            query_data.append({
                "pseudo_cate.top 5": {
                    "$in": [cate],
                },
            })
        if attr:
            query_data.append({
                "pseudo_attr.top 10": {
                    "$in": [attr],
                },
            })
        if color and len(color):
            query_data.append({
                "pseudo_color": {
                    "$in": color,
                },
            })
        images = []
        if len(query_data) > 0:
            images = list(self.db.Image.find({
                "$and": query_data
            }).limit(k))
        return images
