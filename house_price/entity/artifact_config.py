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