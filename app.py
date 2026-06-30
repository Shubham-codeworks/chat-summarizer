import os
import sys
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel

sys.path.append(os.path.abspath("src"))

from textSummarizer.pipeline.prediction import PredictionPipeline
from textSummarizer.logging import logger

app = FastAPI(
    title="Pegasus Text Summarizer API",
    description="A FastAPI backend for conversational text summarization fine-tuned on the SAMSum dataset.",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    text: str

# Initializing the pipeline globally
try:
    logger.info("Initializing global PredictionPipeline for API...")
    predictor = PredictionPipeline()
except Exception as e:
    logger.error(f"Failed to initialize PredictionPipeline: {e}")
    predictor = None


@app.get("/", tags=["Root"])
async def index():
    return {"message": "Pegasus Text Summarizer API is running successfully. Head over to /docs for interactive Swagger UI."}


@app.get("/train", tags=["Pipeline"])
async def train_route():
    try:
        logger.info("Training route triggered.")
        os.system("python main.py")
        return Response("Training successful!!")
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Error occurred during training: {e}")


@app.post("/predict", tags=["Inference"])
async def predict_route(request: PredictionRequest):
    """
    Accepts a JSON payload containing the conversation text and returns the model summary.
    """
    if predictor is None:
        raise HTTPException(
            status_code=503, 
            detail="Prediction pipeline model weights are not loaded properly on the server."
        )
    
    try:
        incoming_text = request.text
        logger.info(f"API received inference request with characters count: {len(incoming_text)}")
        
        # Strip trailing spaces or formatting artifacts
        clean_text = incoming_text.strip()
        
        # Fire inference
        summary = predictor.predict(clean_text)
        
        return {"summary": summary}
        
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)