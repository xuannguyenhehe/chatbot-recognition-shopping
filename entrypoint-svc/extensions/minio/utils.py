import os
from enum import Enum
from datetime import datetime
from typing import Tuple
from minio.commonconfig import CopySource

from extensions.minio import storage

# HARD CORE, move this to db or somewhere else for multi-tenant
DEFAULT_BUCKET = "tessel-nutifood"

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
    now = datetime.now()
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    return os.path.join(year, month, day)


def save_object(
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
        bucket_name = DEFAULT_BUCKET

    # check object type
    if not ObjectType.has_value(object_type):
        raise ValueError(f"expect object_type to be one of {ObjectType.list()}, got {object_type}")

    if not storage.client.bucket_exists(bucket_name):
        raise FileNotFoundError(f"bucket {bucket_name} does not exist")

    object_name = os.path.join(object_type, make_dirname(), file_name)

    storage.put_object(
        bucket_name=bucket_name,
        object_name=object_name,
        data=data,
    )
    full_path = os.path.join(bucket_name, object_name)
    return full_path


def split_bucket_path(path):
    """Split full path (bucket name + object name)
    to bucket name + object name

    Args:
        path (str): full path (bucket name + object name)

    Returns:
        Tuple[str, str]: bucket name, object name
    """
    path = os.path.normpath(path)
    bucket_name = path.split(os.path.sep)[0]
    object_name = os.path.relpath(path, bucket_name)
    return bucket_name, object_name


def download_objects(ls_path: list, save_dir: str = None):
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
        obj = storage.get_object(bucket_name, object_name)
        if obj is not None:
            objs.append(obj)

            if save_dir:
                head_tail = os.path.split(object_name)
                tail_object_name = head_tail[1]
                tmp_file_name = os.path.join(save_dir, tail_object_name)
                with open(tmp_file_name, "wb") as fh:
                    fh.write(obj)
    return objs


def get_object_from_path(path):
    """Convenience for getting object from path"""
    bucket_name, object_name = split_bucket_path(path)
    obj = storage.get_object(bucket_name, object_name)
    return obj


def copy_object(src, dst):
    old_bucket, old_object = split_bucket_path(src)
    new_bucket, new_object = split_bucket_path(dst)
    if (
        not storage.client.bucket_exists(old_bucket)
        or not storage.client.bucket_exists(new_bucket)
    ):
        return False
    try:
        storage.client.copy_object(
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


def path_exists(path):
    bucket, object_name = split_bucket_path(path)
    return storage.object_exists(bucket, object_name)
