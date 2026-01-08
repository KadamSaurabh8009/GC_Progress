from fastapi import FastAPI
from pydantic import BaseModel

from RAG.search import similarity_search

app = FastAPI(title="Semantic Search API")

# ---------- Request Schema ----------
class QueryRequest(BaseModel):
    query: str


# ---------- Response Schema ----------
class SearchResponse(BaseModel):
    score: float
    text: str
    vector_first_5: list


# ---------- Search Endpoint ----------
@app.post("/search", response_model=SearchResponse)
def search_endpoint(request: QueryRequest):
    result = similarity_search(request.query)

    if result is None:
        return {
            "score": 0.0,
            "text": "No relevant match found",
            "vector_first_5": []
        }

    return {
        "score": result["score"],
        "text": result["text"],
        "vector_first_5": result["vector"][:5]
    }
