import os
from enum import Enum
from typing import List, Union
from urllib import parse

import minio
from extensions.minio.utils import make_dirname, split_bucket_path
from loguru import logger
from minio.commonconfig import CopySource
from minio.error import S3Error
from minio.versioningconfig import ENABLED, VersioningConfig


class ObjectType(str, Enum):
    IMAGE = "images"
    CHECKPOINT = "checkpoints"

    @staticmethod
    def list():
        return list(map(lambda c: c.value, ObjectType))

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

class MinioConnector():
    def __init__(self, config=None):
        self.client = None
        self.init_app(config)
        self.default_bucket = config["DEFAULT_BUCKET"]
        self.init_bucket(config=config)

    def init_app(self, config):
        config.setdefault("MINIO_SECURE", True)
        config.setdefault("MINIO_REGION", None)
        config.setdefault("MINIO_HTTP_CLIENT", None)
        self.client = self.connect(config)

    def connect(self, config):
        _pre_config = {
            "endpoint": parse.urlsplit(config["ADMIN_MINIO_URL"]).netloc,
            "secure": config["MINIO_SECURE"],
            "region": config["MINIO_REGION"],
            "http_client": config["MINIO_HTTP_CLIENT"],
        }

        if config["MINIO_ROOT_USER"] and config["MINIO_ROOT_PASSWORD"]:
            return minio.Minio(
                access_key=config["MINIO_ROOT_USER"],
                secret_key=config["MINIO_ROOT_PASSWORD"],
                **_pre_config,
            )
        elif config["MINIO_ACCESS_KEY"] and config["MINIO_SECRET_KEY"]:
            return minio.Minio(
                access_key=config["MINIO_ACCESS_KEY"],
                secret_key=config["MINIO_SECRET_KEY"],
                **_pre_config,
            )
        raise ConnectionError("Config Minio is not matching on this platform")

    def init_bucket(self, buckets: list = [], config = None):
        """ Initialize some buckets if they not exist.

        Args:
            buckets (list): the list of buckets to initialize.
        """
        buckets = buckets or config["MINIO_BUCKETS"].split(',')
        for bucket in buckets:
            bucket = bucket.lower()
            if not self.client.bucket_exists(bucket):
                self.client.make_bucket(bucket, object_lock=True)
                self.client.set_bucket_versioning(bucket, VersioningConfig(ENABLED))

    def object_exists(self, bucket_name: str, object_name: str) -> bool:
        """Check whether a file name (prefix + file_name) exists 
            before saving in MinIO

        Args:
            bucket_name (str): name of exist bucket
            object_name (str): prefix + file_name

        Returns:
            bool: whether file name exist and vice versa
        """
        try:
            self.client.stat_object(
                bucket_name=bucket_name,
                object_name=object_name,
            )
            return True
        except S3Error:
            False

    def get_object(self, bucket_name: str, object_name: str) -> Union[bytes, None]:
        """Return bytestring of object (image or checkpoint)

        Args:
            bucket_name (str): name of exist bucket
            object_name (str): prefix + filename

        Returns:
            bytes: bytestring of object
        """
        response = None
        try:
            response = self.client.get_object(bucket_name, object_name)
            return response.data or None
        except S3Error as e:
            logger.error(e)
            return None
        finally:
            if response is not None: 
                response.close()
                response.release_conn()

    def put_object(
        self,
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
        result = self.client.put_object(
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

    def list_objects(
        self,
        bucket_name: str,
        prefix: str,
        recursive: bool = True,
    ) -> List:
        """List all objects

        Args:
            bucket_name (str): bucket name.
            prefix (str): prefix path to list objects
            recursive (bool, optional): recursive to all folder. Defaults to True.

        Returns:
            List: list objects
        """
        return self.client.list_objects(
            bucket_name,
            prefix,
            recursive,
        )
    
    def save_object(
        self,
        file_name,
        data,
        object_type,
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
            bucket_name = self.default_bucket

        # check object type
        if not ObjectType.has_value(object_type):
            raise ValueError(f"expect object_type to be one of {ObjectType.list()}, got {object_type}")

        if not self.client.bucket_exists(bucket_name):
            raise FileNotFoundError(f"bucket {bucket_name} does not exist")

        object_name = os.path.join(object_type, make_dirname(), file_name)

        self.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=data,
        )
        full_path = os.path.join(bucket_name, object_name)
        return full_path
    
    def download_objects(self, ls_path: list, save_dir: str = None):
        """Create temporary directory for all objects belong to save_dir
        by list of path of objects

        Args:
            ls_path (list): list of path of objects
            save_dir (str): directory to save objects if given
        Returns:
            List of byte objects
        """
        if save_dir and not os.path.exists(save_dir):
            os.mkdir(save_dir)

        objs = []
        for path in ls_path:
            bucket_name, object_name = split_bucket_path(path)
            obj = self.get_object(bucket_name, object_name)
            if obj is not None:
                objs.append(obj)

                if save_dir:
                    head_tail = os.path.split(object_name)
                    tail_object_name = head_tail[1]
                    tmp_file_name = os.path.join(save_dir, tail_object_name)
                    with open(tmp_file_name, "wb") as fh:
                        fh.write(obj)
        return objs

    def get_object_from_path(self, path):
        """Convenience for getting object from path"""
        bucket_name, object_name = split_bucket_path(path)
        obj = self.get_object(bucket_name, object_name)
        return obj
    
    
    def copy_object(self, src, dst):
        old_bucket, old_object = split_bucket_path(src)
        new_bucket, new_object = split_bucket_path(dst)
        if (
            not self.client.bucket_exists(old_bucket)
            or not self.client.bucket_exists(new_bucket)
        ):
            return False
        try:
            self.client.copy_object(
                new_bucket,
                new_object,
                CopySource(
                    old_bucket,
                    old_object
                ))
            return True
        except Exception as e:
            print(e)
            return False


    def path_exists(self, path):
        bucket, object_name = split_bucket_path(path)
        return self.object_exists(bucket, object_name)