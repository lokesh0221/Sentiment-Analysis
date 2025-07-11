# backend/model_utils.py
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os

MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
MODEL_DIR = "./model"

def load_model():
    if os.path.isdir(MODEL_DIR) and os.listdir(MODEL_DIR):
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        print("🔁 Loaded fine-tuned model from ./model/")
    else:
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        print("✅ Loaded pre-trained model from Hugging Face")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    return model, tokenizer
