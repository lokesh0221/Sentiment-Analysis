# app.py
import os
import strawberry
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from inference import predict_sentiment
from model_utils import load_model

# Load model
model, tokenizer = load_model()

@strawberry.type
class Prediction:
    label: str
    score: float

@strawberry.type
class Query:
    @strawberry.field
    def sentiment(self, text: str) -> Prediction:
        label, score = predict_sentiment(text, model, tokenizer)
        return Prediction(label=label, score=score)

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

# ✅ FastAPI app
app = FastAPI()

# ✅ CORS middleware (allow frontend to call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"] for tighter security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
