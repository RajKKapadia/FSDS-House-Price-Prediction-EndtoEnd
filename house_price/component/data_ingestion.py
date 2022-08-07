import traceback
import os
import sys
import urllib.request
import tarfile

import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit
import numpy as np

from house_price.entity.entity_config import DataIngestionConfig
from house_price.entity.artifact_config import DataIngestionArtifacts
from house_price.logger import logging
from house_price.exception import HousePricePredictionException
logger = logging.getLogger(__name__)

class DataIngestion:

    def __init__(self, data_ingestion_config: DataIngestionConfig) -> None:
        try:
            self.data_ingestion_config = data_ingestion_config
            logger.info(f'{"=" * 20} Data ingestion log started. {"=" * 20}')
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e
        
    def __download_data_from_url(self, url: str) -> str:
        try:
            file_name = os.path.basename(url)
            tgz_dir = self.data_ingestion_config.downloaded_zip_file_path
            os.makedirs(tgz_dir, exist_ok=True)
            tgz_file_path = os.path.join(tgz_dir, file_name)
            logger.info(f'Started downloading the file from {url} at {tgz_file_path}')
            urllib.request.urlretrieve(url, tgz_file_path)
            logger.info(f'File downloaded at {tgz_file_path}')
            
            return tgz_file_path
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def __extract_tgz_file(self, tar_file_path: str) -> None:
        try:
            if tarfile.is_tarfile(tar_file_path):
                raw_data_dir = self.data_ingestion_config.raw_data_path
                os.makedirs(raw_data_dir, exist_ok=True)
                logger.info(f'Extracting tgz file at {raw_data_dir}')
                with tarfile.open(tar_file_path) as file:
                    file.extractall(raw_data_dir)
                logger.info(f'File extracted at {raw_data_dir}')
            else:
                logger.info('The file is not a valid tgz file.')
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def __split_data(self, raw_data_dir: str) -> None:
        try:
            file_name = os.listdir(raw_data_dir)[0]
            file_path = os.path.join(raw_data_dir, file_name)
            df = pd.read_csv(filepath_or_buffer=file_path)
            df['income_category'] = pd.cut(
                df['median_income'],
                bins=[0.0, 1.5, 3.0, 4.5, 6.0, np.inf],
                labels=[1, 2, 3, 4, 5]
            )
            sss = StratifiedShuffleSplit(
                n_splits=1,
                test_size=0.2,
                random_state=2022
            )
            for train_idx, test_idx in sss.split(X=df, y=df['income_category']):
                train_df = df.loc[train_idx].drop(labels=['income_category'], axis=1)
                test_df = df.loc[test_idx].drop(labels=['income_category'], axis=1)
            logger.info('Finished splitting the data.')

            return train_df, test_df
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        try:
            url = self.data_ingestion_config.dataset_download_url
            tgz_file_path = self.__download_data_from_url(url)
            self.__extract_tgz_file(tgz_file_path)
            raw_data_dir = self.data_ingestion_config.raw_data_path
            train_df, test_df = self.__split_data(raw_data_dir)
            train_data_dir = self.data_ingestion_config.train_data_dir
            test_data_dir = self.data_ingestion_config.test_data_dir
            os.makedirs(train_data_dir, exist_ok=True)
            os.makedirs(test_data_dir, exist_ok=True)
            train_file_path = os.path.join(
                self.data_ingestion_config.train_data_dir,
                self.data_ingestion_config.train_data_file_name
            )
            test_file_path = os.path.join(
                self.data_ingestion_config.test_data_dir,
                self.data_ingestion_config.test_data_file_name
            )
            train_df.to_csv(path_or_buf=train_file_path, index=False)
            test_df.to_csv(path_or_buf=test_file_path, index=False)
            logger.info('Training and testing csv file is created.')
            logger.info(f'{"=" * 20} Data ingestion log finished. {"=" * 20}')
            
            return DataIngestionArtifacts(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message='Data ingestion is successfull.'
            )
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e
            