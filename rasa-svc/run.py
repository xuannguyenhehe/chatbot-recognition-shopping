import logging
import os

import uvicorn
from app import create_app

if __name__ == "__main__":
    ENVIRONMENT_DEBUG = os.environ.get("APP_DEBUG")
    ENVIRONMENT_PORT = os.environ.get("APP_PORT")
    ENVIRONMENT_HOST = os.environ.get("APP_HOST")
    uvicorn.run(
        "run:create_app",
        port=8005,
    )
else:
    gunicorn_app = create_app()
    gunicorn_logger = logging.getLogger('gunicorn.error')