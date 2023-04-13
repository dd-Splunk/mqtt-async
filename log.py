import logging
from os import environ as env

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


def set_log():
    log_level = env.get("LOG_LEVEL", "INFO").upper()
    print(log_level)
    log_format = "%(asctime)s %(levelname)s %(funcName)s %(message)s"
    logging.basicConfig(level=log_level, format=log_format)
