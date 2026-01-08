import ollama
from RAG.vector_store import client, COLLECTION_NAME

def similarity_search(query: str):
    if not query.strip():
        raise ValueError("Query is empty")

    # 1. Create query embedding
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )
    query_vector = response["embedding"]

    # 2. Query Qdrant
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=1,
        with_payload=True,
        with_vectors=True
    )

    # 3. Handle QueryResponse correctly
    if not response.points:
        return None

    r = response.points[0]  # ✅ TOP MATCH

    return {
        "score": r.score,
        "text": r.payload.get("text"),
        "vector": r.vector
    }
