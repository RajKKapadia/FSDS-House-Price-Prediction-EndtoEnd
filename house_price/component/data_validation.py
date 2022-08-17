import traceback
import os
import sys

import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab
import json

from house_price.entity.entity_config import DataValidationConfig, DataIngestionConfig
from house_price.entity.artifact_config import DataValidationArtifacts
from house_price.exception import HousePricePredictionException
from house_price.logger import logging
logger = logging.getLogger(__name__)

class DataValidation:

    def __init__(
        self,
        data_validation_config: DataValidationConfig,
        data_ingestion_config: DataIngestionConfig
    ) -> None:
        try:
            self.data_validation_config = data_validation_config
            self.data_ingestion_config = data_ingestion_config
            logger.info(f'{"=" * 20} Data validation log started. {"=" * 20}')
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def data_exists(self) -> bool:
        try:
            is_train_exists = False
            is_test__exists = False
            is_train_exists = os.path.exists(
                os.path.join(
                    self.data_ingestion_config.train_data_dir,
                    self.data_ingestion_config.train_data_file_name
                )
            )
            is_test__exists = os.path.exists(
                os.path.join(
                    self.data_ingestion_config.test_data_dir,
                    self.data_ingestion_config.test_data_file_name
                )
            )
            is_data_exists = is_train_exists and is_test__exists
            if not is_data_exists:
                logger.error('Train and Test file does not exists.')
                raise Exception('Train and Test file does not exists.')
            logger.info('Data exists.')

            return is_data_exists
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def get_data(self) -> tuple:
        try:
            logger.info('Reading csv files.')
            train_df = pd.read_csv(
                filepath_or_buffer=os.path.join(
                    self.data_ingestion_config.train_data_dir,
                    self.data_ingestion_config.train_data_file_name
                )
            )
            test_df = pd.read_csv(
                filepath_or_buffer=os.path.join(
                    self.data_ingestion_config.test_data_dir,
                    self.data_ingestion_config.test_data_file_name
                )
            )
            logger.info('Finished reading csv files.')

            return train_df, test_df
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e


    def validate_data(self) -> bool:
        ''' TODO
            validate data
        '''
        try:
            is_validated = True

            return is_validated
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def generate_data_drift_report(self) -> json:
        try:
            profile = Profile(sections=[DataDriftProfileSection()])
            train_df, test_df = self.get_data()
            profile.calculate(train_df, test_df)
            report = json.loads(profile.json())
            report_dir = os.path.dirname(self.data_validation_config.report_file_path)
            os.makedirs(report_dir, exist_ok=True)
            with open(self.data_validation_config.report_file_path, 'w') as report_file:
                json.dump(
                    report,
                    report_file,
                    indent=2
                )
            logger.info('Data drift report generated.')

            return report
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def generate_data_drift_page(self) -> None:
        try:
            dashboard = Dashboard(tabs=[DataDriftTab()])
            train_df, test_df = self.get_data()
            dashboard.calculate(train_df, test_df)
            report_page_dir = os.path.dirname(self.data_validation_config.report_page_file_path)
            os.makedirs(report_page_dir, exist_ok=True)
            dashboard.save(self.data_validation_config.report_page_file_path)
            logger.info('Data drift report saved.')
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def is_data_drift(self) -> bool:
        ''' TODO
            validate data drift
        '''
        try:
            report = self.generate_data_drift_report()

            is_data_drift = report['data_drift']['data']['metrics']['dataset_drift']

            return is_data_drift
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifacts:
        try:
            self.data_exists()
            schema_file_path = self.data_validation_config.schema_file_path
            report_file_path = self.generate_data_drift_report()
            report_page_file_path = self.generate_data_drift_page()
            is_validated = self.validate_data()
            is_data_drift = self.is_data_drift()
            if not is_validated:
                logger.error('The data is not validate.')
                raise Exception('The data is not validated.')
            if is_data_drift:
                logger.error('There is a data drift.')
                raise Exception('There is a data drift.')
            data_validation_artifacts = DataValidationArtifacts(
                schema_file_path=schema_file_path,
                report_file_path=report_file_path,
                report_page_file_path=report_page_file_path,
                is_validated=is_validated,
                message='Data is okay.'
            )
            logger.info(f'{"=" * 20} Data validation log finished. {"=" * 20}')
            
            return data_validation_artifacts
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e