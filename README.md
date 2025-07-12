# 🧠 Electronix AI — Binary Sentiment Analysis Microservice

This project is an end-to-end containerized sentiment classification system using Hugging Face Transformers. It supports fine-tuning on custom datasets, inference via GraphQL API, and a minimal React frontend with dark mode and live typing inference.

---

## 🚀 Tech Stack

- **Backend**: FastAPI + Strawberry GraphQL + Transformers (DistilBERT)
- **Frontend**: React (with live sentiment typing + dark mode)
- **Model**: `distilbert-base-uncased` (fine-tunable)
- **Deployment**: Docker Compose
- **Optional Enhancements**: 
  - Async inference
  - Multi-stage Docker builds
  - Fine-tuning CLI

---

## 🧩 Folder Structure

```
electronix-ai-sentiment/
├── backend/
│   ├── app.py
│   ├── inference.py
│   ├── model_utils.py
│   ├── finetune.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

---

## ⚙️ Setup Instructions

### 📦 Option 1: Docker Compose (Recommended)
```bash
git clone https://github.com/your-username/electronix-ai.git
cd electronix-ai
docker-compose up --build
```
Frontend: http://localhost:3000

Backend (GraphQL): http://localhost:8000/graphql

#### 🧪 Run Fine-Tuning (in Docker)
```bash
docker-compose run --rm backend python finetune.py -data data.jsonl -epochs 3 -lr 3e-5
```

### 🖥️ Option 2: Run manually (Dev mode)
**Backend:**
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```
**Frontend:**
```bash
cd frontend
npm install
npm start
```

---

## 🔌 GraphQL API Schema

### 📥 Mutation/Query Example
```graphql
query {
  sentiment(text: "This product is fantastic!") {
    label
    score
  }
}
```

### 📤 Response
```json
{
  "data": {
    "sentiment": {
      "label": "positive",
      "score": 0.982
    }
  }
}
```

---

## 📹 Demo & Deployment

- 🔗 **Demo Video**: Watch 3-minute walkthrough (unlisted)
- 🌐 **Deployed Frontend**: https://electronix-ai.vercel.app (optional)
- ☁️ **Model Hosting (optional)**: Hugging Face Spaces

---

## 📦 Dockerfile Summary

- ✅ Multi-stage builds (backend & frontend)
- ✅ Final backend image < 200MB
- ✅ Static React build served via NGINX
- ✅ CORS configured
- ✅ Model auto-reloads from ./model if present



---

