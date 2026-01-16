from typing import List, Dict, Any
from qdrant_client.models import (
    ScoredPoint,
    Filter,
    FieldCondition,
    MatchValue,
    Range,
)
from RAG.embeddings.embedding import EmbeddingModel
from RAG.vector_store.qdrant_client import QdrantVectorStore


class RecipeRetriever:
    def __init__(self, collection_name: str = "recipes_data", top_k: int = 5):
        self.top_k = top_k
        self.embedder = EmbeddingModel()
        self.vector_store = QdrantVectorStore(collection_name=collection_name)

    def retrieve(
        self,
        query: str,
        cuisine: str = "Any",
        max_time: int | None = None,
        veg_only: bool = False,
    ) -> List[Dict[str, Any]]:
        # 1. Embed query
        query_vector = self.embedder.model.encode(query).tolist()

        # 2. Build Qdrant metadata filters
        filter_conditions = []

        # Cuisine filter
        if cuisine and cuisine != "Any":
            filter_conditions.append(
                FieldCondition(
                    key="cuisine",
                    match=MatchValue(value=cuisine),
                )
            )

        # Max cooking time filter
        if max_time is not None:
            filter_conditions.append(
                FieldCondition(
                    key="total_time",
                    range=Range(lte=max_time),
                )
            )

        qdrant_filter = (
            Filter(must=filter_conditions) if filter_conditions else None
        )

        # 3. Query Qdrant
        response = self.vector_store.client.query_points(
            collection_name=self.vector_store.collection_name,
            query=query_vector,
            limit=self.top_k,
            with_payload=True,
            query_filter=qdrant_filter,
        )

        hits = response.points if hasattr(response, "points") else response

        results: List[Dict[str, Any]] = []

        for hit in hits:
            if not isinstance(hit, ScoredPoint):
                continue

            payload = hit.payload or {}

            results.append({
                "id": hit.id,
                "score": float(hit.score),
                "recipe_name": payload.get("recipe_name"),
                "cuisine": payload.get("cuisine"),
                "total_time": payload.get("total_time"),
                "text": payload.get("full_text") or payload.get("text", ""),
            })

        return results
