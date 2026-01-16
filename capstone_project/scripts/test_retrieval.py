from RAG.retriver.retriver import RecipeRetriever


def main():
    retriever = RecipeRetriever(top_k=3)

    query = "Quick Indian dinner under 30 minutes"
    print(f"\n🔎 Query: {query}\n")

    results = retriever.retrieve(query)

    

    for idx, res in enumerate(results, start=1):
        print(f"\n{idx}. {res['recipe_name']} | Score: {res['score']:.4f}")
        print(f"Cuisine: {res['cuisine']}")
        print(f"Total Time: {res['total_time']} mins")
        
        print("\nIngredients:")
        print(res["content"].get("ingredients", "N/A"))
        
        print("\nInstructions:")
        print(res["content"].get("instructions", "N/A"))


if __name__ == "__main__":
    main()
