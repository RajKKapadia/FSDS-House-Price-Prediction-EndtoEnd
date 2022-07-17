import logging
from datetime import datetime
import os

LOG_DIR = 'app_logs'

TIMESTAMP = f'{datetime.now().strftime("%H-%M_%Y-%m-%d")}'

FILE_NAME = f'logs_{TIMESTAMP}.log'

os.makedirs(LOG_DIR, exist_ok=True)

FILE_PATH = os.path.join(LOG_DIR, FILE_NAME)

logging.basicConfig(
    filename=FILE_PATH,
    filemode='w',
    format='[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)