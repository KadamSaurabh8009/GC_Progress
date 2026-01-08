from RAG.ingestion.pdf_loader import load_pdf_text
from RAG.ingestion.chunker import chunk_text
from RAG.embeddings.embedding import generate_embedding
from RAG.vector_store.vector_store import create_collection, store_vectors
from RAG.retrival.search import similarity_search

PDF_PATH = "RAG/data/tax.pdf.pdf"


def main():
    # ---------- INGESTION ----------
    print("🔹 Starting PDF ingestion")

    # 1. Load PDF text
    text = load_pdf_text(PDF_PATH)
    if not text.strip():
        print("❌ No text found in PDF")
        return

    print("✅ PDF text loaded")

    # 2. Chunk text
    chunks = chunk_text(text)
    print(f"✅ Total chunks created: {len(chunks)}")

    if not chunks:
        print("❌ No chunks created")
        return

    # Preview first few chunks (useful for large PDFs)
    for i, chunk in enumerate(chunks[:3]):
        print(f"\n🔹 Chunk {i + 1} preview:\n{chunk[:200]}")

    # 3. Generate embeddings
    embeddings = [generate_embedding(chunk) for chunk in chunks]
    print("✅ Embeddings generated")

    # 4. Store in Qdrant
    create_collection(len(embeddings[0]))
    store_vectors(embeddings, chunks)
    print("✅ PDF data stored in Qdrant")

    # ---------- SEARCH ----------
    print("\n🔹 Starting similarity search")

    query = input("Enter your query: ").strip()
    if not query:
        print("❌ Empty query entered")
        return

    results = similarity_search(query, top_k=3)

    print("\n🔍 Top 3 Search Results:")

    if not results:
        print("❌ No matching results found")
        return

    for r in results:
        print("\n-----------------------------")
        print(f"Rank: {r['rank']}")
        print(f"Similarity Score: {r['score']}")
        print(f"Matched Text:\n{r['text'][:300]}")


if __name__ == "__main__":
    main()
