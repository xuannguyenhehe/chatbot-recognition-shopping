from typing import List, Union
from urllib import parse

from minio.versioningconfig import VersioningConfig, ENABLED
from minio.error import S3Error

from flask import current_app

import minio


class MinioConnector():
    def __init__(self, app=None):
        self.client = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("MINIO_SECURE", True)
        app.config.setdefault("MINIO_REGION", None)
        app.config.setdefault("MINIO_HTTP_CLIENT", None)
        self.client = self.connect(app)

    def connect(self, app):
        _pre_config = {
            "endpoint": parse.urlsplit(app.config["ADMIN_MINIO_URL"]).netloc,
            "secure": app.config["MINIO_SECURE"],
            "region": app.config["MINIO_REGION"],
            "http_client": app.config["MINIO_HTTP_CLIENT"],
        }

        if app.config["MINIO_ROOT_USER"] and app.config["MINIO_ROOT_PASSWORD"]:
            return minio.Minio(
                access_key=app.config["MINIO_ROOT_USER"],
                secret_key=app.config["MINIO_ROOT_PASSWORD"],
                **_pre_config,
            )
        elif app.config["MINIO_ACCESS_KEY"] and app.config["MINIO_SECRET_KEY"]:
            return minio.Minio(
                access_key=app.config["MINIO_ACCESS_KEY"],
                secret_key=app.config["MINIO_SECRET_KEY"],
                **_pre_config,
            )
        raise ConnectionError("Config Minio is not matching on this platform")

    def init_bucket(self, buckets: list):
        """ Initialize some buckets if they not exist.

        Args:
            buckets (list): the list of buckets to initialize.
        """
        buckets = buckets or current_app.config["MINIO_BUCKETS"]
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
            current_app.logger.error(e)
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
