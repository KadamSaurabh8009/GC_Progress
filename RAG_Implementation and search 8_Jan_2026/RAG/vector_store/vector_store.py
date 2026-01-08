from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

COLLECTION_NAME = "rag_collection"
QDRANT_PATH = "./qdrant_db"


def get_qdrant_client():
    return QdrantClient(path=QDRANT_PATH)


def create_collection(vector_size: int):
    client = get_qdrant_client()

    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(COLLECTION_NAME)

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=vector_size,
            distance=Distance.COSINE
        )
    )

    client.close()


def store_vectors(embeddings, texts):
    client = get_qdrant_client()

    points = []
    for i, (vector, text) in enumerate(zip(embeddings, texts)):
        points.append(
            PointStruct(
                id=i,
                vector=vector,
                payload={
                    "chunk_id": i,
                    "text": text
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    client.close()
