import os
from textSummarizer.entity import DataValidationConfig

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config

    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = True 
            data_ingestion_dir = os.path.join("artifacts", "data_ingestion")
            all_files = os.listdir(data_ingestion_dir)

            for file in self.config.ALL_REQUIRED_FILES:
                if file not in all_files:
                    validation_status = False
                    break  

            os.makedirs(os.path.dirname(self.config.STATUS_FILE), exist_ok=True)

            with open(self.config.STATUS_FILE, 'w') as f:
                f.write(f"Validation status: {validation_status}")

            return validation_status
        
        except Exception as e:
            raise e