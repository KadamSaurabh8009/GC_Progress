from RAG.retrival.search import similarity_search

def test_similarity_search():
    results = similarity_search("tax saving", top_k=3)
    assert isinstance(results, list)
