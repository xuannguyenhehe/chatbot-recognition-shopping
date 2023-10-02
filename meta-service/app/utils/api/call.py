import json
from typing import Tuple
from urllib.parse import urljoin

import requests
from config import config
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

TIMEOUT = 100000000

def get_base_url(url: str) -> str:
    """Get base url according to prefix of url

    Args:
        url (str): suffix of url

    Returns:
        str: full base url
    """
    if url.startswith("/api/meta-service/v1"):
        url = url.replace("/api/meta-service/v1", "")
        base_url = urljoin(config["META_URL"], url)
    elif url.startswith("/api/rasa-service/v1"):
        url = url.replace("/api/rasa-service/v1", "")
        base_url = urljoin(config["RASA_URL"], url)
    elif url.startswith("/api/mmfashion-service/v1"):
        url = url.replace("/api/mmfashion-service/v1", "")
        base_url = urljoin(config["MMFASHION_URL"], url)
    else:
        base_url = url
    return base_url

def attemp_get_json(response):
    """
    Attemping get json data from response
    return None if failed
    """
    try:
        return response.json()
    except:
        return None


class API:
    @staticmethod
    def get(url: str, params: json = {}) -> Tuple[dict, int]:
        base_url = get_base_url(url)
        session = API.requests_retry_session()
        res = session.get(base_url, params=params, timeout=TIMEOUT)
        return_data = res.json() \
            if res.status_code == requests.codes.ok else None
        return return_data, res.status_code

    @staticmethod
    def post(
        url: str,
        data: json = {},
        get_json: bool = False
    ) -> Tuple[dict, int]:
        payload = json.dumps(data, indent=4, sort_keys=True, default=str)
        base_url = get_base_url(url)
        session = API.requests_retry_session()
        res = session.post(base_url, data=payload, timeout=TIMEOUT)

        if res.status_code == requests.codes.ok:
            return_data = res.json()
        else:
            logger.debug(
                (f"Request {base_url} failed with status code {res.status_code}, "
                 f"Response: {res.text}")
            )
            return_data = None

        if get_json:
            return_data = attemp_get_json(res)

        return return_data, res.status_code

    @staticmethod
    def put(url: str, data: json = {}):
        payload = json.dumps(data, indent=4, sort_keys=True, default=str)

        base_url = get_base_url(url)
        session = API.requests_retry_session()
        res = session.put(base_url, data=payload)
        return_data = res.json() \
            if res.status_code == requests.codes.ok else None
        return return_data, res.status_code

    @staticmethod
    def requests_retry_session(
        retries: int = 2,
        backoff_factor: float = 0.1,
        status_forcelist: tuple = (500, 502, 504),
        session=None,
    ):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        session.headers.update({'Content-Type': 'application/json'})
        # if hasattr(g, 'access_token'):
        #     session.headers.update({'Authorization': f'Bearer {g.access_token}'})
        return session
