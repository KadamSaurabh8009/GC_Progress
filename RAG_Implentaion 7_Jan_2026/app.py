from RAG.pdf_loader import load_pdf_text
from RAG.chunker import chunk_text
from RAG.embedding import generate_embedding
from RAG.vector_store import create_collection, store_vectors, client
from RAG.search import similarity_search

PDF_PATH = "RAG/data.pdf"

def main():
    # ---------- INGESTION ----------
    print("🔹 Starting PDF ingestion")

    # 1. Load PDF text
    text = load_pdf_text(PDF_PATH)
    if not text.strip():
        print("❌ No text found in PDF")
        client.close()
        return
    print("✅ PDF text loaded")

    # 2. Chunk text
    chunks = chunk_text(text)
    print(f"✅ Total chunks created: {len(chunks)}")

    if not chunks:
        print("❌ No chunks created")
        client.close()
        return

    # 3. Generate embeddings
    embeddings = []
    for chunk in chunks:
        embeddings.append(generate_embedding(chunk))
    print("✅ Embeddings generated")

    # 4. Store in Qdrant
    create_collection(len(embeddings[0]))
    store_vectors(embeddings, chunks)
    print("✅ PDF data stored in Qdrant")

   # ---------- SEARCH ----------
    print("\n🔹 Starting similarity search")

    query = input("Enter your query: ").strip()

    if not query:
        print("❌ Empty query entered. Please type a question.")
        client.close()
        return
    
    result = similarity_search(query)
    print("\n🔍 Search Result (Top Match):")
   
    if result is None:
        print("❌ No matching result found.")
    else:
        print("Similarity Score:", result["score"])
        print("Matched Text:", result["text"][:200])
        print("Vector first 5 values:", result["vector"][:5])

    # ---------- CLEANUP ----------
    client.close()
    print("\n✅ Qdrant client closed cleanly")


if __name__ == "__main__":
    main()
