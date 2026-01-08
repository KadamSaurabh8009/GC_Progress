import ollama
from RAG.vector_store.vector_store import get_qdrant_client, COLLECTION_NAME


def similarity_search(query: str, top_k: int = 3):
    """
    Perform semantic similarity search and return top_k chunks with scores.
    """

    if not query or not query.strip():
        raise ValueError("Query is empty")

    # 1️⃣ Generate embedding for query
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=query
    )
    query_vector = response["embedding"]

    # 2️⃣ Get Qdrant client (local)
    client = get_qdrant_client()

    # 3️⃣ Perform similarity search (LOCAL QDRANT API)
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )

    client.close()

    # 4️⃣ Extract scored points safely
    results = []

    for idx, point in enumerate(response.points, start=1):
        results.append({
            "rank": idx,
            "score": float(point.score),
            "text": point.payload.get("text", "")
        })

    return results
