import base64
import io
import os
import uuid
from typing import Tuple

from PIL import Image as PILImage

from app.models.image import Image
from app.services import AppCRUD, AppService


class ImageService(AppService):
    def __init__ (self, storage, *args, **kwargs):
        super(AppService, self).__init__(*args, **kwargs)
        self.storage = storage

    def get_image_content(self, path: str) -> io.BytesIO:
        image = self.storage.get_object_from_path(path)
        img_io = io.BytesIO(image)
        return img_io
    
    def save_image(self, image):
        print("image", image)
        # base64_image, error = self.attemp_decode(image["content"])
        # filedata = io.BytesIO(base64_image)
        # image_uuid = str(uuid.uuid4())
        # image_name = self.make_image_name(image["filename"], image_uuid)
        # image_path = save_object(
        #     self.storage,
        #     file_name=image_name,
        #     data=filedata,
        #     object_type=ObjectType.IMAGE,
        # )
        # image_width, image_height = PILImage.open(filedata).size
        # image_obj = Image(
        #     uuid=image_uuid,
        #     path=image_path,
        #     name=image_name,
        #     usage=usage,
        #     height=image_height,
        #     width=image_width,
        #     volume=sys.getsizeof(base64_image),
        #     batch_id=batch.id,
        #     user_id=user_id,
        #     meta_data=image.get("meta_data")
        # )
        return ""
    
    @staticmethod
    def attemp_decode(base64_string):
        try:
            base64_image = base64.b64decode(base64_string)
            return base64_image, None
        except Exception as e:
            return None, str(e)
        
    @staticmethod
    def make_image_name(filename, image_uuid):
        file_name, extension = os.path.splitext(filename)
        image_name = "_".join([file_name, image_uuid + extension])
        return image_name
    
class ImageCRUD(AppCRUD):
    def create(self, image: Image) -> Tuple:
        image = Image(**image.dict())
        message, status_code = self.insert("Image", self.serialize(image))
        return message, status_code

#     def get(self, username: str, name: str = None, id: int = None) -> List[Chat]:
#         query = {
#             "username": username,
#             "is_active": True,
#         }
#         if name: 
#             query.update({
#                 "name": name,
#             })
#         if id: 
#             query.update({
#                 "id": id,
#             })
#         no_query = {
#             "_id": False,
#             "is_active": False,
#             "created_date": False,
#             "updated_date": False,
#         }
#         chats = list(self.db.Chat.find(query, no_query))
#         return chats
