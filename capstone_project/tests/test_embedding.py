from RAG.embeddings.embedding import EmbeddingModel

def test_embedding_output_shape():
    embedder = EmbeddingModel()
    vectors = embedder.embed_texts([
        {"id": 1, "text": "Simple recipe", "metadata": {}}
    ])

    assert len(vectors) == 1
    assert len(vectors[0]["vector"]) == 384  # MiniLM dimension
