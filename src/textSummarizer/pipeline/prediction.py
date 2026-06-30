import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from textSummarizer.config.configuration import ConfigurationManager
from textSummarizer.logging import logger

class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()
        
        logger.info("Loading fine-tuned tokenizer from artifacts...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        
        logger.info("Loading fine-tuned Seq2Seq model weights from artifacts...")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path)
        logger.info("Prediction pipeline components initialized successfully.")
    
    def predict(self, text: str) -> str:
        logger.info("Received text dialogue for summary generation.")
        print(f"\n===== [INPUT DIALOGUE] =====\n{text}")

        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            max_length=1024, 
            truncation=True
        )

        summary_ids = self.model.generate(
            inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            num_beams=8,
            length_penalty=0.8,
            max_length=128,
            min_length=30
        )

        output = self.tokenizer.decode(
            summary_ids[0], 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=True
        )
        
        print(f"\n===== [MODEL GENERATED SUMMARY] =====\n{output}")
        logger.info("Summary generated successfully by the model.")

        return output
    
# if __name__ == "__main__":
#     sample_text = """
#     Amanda: Hey, did you finish the evaluation script for the Pegasus model?
#     Shubham: Yes, just completed it on Colab! It took about 21 minutes on the T4 GPU.
#     Amanda: Awesome! What were the ROUGE scores looking like?
#     Shubham: ROUGE-1 hit 44.32% and ROUGE-2 is at 21.21%. Pretty solid metrics.
#     Amanda: Wow, that's fantastic news. Let's push it to GitHub and start the prediction pipeline next.
#     """
    
#     try:
#         predictor = PredictionPipeline()
#         summary = predictor.predict(sample_text)
#     except Exception as e:
#         logger.exception(e)
#         raise e