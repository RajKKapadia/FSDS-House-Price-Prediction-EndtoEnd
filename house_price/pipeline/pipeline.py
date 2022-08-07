import logging
logger = logging.getLogger(__name__)

from house_price.config.configuration import Configuration
from house_price.entity.artifact_config import DataIngestionArtifacts, DataTransformationArtifacts, DataValidationArtifacts
from house_price.component.data_ingestion import DataIngestion
from house_price.component.data_validation import DataValidation
from house_price.component.data_transformation import DataTransformation

class Pipeline:

    def __init__(self, configuration: Configuration = Configuration()) -> None:
        self.configuration = configuration

    def __start_data_ingestion(self) -> DataIngestionArtifacts:
        data_ingestion = DataIngestion(
            data_ingestion_config=self.configuration.get_data_ingestion_config()
        )
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

        return data_ingestion_artifacts

    def __start_data_validation(self) -> DataValidationArtifacts:
        data_validation = DataValidation(
            data_ingestion_config=self.configuration.get_data_ingestion_config(),
            data_validation_config=self.configuration.get_data_validation_config()
        )
        data_validation_artifacts = data_validation.initiate_data_validation()

        return data_validation_artifacts

    def _start_data_transformation(
        self,
        data_ingestion_artifacts,
        data_validation_artifacts
    ) -> DataTransformationArtifacts:
        data_transformation = DataTransformation(
            data_ingestion_artifacts=data_ingestion_artifacts,
            data_validation_artifacts=data_validation_artifacts,
            data_transformation_config=self.configuration.get_data_transformation_config()
        )
        data_transformation_artifacts = data_transformation.initiate_data_transformation()

        return data_transformation_artifacts

    def start_pipeline(self):
        data_ingestion_artifacts = self.__start_data_ingestion()
        data_validation_artifacts = self.__start_data_validation()
        data_transformation_artifacts = self._start_data_transformation(
            data_ingestion_artifacts=data_ingestion_artifacts,
            data_validation_artifacts=data_validation_artifacts
        )
    