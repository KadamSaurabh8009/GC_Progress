from RAG.loader import load_text
from RAG.chunker import chunk_text
from RAG.embedding import generate_embedding
from RAG.vector_store import create_collection, store_vectors

DATA_PATH = "RAG/data.txt"

def main():
    # 1. Load
    text = load_text(DATA_PATH)

    # 2. Chunk
    chunks = chunk_text(text)

    # 3. Embed
    embeddings = [generate_embedding(chunk) for chunk in chunks]

    # 4. Store in Qdrant
    create_collection(len(embeddings[0]))
    store_vectors(embeddings, chunks)

    print("✅ Text + vectors stored successfully in Qdrant!")

if __name__ == "__main__":
    main()
