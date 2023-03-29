import logging
from ..constants import LOGGING_NAME

def set_logging(name :str = LOGGING_NAME):
    # sets up logging for the given name
    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            name: {
                "format": "%(asctime)s %(levelname)s %(message)s"
            }},
    })

