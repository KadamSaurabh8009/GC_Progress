from RAG.ingestion.pdf_loader import load_pdf_text

def test_pdf_loader():
    text = load_pdf_text("RAG/data/tax.pdf")
    assert isinstance(text, str)
    assert len(text) > 0
