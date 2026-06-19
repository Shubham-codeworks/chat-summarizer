import os
from transformers import AutoTokenizer
from datasets import load_dataset
from textSummarizer.entity import DataTransformationConfig

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        self.tokenizer = AutoTokenizer.from_pretrained(config.tokenizer_name)

    def convert_examples_to_features(self, example_batch):
        input_encodings = self.tokenizer(example_batch["dialogue"], 
                                         max_length = 1024, truncation=True)

        target_encodings = self.tokenizer(text_target=example_batch["summary"], 
                                          max_length = 128, truncation=True)

        return {
            "input_ids": input_encodings["input_ids"],
            "attention_mask": input_encodings["attention_mask"],
            "labels": target_encodings["input_ids"]
        }
    
    def convert(self):
        try:
            dataset_samsum = load_dataset('json', data_files={
                'train': os.path.join(self.config.data_path, 'train.json'),
                'test': os.path.join(self.config.data_path, 'test.json'),
                'validation': os.path.join(self.config.data_path, 'val.json')
            })
            
            dataset_samsum_pt = dataset_samsum.map(self.convert_examples_to_features, batched=True)
            
            output_path = os.path.join(self.config.root_dir, "samsum_dataset")
            dataset_samsum_pt.save_to_disk(output_path) 
            
        except Exception as e:
            raise e