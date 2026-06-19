from pathlib import Path
from textSummarizer.constants import *
from textSummarizer.utils.common import read_yaml, create_directories
from textSummarizer.entity import (DataIngestionConfig, 
                                   DataValidationConfig, 
                                   DataTransformationConfig)


class ConfigurationManager:
    def __init__(self, 
                 config_filepath = CONFIG_FILE_PATH,
                 params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories(path_to_directories=[Path(self.config.artifacts_root)])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories(path_to_directories=[Path(config.root_dir)])

        data_ingestion_config = DataIngestionConfig(
            root_dir=Path(config.root_dir),
            source_URL=config.source_URL,
            local_data_file=Path(config.local_data_file),
            unzip_dir=Path(config.unzip_dir) 
        )

        return data_ingestion_config
    
    def get_data_validation_config(self) -> DataValidationConfig:
        config = self.config.data_validation
        root_dir = Path(config.root_dir)
        status_file = Path(config.STATUS_FILE)

        create_directories(path_to_directories=[root_dir])

        data_validation_config = DataValidationConfig(
            root_dir=root_dir,
            STATUS_FILE=status_file,
            ALL_REQUIRED_FILES=config.ALL_REQUIRED_FILES
        )

        return data_validation_config
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        root_dir = Path(config.root_dir)
        data_path = Path(config.data_path)

        create_directories(path_to_directories=[root_dir])

        data_transformation_config = DataTransformationConfig(
            root_dir=root_dir,
            data_path=data_path,
            tokenizer_name=str(config.tokenizer_name)
        )

        return data_transformation_config