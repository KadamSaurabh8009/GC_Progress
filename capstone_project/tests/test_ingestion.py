from RAG.ingestion.ingestion import build_document

def test_build_document_basic():
    row = {
    "TranslatedRecipeName": "Test Recipe",
    "TranslatedIngredients": "Salt, Water",
    "TranslatedInstructions": "Mix well",
    "Cuisine": "Indian",
    "TotalTimeInMins": 20
}


    doc = build_document(row, doc_id=1)

    assert doc["id"] == 1
    assert "Recipe Name: Test Recipe" in doc["text"]
    assert doc["metadata"]["cuisine"] == "Indian"
