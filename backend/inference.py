# backend/inference.py
import torch
import torch.nn.functional as F

def predict_sentiment(text, model, tokenizer):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
        score, pred = torch.max(probs, dim=1)
        label = model.config.id2label[pred.item()]
        return label.lower(), round(score.item(), 4)
