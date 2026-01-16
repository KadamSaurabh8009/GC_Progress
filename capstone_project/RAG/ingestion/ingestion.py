import pandas as pd
from typing import List, Dict


def load_csv(csv_path: str) -> pd.DataFrame:
    """
    Load the recipe CSV file into a DataFrame.
    """
    return pd.read_csv(csv_path)


def clean_text(text) -> str:
    """
    Minimal text cleaning to preserve semantics.
    """
    if pd.isna(text):
        return ""
    return str(text).strip()


def build_document(row: pd.Series, doc_id: int) -> Dict:
    """
    Convert one CSV row into one rich RAG-ready document.
    """

    recipe_name = clean_text(row.get("TranslatedRecipeName"))
    cuisine = clean_text(row.get("Cuisine"))
    ingredients = clean_text(row.get("TranslatedIngredients"))
    instructions = clean_text(row.get("TranslatedInstructions"))
    total_time = row.get("TotalTimeInMins")
 


    # 🔥 RICH TEXT FOR EMBEDDING + LLM CONTEXT

    full_text = f"""
    Recipe Name: {recipe_name}
    Cuisine: {cuisine}
    Total Cooking Time: {total_time} minutes
    Ingredients:
    {ingredients}
    Instructions:
    {instructions}
    """.strip()

    

    document = {
        "id": doc_id,
        "text": full_text,
        "metadata": {
            "recipe_name": recipe_name,
            "cuisine": cuisine,
            
            
            "total_time": total_time,
            "ingredients": ingredients,
            "instructions": instructions,
            }
    }

    return document


def ingest_recipes(csv_path: str) -> List[Dict]:
    """
    Main ingestion function.
    Reads CSV and returns list of rich documents.
    """
    df = load_csv(csv_path)

    documents: List[Dict] = []
    for idx, row in df.iterrows():
        doc = build_document(row, doc_id=idx)
        documents.append(doc)

    return documents


if __name__ == "__main__":
    # Local sanity test
    docs = ingest_recipes("C:\\Users\\USER\\Desktop\\GC-Progress\\capstone_project\\RAG\\data\\recipes.csv")
    print(f"Total documents created: {len(docs)}")
    print("\nSample document:\n")
    print(docs[0]["text"])
