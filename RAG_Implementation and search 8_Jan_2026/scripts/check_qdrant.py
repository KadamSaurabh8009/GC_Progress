from qdrant_client import QdrantClient

client = QdrantClient(path="./qdrant_db")
COLLECTION_NAME = "rag_collection"

info = client.get_collection(COLLECTION_NAME)
print("Total vectors stored:", info.points_count)

# Retrieve all points
points = client.retrieve(
    collection_name=COLLECTION_NAME,
    ids=list(range(info.points_count)),
    with_vectors=True
)

for p in points:
    print("\n--------------------")
    print("Text Chunk:")
    print(p.payload["text"][:150])
    print("Vector length:", len(p.vector))
    print("Vector first 5 values:", p.vector[:5])

client.close()
