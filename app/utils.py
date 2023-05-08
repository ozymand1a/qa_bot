import logging
from pathlib import Path


def get_logger(name):
    logger = logging.getLogger(name)  # todo: move out to utils
    return logger


def get_data_path() -> Path:
    return Path(__file__).parent / 'data'
