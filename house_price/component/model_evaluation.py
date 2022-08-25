import sys
import os
import traceback

import dill
import yaml

from house_price.entity.entity_config import ModelEvaluationConfig
from house_price.entity.artifact_config import DataIngestionArtifacts, DataValidationArtifacts, ModelEvaluationArtifacts, ModelTrainingArtifacts
from house_price.exception import HousePricePredictionException
from house_price.util import util
from logger import logging
logger = logging.getLogger(__name__)

class ModelEvaluation:

    def __init__(
        self,
        model_evalution_config: ModelEvaluationConfig,
        data_ingestion_artifacts: DataIngestionArtifacts,
        data_validation_artifacts: DataValidationArtifacts,
        model_training_artifacts: ModelTrainingArtifacts
    ) -> None:
        try:
            self.model_evalution_config = model_evalution_config
            self.data_ingestion_artifacts = data_ingestion_artifacts,
            self.data_validation_artifacts = data_validation_artifacts
            self.model_training_artifacts = model_training_artifacts
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def get_best_model(self) -> None:
        ''' Try to read the best model from model_evalution
        '''
        try:
            model_evaluation_file_path = self.model_evalution_config.model_evaluation_file_path
            if not os.path.exists(path=model_evaluation_file_path):
                with open(model_evaluation_file_path, 'r') as file:
                    yaml.dump(None, file)
                return None
            model_evaluation_file_data = util.read_yaml_file(model_evaluation_file_path)
            if model_evaluation_file_data is None:
                model_evaluation_file_data = dict()
            if 'best_model' not in model_evaluation_file_data:
                return None
            with open(model_evaluation_file_data['best_model']['model_path'], 'rb') as file:
                model = dill.load(file)
            return model
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def update_evaluation_report(self) -> None:
        pass

    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        logger.info(f'{"=" * 20} Model evaluation log started. {"=" * 20}')
        trained_model_file_path = self.model_training_artifacts.trained_model_file_path
        with open(trained_model_file_path, 'rb') as file:
            trained_model = dill.load(file=file)
        