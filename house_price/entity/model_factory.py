from abc import ABCMeta
from collections import namedtuple
import importlib
import sys
import traceback
from typing import List

import numpy as np
from sklearn.metrics import r2_score, mean_squared_error

from house_price.exception import HousePricePredictionException
from house_price.util import util
from house_price.logger import logging
logger = logging.getLogger(__name__)

InitializedModelDetails = namedtuple(
    'InitializedModelDetails',
    [
        'model',
        'model_name',
        'model_serial_number',
        'grid_search_parameters'
    ]
)

GridSearchedBestModel = namedtuple(
    'GridSearchedBestModel',
    [
        'initialized_model',
        'model_name',
        'model_serial_number',
        'best_searched_model',
        'best_model_parameters',
        'best_model_score'
    ]
)

BestModel = namedtuple(
    'BestModel',
    [
        'model_serial_number',
        'model',
        'best_model',
        'best_parameters',
        'best_score'
    ]
)

MetricInfoArtifacts = namedtuple(
    'MetricInfoArtifacts',
    [
        'model_object',
        'model_name',
        'model_accuracy',
        'model_serial_number',
        'train_rsme',
        'train_accuracy',
        'test_rsme',
        'test_accuracy'
    ]
)

class ModelFactory:
    def __init__(self, model_config_file_path: str) -> None:
        try:
            self.model_config = util.read_yaml_file(
                file_path=model_config_file_path
            )
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def get_class_reference(self, module_name: str, class_name: str) -> ABCMeta:
        ''' Get the class reference to generate model dynamically
        '''
        try:
            module = importlib.import_module(module_name)
            class_reference = getattr(module, class_name)
            return class_reference
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def update_property_of_class(self, instance_reference: object, property_data: dict):
        try:
            if not isinstance(property_data, dict):
                raise Exception('property_data parameter must be a dictionary.')
            for key, value in property_data.items():
                setattr(instance_reference, key, value)
            return instance_reference
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def get_best_model(
        self, models: list, X_train: np.ndarray, y_train: np.ndarray,
        X_test: np.ndarray, y_test: np.ndarray, base_accuracy: float = 0.6
    ) -> MetricInfoArtifacts:
        try:
            index = 0
            metric_info_artifacts = None
            for model in models:
                logger.info(f'Model number - {index + 1}')
                logger.info(f'Model name - {str(model)}')
                y_train_prediction = model.predict(X_train)
                y_test_prediction = model.predict(X_test)
                train_accuracy = r2_score(y_train, y_train_prediction)
                test_accuracy = r2_score(y_test, y_test_prediction)
                train_rsme = np.sqrt(mean_squared_error(y_train, y_train_prediction))
                test_rsme = np.sqrt(mean_squared_error(y_test, y_test_prediction))
                model_accuracy = (2 * (train_accuracy * test_accuracy)) / (train_accuracy + test_accuracy)
                accuracy_difference = abs(test_accuracy - train_accuracy)
                logger.info(f'Model train accuracy - {round(train_accuracy, 4)}')
                logger.info(f'Model test accuracy - {round(test_accuracy, 4)}')
                logger.info(f'Model train RSME - {round(train_rsme, 4)}')
                logger.info(f'Model test RSME - {round(test_rsme, 4)}')
                logger.info(f'Model accuracy - {round(model_accuracy, 4)}')
                logger.info(f'Accuracy difference - {round(accuracy_difference, 4)}')
                if model_accuracy > base_accuracy and accuracy_difference < 0.15:
                    metric_info_artifacts = MetricInfoArtifacts(
                        model_accuracy=model_accuracy,
                        model_name=str(model),
                        model_object=model,
                        model_serial_number=index,
                        test_accuracy=test_accuracy,
                        train_accuracy=train_accuracy,
                        test_rsme=test_rsme,
                        train_rsme=train_rsme
                    )
                    base_accuracy = model_accuracy
                index += 1
            if metric_info_artifacts is None:
                logger.info('No model found with better accuracy.')
            return metric_info_artifacts
        except Exception as e:
                logger.exception(f'Uncaught exception - {traceback.format_exc()}')
                raise HousePricePredictionException(e, sys) from e

    def initialize_all_models(self) -> List[InitializedModelDetails]:
        try:
            models = []
            for module in self.model_config['model_selection']:
                module_config = self.model_config['model_selection'][module]
                model_object = self.get_class_reference(
                    module_name=module_config['module'],
                    class_name=module_config['class']
                )
                if 'params' in module_config:
                    parameters = module_config['params']
                    model_object = self.update_property_of_class(
                        instance_reference=model_object,
                        property_data=parameters
                    )
                    model = model_object()
                else:
                    model = model_object()
                if 'grid_search_params' in module_config:
                    grid_search_parameters = module_config['grid_search_params']
                else:
                    grid_search_parameters = None
                models.append(
                    InitializedModelDetails(
                        model=model,
                        model_name=f'{module_config["class"]}',
                        model_serial_number=module,
                        grid_search_parameters=grid_search_parameters
                    )
                )

            return models
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def grid_search(self, initialized_model: InitializedModelDetails, X: np.ndarray, y: np.ndarray) -> GridSearchedBestModel:
        try:
            if initialized_model.grid_search_parameters == None:
                logger.info('No parameters set for grid search.')
                logger.info(f'Skipping grid search for {initialized_model.model_name}')
                model = initialized_model.model
                model.fit(X, y)
                grid_searched_best_model = GridSearchedBestModel(
                    initialized_model=initialized_model.model,
                    model_serial_number=initialized_model.model_serial_number,
                    model_name=initialized_model.model_name,
                    best_searched_model=model,
                    best_model_parameters=None,
                    best_model_score=None
                )
                return grid_searched_best_model
            logger.info(f'Started grid search for {initialized_model.model_name}')
            grid_search_object = self.get_class_reference(
                module_name=self.model_config['grid_search']['module'],
                class_name=self.model_config['grid_search']['class']
            )
            grid_search = grid_search_object(
                estimator=initialized_model.model,
                param_grid=initialized_model.grid_search_parameters 
            )
            grid_search = self.update_property_of_class(
                instance_reference=grid_search,
                property_data=self.model_config['grid_search']['params']
            )
            grid_search.fit(X, y)
            grid_searched_best_model = GridSearchedBestModel(
                initialized_model=initialized_model.model,
                model_serial_number=initialized_model.model_serial_number,
                model_name=initialized_model.model_name,
                best_searched_model=grid_search.best_estimator_,
                best_model_parameters=grid_search.best_params_,
                best_model_score=grid_search.best_score_
            )

            logger.info(f'Finished grid search for {initialized_model.model_name}')
            logger.info(f'Best parameters - {grid_search.best_params_}')
            return grid_searched_best_model
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def perform_grid_search(self, initialized_models: List[InitializedModelDetails], X: np.ndarray, y: np.ndarray) -> List[GridSearchedBestModel]:
        try:
            grid_searched_best_models = []
            for initialized_model in initialized_models:
                grid_searched_best_model = self.grid_search(
                    initialized_model=initialized_model,
                    X=X,
                    y=y
                )
                grid_searched_best_models.append(grid_searched_best_model)
            
            return grid_searched_best_models
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e
