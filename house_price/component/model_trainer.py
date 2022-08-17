import sys
import traceback
import os

import numpy as np
import dill

from house_price.entity.entity_config import ModelTrainingConfig
from house_price.entity.artifact_config import DataTransformationArtifacts, ModelTrainingArtifacts
from house_price.entity.model_factory import ModelFactory
from house_price.exception import HousePricePredictionException
from house_price import constant
from house_price.logger import logging
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self, model_training_config: ModelTrainingConfig, data_transformation_artifacts: DataTransformationArtifacts) -> None:
        try:
            self.model_training_config = model_training_config
            self.data_transformation_artifacts = data_transformation_artifacts
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def initiate_model_trainer(self) -> ModelTrainingArtifacts:
        logger.info(f'{"=" * 20} Model training log started. {"=" * 20}')
        training_array = np.load(
            file=self.data_transformation_artifacts.transformed_train_file_path
        )
        testing_array = np.load(
            file=self.data_transformation_artifacts.transformed_test_file_path
        )
        X_train, y_train = training_array[:, :-1], training_array[:, -1]
        X_test, y_test = testing_array[:, :-1], testing_array[:, -1]
        model_config_file_path = os.path.join(
            self.model_training_config.model_config_dir,
            self.model_training_config.model_config_file_name
        )
        logger.info('Training and testing data loaded successfully.')
        model_factory = ModelFactory(
            model_config_file_path=model_config_file_path
        )
        initialized_models = model_factory.initialize_all_models()
        logger.info('Initialized all the models.')
        logger.info('Started grid serch for all the initialized models.')
        grid_searched_best_models = model_factory.perform_grid_search(
            initialized_models=initialized_models,
            X=X_train,
            y=y_train
        )
        logger.info('Started evaluation of all the best models.')
        models = [model.best_searched_model for model in grid_searched_best_models]
        best_model = model_factory.get_best_model(
            models=models,
            X_train=X_train,
            y_train=y_train,
            X_test=X_test,
            y_test=y_test
        )
        if best_model == None:
            logger.info('No best model found.')
        logger.info('Saving the best model.')
        trained_model_dir = os.path.join(
            constant.ARTIFACT_DIR_PATH,
            constant.CURRENT_TIMESTAMP,
            self.model_training_config.trained_model_dir
        )
        os.makedirs(trained_model_dir, exist_ok=True)
        trained_model_file_path = os.path.join(
            trained_model_dir,
            self.model_training_config.trained_model_file_name
        )
        with open(trained_model_file_path, 'wb') as file_object:
            dill.dump(best_model, file_object)
        model_training_artifact = ModelTrainingArtifacts(
            is_trained=True,
            message='Training successfull',
            model_accuracy=best_model.model_accuracy,
            test_accuracy=best_model.test_accuracy,
            test_rsme=best_model.test_rsme,
            train_accuracy=best_model.train_accuracy,
            train_rsme=best_model.train_rsme,
            trained_model_file_path=trained_model_file_path
        )

        logger.info(f'{"=" * 20} Model training log finished. {"=" * 20}')
        return model_training_artifact