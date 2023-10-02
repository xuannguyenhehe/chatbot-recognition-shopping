import io
import base64
import uuid
import os
from PIL import Image as PILImage
from app.services import AppService, AppCRUD
from app.models.image import Image
from typing import Tuple

# class ImageService():
#     def __init__ (self, storage):
#         self.storage = storage

#     def get_image_content(self, path: str):
#         image = get_object_from_path(self.storage, path)
#         img_io = io.BytesIO(image)
#         return img_io
    
#     def save_image(self, image):
#         base64_image, error = self.attemp_decode(image["content"])
#         filedata = io.BytesIO(base64_image)
#         image_uuid = str(uuid.uuid4())
#         image_name = self.make_image_name(image["filename"], image_uuid)
#         image_path = save_object(
#             self.storage,
#             file_name=image_name,
#             data=filedata,
#             object_type=ObjectType.IMAGE,
#         )
#         image_width, image_height = PILImage.open(filedata).size
#         image_obj = Image(
#             uuid=image_uuid,
#             path=image_path,
#             name=image_name,
#             usage=usage,
#             height=image_height,
#             width=image_width,
#             volume=sys.getsizeof(base64_image),
#             batch_id=batch.id,
#             user_id=user_id,
#             meta_data=image.get("meta_data")
#         )
    
#     @staticmethod
#     def attemp_decode(base64_string):
#         try:
#             base64_image = base64.b64decode(base64_string)
#             return base64_image, None
#         except Exception as e:
#             return None, str(e)
        
#     @staticmethod
#     def make_image_name(filename, image_uuid):
#         file_name, extension = os.path.splitext(filename)
#         image_name = "_".join([file_name, image_uuid + extension])
#         return image_name

class ImageCRUD(AppCRUD):
    def create(self, image: Image) -> Tuple:
        image = Image(**image.dict())
        message, status_code = self.insert("Image", self.serialize(image))
        return message, status_code

    def get_by_index(self, index_label: int, index_image_in_label: int) -> str:
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
    
    def query_by_cate_attr_color(self, cate: list, attr: list, color: list, k: int) -> list:
        query_data = []
        if len(cate):
            query_data.append({
                "pseudo_cate.top 5": {
                    "$in": cate,
                },
            })
        if len(attr):
            query_data.append({
                "pseudo_attr.top 10": {
                    "$in": attr,
                },
            })
        if len(color):
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