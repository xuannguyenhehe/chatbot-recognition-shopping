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

