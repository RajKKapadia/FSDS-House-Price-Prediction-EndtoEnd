import os
import traceback

from house_price.entity.entity_config import DataIngestionConfig, DataTransformationConfig, DataValidationConfig, ModelEvaluationConfig, ModelTrainingConfig, PushModelConfig
from house_price.util import util
from house_price import constant
from house_price.logger import logging
logger = logging.getLogger(__name__)

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
        train_data_file_name = data_ingestion_config['train_data_file_name']
        test_data_file_name = data_ingestion_config['test_data_file_name']
        data_ingestion_config = DataIngestionConfig(
            dataset_download_url=dataset_download_url,
            raw_data_path=raw_data_path,
            downloaded_zip_file_path=downloaded_zip_file_path,
            ingested_dir=ingested_dir,
            train_data_dir=train_data_dir,
            train_data_file_name=train_data_file_name,
            test_data_dir=test_data_dir,
            test_data_file_name=test_data_file_name
        )
        
        return data_ingestion_config

    def get_data_validation_config(self) -> DataValidationConfig:
        data_validation_config = self.config_info[constant.DATA_VALIDATION_CONFIG_KEY]
        data_validation_base_path = os.path.join(
            constant.ARTIFACT_DIR_PATH,
            constant.DATA_VALIDATION_DIR,
            self.current_timestamp
        )
        schema_file_name = data_validation_config['schema_file_name']
        schema_file_path = os.path.join(
            constant.ROOT_DIR,
            data_validation_config['schema_file_path'],
            schema_file_name
        )
        report_file_path = os.path.join(
            data_validation_base_path,
            data_validation_config['report_file_path']
        )
        report_page_file_path = os.path.join(
            data_validation_base_path,
            data_validation_config['report_page_file_path']
        )
        data_validation_config = DataValidationConfig(
            schema_file_name=schema_file_name,
            schema_file_path=schema_file_path,
            report_file_path=report_file_path,
            report_page_file_path=report_page_file_path
        )

        return data_validation_config

    def get_data_transformation_config(self) -> DataTransformationConfig:
        data_transformation_config = self.config_info[constant.DATA_TRANSFORMATION_CONFIG_KEY]
        data_transformation_base_path = os.path.join(
            constant.ARTIFACT_DIR_PATH,
            constant.DATA_TRANSFORMATION_DIR,
            self.current_timestamp
        )
        add_bedroom_per_room = data_transformation_config['add_bedroom_per_room']
        processed_object_dir = os.path.join(
            data_transformation_base_path,
            data_transformation_config['processed_object_dir']
        )
        transformed_dir = os.path.join(
            data_transformation_base_path,
            data_transformation_config['transformed_dir']
        )
        transformed_test_dir = os.path.join(
            transformed_dir,
            data_transformation_config['transformed_test_dir']
        )
        transformed_train_dir = os.path.join(
            transformed_dir,
            data_transformation_config['transformed_train_dir']
        )
        processed_object_file_name = data_transformation_config['processed_object_file_name']
        transformed_train_file_name = data_transformation_config['transformed_train_file_name']
        transformed_test_file_name = data_transformation_config['transformed_test_file_name']
        data_transformation_config = DataTransformationConfig(
            add_bedroom_per_room=add_bedroom_per_room,
            processed_object_dir=processed_object_dir,
            processed_object_file_name=processed_object_file_name,
            transformed_dir=transformed_dir,
            transformed_test_dir=transformed_test_dir,
            transformed_test_file_name=transformed_test_file_name,
            transformed_train_dir=transformed_train_dir,
            transformed_train_file_name=transformed_train_file_name
        )

        return data_transformation_config

    def get_model_training_config(self) -> ModelTrainingConfig:
        model_training_config = self.config_info[constant.MODEL_TRAINING_CONFIG_KEY]
        model_training_base_path = os.path.join(
            constant.ARTIFACT_DIR_PATH,
            constant.MODEL_TRIAINNG_DIR,
            constant.CURRENT_TIMESTAMP
        )
        trained_model_dir = os.path.join(
            model_training_base_path,
            model_training_config['trained_model_dir']
        )
        trained_model_file_name = model_training_config['trained_model_file_name']
        base_accuracy = model_training_config['base_accuracy']
        model_config_dir = model_training_config['model_config_dir']
        model_config_file_name = model_training_config['model_config_file_name']
        model_training_config = ModelTrainingConfig(
            trained_model_dir=trained_model_dir,
            trained_model_file_name=trained_model_file_name,
            base_accuracy=base_accuracy,
            model_config_dir=model_config_dir,
            model_config_file_name=model_config_file_name
        )

        return model_training_config

    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        pass

    def get_push_model_config(self) -> PushModelConfig:
        pass