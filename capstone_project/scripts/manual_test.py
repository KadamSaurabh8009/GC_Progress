from app.services.query_service import QueryService


def main():
    service = QueryService(top_k=2)

    query = "Quick Indian dinner under 30 minutes"

    print("Running query...")
    response = service.process_query(query)

    print("\nFinal Response:\n")
    print(response)


if __name__ == "__main__":
    main()
