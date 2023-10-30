import os
from datetime import datetime


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
