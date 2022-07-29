import logging
logger = logging.getLogger(__name__)

from house_price.config.configuration import Configuration
from house_price.entity.artifact_config import DataIngestionArtifacts
from house_price.component.data_ingestion import DataIngestion

class Pipeline:

    def __init__(self, configuration: Configuration = Configuration()) -> None:
        self.configuration = configuration

    def start_data_ingestion(self) -> DataIngestionArtifacts:
        data_ingestion = DataIngestion(
            data_ingestion_config=self.configuration.get_data_ingestion_config()
        )
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        return data_ingestion_artifacts

    def start_pipeline(self):
        self.start_data_ingestion()
    