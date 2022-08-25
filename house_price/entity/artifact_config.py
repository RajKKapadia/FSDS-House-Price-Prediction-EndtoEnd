from collections import namedtuple

DataIngestionArtifacts = namedtuple(
    'DataIngestionArtifacts',
    [
        'train_file_path',
        'test_file_path',
        'is_ingested',
        'message'
    ]
)

DataValidationArtifacts = namedtuple(
    'DataValidationArtifacts',
    [
        'schema_file_path',
        'report_file_path',
        'report_page_file_path',
        'is_validated',
        'message'
    ]
)

DataTransformationArtifacts = namedtuple(
    'DataTransformationArtifacts',
    [
        'is_transformed',
        'transformed_train_file_path',
        'transformed_test_file_path',
        'processed_object_file_path',
        'message'
    ]
)

ModelTrainingArtifacts = namedtuple(
    'ModelTrainingArtifacts',
    [
        'is_trained',
        'message',
        'trained_model_file_path',
        'train_accuracy',
        'test_accuracy',
        'train_rsme',
        'test_rsme',
        'model_accuracy'
    ]
)

ModelEvaluationArtifacts = namedtuple(
    'ModelEvaluationArtifacts',
    [
        'is_model_accepted',
        'evaluated_model_path'
    ]
)

ModelPusherArtifacts = namedtuple(
    'ModelPusherArtifacts',
    [
        'is_model_pushed',
        'export_model_file_path'
    ]
)