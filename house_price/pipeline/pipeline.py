from asyncio.log import logger
from house_price.config.configuration import Configuration
from house_price.entity.artifact_config import DataIngestionArtifacts, DataTransformationArtifacts, DataValidationArtifacts, ModelTrainingArtifacts
from house_price.component.data_ingestion import DataIngestion
from house_price.component.data_validation import DataValidation
from house_price.component.data_transformation import DataTransformation
from house_price.component.model_trainer import ModelTrainer

class Pipeline:

    def __init__(self, configuration: Configuration = Configuration()) -> None:
        self.configuration = configuration

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        data_ingestion = DataIngestion(
            data_ingestion_config=self.configuration.get_data_ingestion_config()
        )
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()

        return data_ingestion_artifacts

    def start_data_validation(self) -> DataValidationArtifacts:
        data_validation = DataValidation(
            data_ingestion_config=self.configuration.get_data_ingestion_config(),
            data_validation_config=self.configuration.get_data_validation_config()
        )
        data_validation_artifacts = data_validation.initiate_data_validation()

        return data_validation_artifacts

    def start_data_transformation(
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

    def start_model_training(self, data_transformation_artifacts: DataTransformationArtifacts) -> ModelTrainingArtifacts:
        model_trainer = ModelTrainer(
            self.configuration.get_model_training_config(),
            data_transformation_artifacts=data_transformation_artifacts
        )
        model_training_artifact = model_trainer.initiate_model_trainer()

        return model_training_artifact

    def start_pipeline(self):
        data_ingestion_artifacts = self.start_data_ingestion()
        data_validation_artifacts = self.start_data_validation()
        data_transformation_artifacts = self.start_data_transformation(
            data_ingestion_artifacts=data_ingestion_artifacts,
            data_validation_artifacts=data_validation_artifacts
        )
        model_training_artifact = self.start_model_training(
            data_transformation_artifacts=data_transformation_artifacts
        )
        if model_training_artifact == None:
            print('No model found with better accuracy, please reduce the base accuracy.')
    