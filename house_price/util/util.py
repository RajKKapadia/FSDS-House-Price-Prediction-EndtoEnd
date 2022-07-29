import traceback

import yaml

from logger import logging
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
    except:
        logger.exception(f'Uncaught exception - {traceback.format_exc()}')