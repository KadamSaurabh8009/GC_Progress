from RAG.ingestion.chunker import chunk_text

def test_chunk_creation():
    text = "This is a test text " * 20
    chunks = chunk_text(text, chunk_size=40, overlap=10)

    assert isinstance(chunks, list)
    assert len(chunks) > 1
