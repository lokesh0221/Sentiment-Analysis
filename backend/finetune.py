# backend/finetune.py
import argparse
import json
import os
import random

import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import (
    AutoTokenizer, AutoModelForSequenceClassification,
    AdamW, get_scheduler, set_seed
)

MODEL_NAME = "distilbert-base-uncased"
LABEL2ID = {"negative": 0, "positive": 1}
ID2LABEL = {0: "negative", 1: "positive"}

# Reproducibility
set_seed(42)


class SentimentDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=128):
        self.samples = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        item = self.samples[idx]
        encoding = self.tokenizer(
            item["text"],
            padding="max_length",
            truncation=True,
            max_length=self.max_length,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(),
            "attention_mask": encoding["attention_mask"].squeeze(),
            "labels": torch.tensor(LABEL2ID[item["label"]]),
        }


def load_data(path):
    with open(path, "r") as f:
        return [json.loads(line) for line in f]


def train(args):
    data = load_data(args.data)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    dataset = SentimentDataset(data, tokenizer)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=2,
        id2label=ID2LABEL,
        label2id=LABEL2ID,
    )

    optimizer = AdamW(model.parameters(), lr=args.lr)
    scheduler = get_scheduler(
        "linear", optimizer, num_warmup_steps=0, num_training_steps=len(dataloader) * args.epochs
    )

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    model.train()
    for epoch in range(args.epochs):
        total_loss = 0
        for batch in dataloader:
            batch = {k: v.to(device) for k, v in batch.items()}
            outputs = model(**batch)
            loss = outputs.loss
            loss.backward()

            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            optimizer.step()
            scheduler.step()
            optimizer.zero_grad()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch+1}/{args.epochs} - Loss: {avg_loss:.4f}")

    os.makedirs("./model", exist_ok=True)
    model.save_pretrained("./model")
    tokenizer.save_pretrained("./model")
    print("✅ Fine-tuned model saved to ./model")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", type=str, required=True, help="Path to JSONL file")
    parser.add_argument("-epochs", type=int, default=3)
    parser.add_argument("-lr", type=float, default=3e-5)
    args = parser.parse_args()

    train(args)
#to run docker-compose run --rm backend python finetune.py -data data.jsonl -epochs 3 -lr 3e-5
