from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

client = QdrantClient(path="./qdrant_db")

COLLECTION_NAME = "rag_collection"

def create_collection(vector_size: int):
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config={
            "": VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        }
    )

def store_vectors(embeddings, texts):
    points = []
    for i, (vector, text) in enumerate(zip(embeddings, texts)):
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={"text": text}
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
