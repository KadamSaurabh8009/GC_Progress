from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct


class QdrantVectorStore:
    """
    Handles storage and retrieval of embeddings using Qdrant.
    """

    def __init__(
        self,
        collection_name: str = "recipes_data",
        host: str = "localhost",
        port: int = 6333,
        vector_size: int = 384,
    ):
        self.collection_name = collection_name
        self.vector_size = vector_size

        # Connect to Qdrant
        self.client = QdrantClient(host=host, port=port)

        # Ensure collection exists
        self._create_collection_if_not_exists()

    def _create_collection_if_not_exists(self) -> None:
        """
        Create the collection only if it does not already exist.
        """
        collections = self.client.get_collections().collections
        existing_collection_names = {c.name for c in collections}

        if self.collection_name not in existing_collection_names:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.vector_size,
                    distance=Distance.COSINE,
                ),
            )

    def recreate_collection(self) -> None:
        """
        Recreate the collection (USE ONLY DURING DEVELOPMENT).
        This will delete all existing vectors.
        """
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def store_embeddings(
        self,
        embedded_docs: List[Dict],
        batch_size: int = 100,
    ) -> None:
        """
        Store embedded documents in Qdrant in batches.
        """
        if not embedded_docs:
            return

        for i in range(0, len(embedded_docs), batch_size):
            batch = embedded_docs[i : i + batch_size]
            points: List[PointStruct] = []

            for doc in batch:
                metadata = doc.get("metadata", {})

                payload = {
                    # 🔹 Core searchable / filterable fields
                    "recipe_name": metadata.get("recipe_name"),
                    "cuisine": metadata.get("cuisine"),
                    "course": metadata.get("course"),
                    "diet": metadata.get("diet"),
                    "total_time": metadata.get("total_time"),

                    # 🔹 Rich content for LLM grounding
                    "description": metadata.get("description"),
                    "ingredients": metadata.get("ingredients"),
                    "instructions": metadata.get("instructions"),

                    # 🔹 Optional: full text fallback
                    "full_text": doc.get("text"),
                }

                points.append(
                    PointStruct(
                        id=doc["id"],
                        vector=doc["vector"],
                        payload=payload,
                    )
                )

            self.client.upsert(
                collection_name=self.collection_name,
                points=points,
            )
