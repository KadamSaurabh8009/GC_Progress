from RAG.ingestion.ingestion import ingest_recipes
from RAG.embeddings.embedding import EmbeddingModel
from RAG.vector_store.qdrant_client import QdrantVectorStore


def main():
    print("📥 Loading recipes from CSV...")
    documents = ingest_recipes("RAG/data/recipes.csv")

    print("🧠 Generating embeddings...")
    embedder = EmbeddingModel()
    embedded_docs = embedder.embed_texts(documents)

    print("📦 Storing embeddings in Qdrant...")
    vector_store = QdrantVectorStore(collection_name="recipes_data")
    vector_store.store_embeddings(embedded_docs)

    print("✅ Successfully stored embeddings in Qdrant!")


if __name__ == "__main__":
    main()



