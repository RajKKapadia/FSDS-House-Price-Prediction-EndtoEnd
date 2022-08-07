import traceback
import sys

import yaml
import pandas as pd

from house_price.exception import HousePricePredictionException
import logging
logger = logging.getLogger(__name__)

def read_yaml_file(file_path: str) -> dict:
    ''' This function reads YAML file and returns a dict\n
        ------------------------------------------------
        Takes - yaml file path (str)\n
        Returns - yaml file content as dict
    '''
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logger.exception(f'Uncaught exception - {traceback.format_exc()}')
        raise HousePricePredictionException(e, sys) from e

def read_dataframe(file_path: str, schema_file_path: str) -> pd.DataFrame:
    try:
        schema = data = read_yaml_file(file_path=schema_file_path)
        columns = schema['columns']
        df = pd.read_csv(
            filepath_or_buffer=file_path
        )
        columns = data['columns']
        for key in columns:
            df[key] = df[key].astype(dtype=columns[key])
        
        return df
    except Exception as e:
        logger.exception(f'Uncaught exception - {traceback.format_exc()}')
        raise HousePricePredictionException(e, sys) from e
    