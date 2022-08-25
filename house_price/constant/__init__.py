import os
from datetime import datetime

ROOT_DIR = os.getcwd()

LOG_DIR = 'app_logs'
LOG_DIR_PATH = os.path.join(ROOT_DIR, LOG_DIR)

CONFIG_DIR = 'config'
CONFIG_FILE_NAME = 'config.yaml'
CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, CONFIG_FILE_NAME)

CURRENT_TIMESTAMP = f'{datetime.now().strftime("%Y-%m-%d_%H-%M")}'

DATASET_DIR = 'house_price_prediction'
ARTIFACT_DIR = 'artifact'
ARTIFACT_DIR_PATH = os.path.join(ROOT_DIR, DATASET_DIR, ARTIFACT_DIR)

DATA_INGESTION_CONFIG_KEY = 'data_ingestion_config'
DATA_INGESTION_DIR = 'data_ingestion'

DATA_VALIDATION_CONFIG_KEY = 'data_validation_config'
DATA_VALIDATION_DIR = 'data_validation'

DATA_TRANSFORMATION_CONFIG_KEY = 'data_transformation_config'
DATA_TRANSFORMATION_DIR = 'data_transformation'

MODEL_TRAINING_CONFIG_KEY = 'model_training_config'
MODEL_TRIAINNG_DIR = 'model_training'

MODEL_EVALUATION_CONFIG_KEY = 'model_evaluation_config'
MODEL_EVALUATION_DIR = 'model_evaluation'
