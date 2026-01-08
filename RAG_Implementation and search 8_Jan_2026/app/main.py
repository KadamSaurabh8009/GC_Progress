from fastapi import FastAPI
from app.api import router

app = FastAPI(title="RAG Semantic Search API")

app.include_router(router)
