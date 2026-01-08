from RAG.embeddings.embedding import generate_embedding

def test_embedding_dimension():
    vector = generate_embedding("Test sentence")
    assert isinstance(vector, list)
    assert len(vector) > 100  # nomic-embed-text ≈ 768
