import traceback
import sys
import os
import dill

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import numpy as np

from house_price.entity.entity_config import DataTransformationConfig
from house_price.entity.artifact_config import DataIngestionArtifacts, DataValidationArtifacts, DataTransformationArtifacts
from house_price.exception import HousePricePredictionException
from house_price.util import util
from house_price.logger import logging
logger = logging.getLogger(__name__)

class FeatureGenerator(BaseEstimator, TransformerMixin):

    def __init__(
        self,
        add_bedrooms_per_room: bool = True,
        total_rooms_index: int = 3,
        population_index: int = 5,
        households_index: int = 6,
        total_bedrooms_index: int = 4,
        columns: list = None
    ) -> None:
        ''' FeatureGenerator Initialization
            add_bedrooms_per_room: bool
            total_rooms_index: int index number of total rooms column
            population_index: int index number of total population column
            households_index: int index number of  households column
            total_bedrooms_index: int index number of bedrooms column
        '''
        try:
            self.columns = columns
            if self.columns is not None:
                total_rooms_index = self.columns.index('total_rooms')
                population_index = self.columns.index('population')
                households_index = self.columns.index('households')
                total_bedrooms_index = self.columns.index('total_bedrooms')

            self.add_bedrooms_per_room = add_bedrooms_per_room
            self.total_rooms_index = total_rooms_index
            self.population_index = population_index
            self.households_index = households_index
            self.total_bedrooms_index = total_bedrooms_index
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def fit(self, X, y=None) -> object:
        return self

    def transform(self, X) -> np.ndarray:
        try:
            room_per_household = X[:, self.total_rooms_index] / X[:, self.households_index]
            population_per_household = X[:, self.population_index] / X[:, self.households_index]
            if self.add_bedrooms_per_room:
                bedrooms_per_room = X[:, self.total_bedrooms_index] / X[:, self.total_rooms_index]
                generated_feature = np.c_[
                    X, room_per_household, population_per_household, bedrooms_per_room
                ]
            else:
                generated_feature = np.c_[
                    X, room_per_household, population_per_household
                ]

            return generated_feature
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

class DataTransformation:

    def __init__(
        self,
        data_ingestion_artifacts: DataIngestionArtifacts,
        data_validation_artifacts: DataValidationArtifacts,
        data_transformation_config: DataTransformationConfig
    ) -> None:
        try:
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_artifacts = data_validation_artifacts
            self.data_transformation_config = data_transformation_config
            logger.info(
                f'{"=" * 20} Data transformtaion log started. {"=" * 20}')
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def column_transformer(self) -> ColumnTransformer:
        try:
            schema_file_path = self.data_validation_artifacts.schema_file_path
            schema = util.read_yaml_file(schema_file_path)
            numerical_columns = schema['numerical_columns']
            categorical_columns = schema['categorical_columns']
            numerical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    (
                        'feature_generator',
                        FeatureGenerator(
                            add_bedrooms_per_room=self.data_transformation_config.add_bedroom_per_room,
                            columns=numerical_columns
                        )
                    ),
                    ('scaler', StandardScaler())
                ]
            )
            categorical_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),
                    ('ohe', OneHotEncoder()),
                    ('scaler', StandardScaler(with_mean=False))
                ]
            )
            column_transformer = ColumnTransformer(
                transformers=[
                    ('numerical_pipeline', numerical_pipeline, numerical_columns),
                    ('categorical_pipeline', categorical_pipeline, categorical_columns)
                ]
            )

            logger.info('Column transformer is created successfullt.')
            return column_transformer
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def get_dataframe(self) -> tuple:
        try:
            logger.info('Reading csv files.')
            schema_file_path = self.data_validation_artifacts.schema_file_path
            train_file_path = self.data_ingestion_artifacts.train_file_path
            test_file_path = self.data_ingestion_artifacts.test_file_path
            train_df = util.read_dataframe(
                file_path=train_file_path,
                schema_file_path=schema_file_path
            )
            test_df = util.read_dataframe(
                file_path=test_file_path,
                schema_file_path=schema_file_path
            )

            return train_df, test_df
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def get_features_and_target(self) -> tuple:
        try:
            logger.info('Generating X, y, X_test, and y_test')
            schema_file_path = self.data_validation_artifacts.schema_file_path
            train_df, test_df = self.get_dataframe()
            schema = util.read_yaml_file(
                file_path=schema_file_path
            )
            target_column_name = schema['target_column_name']
            train_features = train_df.drop(
                labels=[target_column_name],
                axis=1
            )
            test_features = test_df.drop(
                labels=[target_column_name],
                axis=1
            )
            train_target = train_df[target_column_name]
            test_target = test_df[target_column_name]

            return train_features, train_target, test_features, test_target
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifacts:
        try:
            train_features, train_target, test_features, test_target = self.get_features_and_target()
            column_transformer = self.column_transformer()
            processed_train_features = column_transformer.fit_transform(train_features)
            processed_test_features = column_transformer.transform(test_features)
            training_data = np.c_[
                processed_train_features,
                np.array(train_target)
            ]
            testing_data = np.c_[
                processed_test_features,
                np.array(test_target)
            ]
            logger.info('Saving training and testing data.')
            transformed_train_file_path = os.path.join(
                self.data_transformation_config.transformed_train_dir,
                self.data_transformation_config.transformed_train_file_name
            )
            transformed_test_file_path = os.path.join(
                self.data_transformation_config.transformed_test_dir,
                self.data_transformation_config.transformed_test_file_name
            )
            os.makedirs(self.data_transformation_config.transformed_train_dir, exist_ok=True)
            os.makedirs(self.data_transformation_config.transformed_test_dir, exist_ok=True)
            np.save(
                file=transformed_train_file_path,
                arr=training_data
            )
            np.save(
                file=transformed_test_file_path,
                arr=testing_data
            )
            logger.info('Saving the processed object.')
            processed_object_file_path = os.path.join(
                self.data_transformation_config.processed_object_dir,
                self.data_transformation_config.processed_object_file_name
            )
            os.makedirs(self.data_transformation_config.processed_object_dir, exist_ok=True)
            with open(processed_object_file_path, 'wb') as file_object:
                dill.dump(column_transformer, file_object)
            is_transformed = True
            data_tranformation_artifacts = DataTransformationArtifacts(
                is_transformed=is_transformed,
                message='Data transformed and saved.',
                processed_object_file_path=processed_object_file_path,
                transformed_train_file_path=transformed_train_file_path,
                transformed_test_file_path=transformed_test_file_path
            )

            logger.info(f'{"=" * 20} Data transformtaion log finished. {"=" * 20}')
            return data_tranformation_artifacts
        except Exception as e:
            logger.exception(f'Uncaught exception - {traceback.format_exc()}')
            raise HousePricePredictionException(e, sys) from e
        
