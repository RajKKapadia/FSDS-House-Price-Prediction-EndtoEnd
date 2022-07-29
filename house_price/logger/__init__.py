import logging
from datetime import datetime
import os

from house_price import constant

LOG_DIR_PATH = constant.LOG_DIR_PATH

os.makedirs(LOG_DIR_PATH, exist_ok=True)

TIMESTAMP = constant.CURRENT_TIMESTAMP

FILE_NAME = f'logs_{TIMESTAMP}.log'

FILE_PATH = os.path.join(LOG_DIR_PATH, FILE_NAME)

logging.basicConfig(
    filename=FILE_PATH,
    filemode='w',
    format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)