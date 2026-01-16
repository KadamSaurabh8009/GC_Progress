from RAG.retriver.retriver import RecipeRetriever
from unittest.mock import MagicMock

def test_retriever_returns_results(mocker):
    retriever = RecipeRetriever()

    mock_response = MagicMock()
    mock_response.points = []

    retriever.vector_store.client.query_points = MagicMock(
        return_value=mock_response
    )

    results = retriever.retrieve("Indian dinner")

    assert isinstance(results, list)
