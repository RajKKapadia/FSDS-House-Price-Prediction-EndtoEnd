import os
import traceback
import logging
logger = logging.getLogger(__name__)

from house_price.entity.entity_config import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelEvaluationConfig, ModelTrainingConfig, PushModelConfig
from house_price.util import util
from house_price import constant

class Configuration:

    def __init__(
        self,
        config_file_path = constant.CONFIG_FILE_PATH,
        current_timestamp = constant.CURRENT_TIMESTAMP
    ) -> None:
        try:
            self.config_info = util.read_yaml_file(file_path=config_file_path)
            self.current_timestamp = current_timestamp
        except:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        data_ingestion_config = self.config_info[constant.DATA_INGESTION_CONFIG_KEY]
        dataset_download_url = data_ingestion_config['dataset_download_url']
        data_ingestion_base_path = os.path.join(
            constant.ARTIFACT_DIR_PATH,
            constant.DATA_INGESTION_DIR,
            self.current_timestamp
        )
        raw_data_path = os.path.join(
            data_ingestion_base_path,
            data_ingestion_config['raw_data_path']
        )
        downloaded_zip_file_path = os.path.join(
            data_ingestion_base_path,
            data_ingestion_config['downloaded_zip_file_path']
        )
        ingested_dir = os.path.join(
            data_ingestion_base_path,
            data_ingestion_config['ingested_dir']
        )
        train_data_dir = os.path.join(
            ingested_dir,
            data_ingestion_config['train_data_dir']
        )
        test_data_dir = os.path.join(
            ingested_dir,
            data_ingestion_config['test_data_dir']
        )
        data_ingestion_config = DataIngestionConfig(
            dataset_download_url=dataset_download_url,
            raw_data_path=raw_data_path,
            downloaded_zip_file_path=downloaded_zip_file_path,
            ingested_dir=ingested_dir,
            train_data_dir=train_data_dir,
            test_data_dir=test_data_dir
        )
        
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        pass

    def get_data_transformation_config(self) -> DataTransformationConfig:
        pass

    def get_model_training_config(Self) -> ModelTrainingConfig:
        pass

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_push_model_config(self) -> PushModelConfig:
        pass