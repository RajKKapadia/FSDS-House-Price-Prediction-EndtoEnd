from collections import namedtuple

DataIngestionConfig = namedtuple(
    'DataIngestionConfig',
    [
        'dataset_download_url',
        'downloaded_zip_file_path',
        'raw_data_path',
        'ingested_dir',
        'train_data_dir',
        'train_data_file_name',
        'test_data_dir',
        'test_data_file_name'
    ]
)

DataValidationConfig = namedtuple(
    'DataValidationConfig',
    [
        'schema_file_path',
        'schema_file_name',
        'report_file_path',
        'report_page_file_path'
    ]
)

DataTransformationConfig = namedtuple(
    'DataTransformationConfig',
    [
        'add_bedroom_per_room',
        'transformed_dir',
        'transformed_train_dir',
        'transformed_train_file_name',
        'transformed_test_file_name',
        'transformed_test_dir',
        'processed_object_dir',
        'processed_object_file_name'
    ]
)

ModelTrainingConfig = namedtuple(
    'ModelTrainingConfig',
    [
        'trained_model_dir',
        'trained_model_file_name',
        'base_accuracy',
        'model_config_dir',
        'model_config_file_name'
    ]
)

ModelEvaluationConfig = namedtuple(
    'ModelEvaluationConfig',
    [
        'model_evaluation_file_path',
        'time_stamp'
    ]
)

PushModelConfig = namedtuple(
    'PushModelConfig',
    ['model_export_dir_path']
)
