import minio
import pymongo
import pandas as pd
import sys
import os
from urllib import parse
import uuid
from PIL import Image as PILImage
import datetime
from io import BytesIO
import base64
import numpy as np
import cv2
from enum import Enum


MONGO_ROOT_USERNAME="admin"
MONGO_ROOT_PASSWORD="admin"
MINIO_REGION=''
MONGO_PORT=27017
MONGO_HOST="127.0.0.1"
MONGO_AUTH_DATABASE="admin"
MINIO_ROOT_USER="minioadmin"
MINIO_ROOT_PASSWORD="minioadmin"
ADMIN_MINIO_URL="http://192.168.1.2178:9099"
MINIO_BUCKETS="rasa-service,meta-service"
MINIO_SECURE=False
MINIO_HTTP_CLIENT=None

def pil_to_base64(image):
    image = image.convert("RGB")
    img = np.array(image)[:,:,::-1]
    _, buf = cv2.imencode(".jpg", img)
    return base64.b64encode(buf)

class ObjectType(str, Enum):
    IMAGE = "images"
    CHECKPOINT = "checkpoints"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ObjectType))

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

def make_dirname():
    """
    Create dir name with format yyyy/mm/dd
    of current time
    """
    now = datetime.datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    return os.path.join(year, month, day)

def put_object(
        data,
        bucket_name: str,
        object_name: str,
        metadata = None,
        sse: str = None,
        part_size: int = 10*1024*1024,
        tags: str = None,
        retention = None,
        length: int = -1,
    ):
        """Put object to bucket.

        Args:
            data (Any): source data
            bucket_name (str): bucket name
            object_name (str): object name
            metadata (Any, optional): Metadata. Defaults to None.
            sse (str, optional): SseCustomerKey. Defaults to None.
            part_size (int, optional): Limit part size for multipart upload. Defaults to 10MB.
            tags (str, optional): tags of object. Defaults to None.
            retention (Retention, optional): Retention object data. Defaults to None.
            length (int, optional): Limit  length file. Defaults to -1.
            
        Returns:
            tuple: bucket name, etag, version_id
        """
        result = mc.put_object(
            data=data,
            bucket_name=bucket_name,
            object_name=object_name,
            sse=sse,
            metadata=metadata,
            part_size=part_size,
            tags=tags,
            retention=retention,
            length=length,
        )
        return result.object_name, result.etag, result.version_id

def save_object(
    file_name,
    data,
    object_type,
    label,
    name_date,
    bucket_name=None
):
    """ Save object to storage with path
        bucket_name/object_type/yyyy/mm/dd/file_name
    Args:
        file_name (str): file name
        data (bytes): bytestring data
        object_type (str): images or checkpoints
        bucket_name (str): name of bucket if not given, use default_bucket

    Returns:
        str: object name with full path
    """
    if bucket_name is None:
        bucket_name = "meta-service"

    # check object type
    if not ObjectType.has_value(object_type):
        raise ValueError(f"expect object_type to be one of {ObjectType.list()}, got {object_type}")

    if not mc.bucket_exists(bucket_name):
        raise FileNotFoundError(f"bucket {bucket_name} does not exist")

    object_name = os.path.join(object_type, label, name_date, file_name)

    put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=data,
    )
    full_path = os.path.join(bucket_name, object_name)
    return full_path

db = pymongo.MongoClient(f"mongodb://{MONGO_ROOT_USERNAME}:{MONGO_ROOT_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin&readPreference=secondary&directConnection=true&ssl=false'")
is_alive = db.admin.command('ping')
if is_alive:
    print("Pinged your deployment. You successfully connected to MongoDB!")
else:
    raise "DB not alive"

_pre_config = {
    "endpoint": parse.urlsplit(ADMIN_MINIO_URL).netloc,
    "secure": MINIO_SECURE,
    "region": MINIO_REGION,
    "http_client": MINIO_HTTP_CLIENT,
}
mc = minio.Minio(
    access_key=MINIO_ROOT_USER,
    secret_key=MINIO_ROOT_PASSWORD,
    **_pre_config,
)
is_alive = mc.list_buckets()
if isinstance(is_alive, list):
    print("Pinged your deployment. You successfully connected to Minio!")
else:
    raise "Minio not alive"

path = sys.argv[1]
is_exist = os.path.exists(path)
if is_exist:
    files = os.listdir(path)
    csv_files = list(filter(lambda file: file.endswith(".csv"), files))
    if len(csv_files) > 0:
        csv_path = os.path.join(path, csv_files[0])
        df = pd.read_csv(csv_path, delimiter=';', index_col=0)
        for index_row, value_row in df.iterrows():
            real_path_image = path + value_row["path"]
            is_exist_image = os.path.exists(real_path_image)
            if not is_exist_image:
                print(f"Need to dump image {real_path_image} by hand")
                break
            PILImage = PILImage.open(real_path_image)
            usage = value_row["usage"]
            height = value_row["height"]
            width = value_row["width"]
            label = value_row["label"]
            name = value_row["name"]
            index_label = index_row // 5
            index_image_in_label = index_row % 5
            uuid_str = str(uuid.uuid4())
            name_date = make_dirname()
            minio_path_image = os.path.join("meta-service", 'image', label, name_date, name)
            file_data = BytesIO(base64.b64decode(pil_to_base64(PILImage)))

            # Save image to minio
            image_path = save_object(
                file_name=name,
                data=file_data,
                object_type=ObjectType.IMAGE,
                label=label,
                name_date=name_date,
            )
            volume = sys.getsizeof(file_data)

            mydict = {
                "uuid": uuid_str,
                "path": minio_path_image,
                "height": height,
                "width": width,
                "volume": volume,
                "usage": usage,
                "label": label,
                "index_label": index_label,
                "index_image_in_label": index_image_in_label,
                "is_active": True,
                "created_date": datetime.datetime.now(),
                "updated_date": datetime.datetime.now(),
            }
            dbchatbot = db["chatbot"]
            col = dbchatbot["Image"]
            col.insert_one(mydict)
    else:
        raise "No exist csv file to dump image"
else:
    raise "No exist directory to dump image"
