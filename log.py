import logging
import os

from dotenv import load_dotenv


def set_log():
    load_dotenv()  # take environment variables from .env.

    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    log_format = "%(asctime)s %(levelname)s %(funcName)s %(message)s"
    logging.basicConfig(level=log_level, format=log_format)
