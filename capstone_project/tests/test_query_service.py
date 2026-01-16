from app.services.query_service import QueryService

def test_query_service_flow(mocker):
    service = QueryService()

    service.retriever.retrieve = mocker.Mock(
        return_value=[{
            "recipe_name": "Test",
            "cuisine": "Indian",
            "total_time": 20,
            "content": {}
        }]
    )

    service.llm.generate = mocker.Mock(return_value="Final Answer")

    response = service.process_query("Quick dinner")

    assert response == "Final Answer"
