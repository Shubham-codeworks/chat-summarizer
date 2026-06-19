from textSummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from textSummarizer.logging import logger

STAGE_NAME = "Data Ingestion Stage"
try:
    logger.info(f">>>>> Stage {STAGE_NAME} started <<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>> Stage {STAGE_NAME} has completed <<<<<\n\nxxxxxxxxxxx")
except Exception as e:
    logger.exception(e)
    raise e