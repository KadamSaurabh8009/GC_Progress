from sentence_transformers import SentenceTransformer
from typing import List, Dict
from tqdm import tqdm


class EmbeddingModel:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, documents: List[Dict]) -> List[Dict]:
        texts = [doc["text"] for doc in documents]
        embeddings = self.model.encode(texts, batch_size=32, show_progress_bar=True)

        embedded_docs = []

        for doc, vector in zip(documents, embeddings):
            embedded_docs.append({
                "id": doc["id"],
                "text": doc["text"],          # 🔥 KEEP TEXT
                "vector": vector.tolist(),   # 🔥 ADD VECTOR
                "metadata": doc["metadata"]
            })

        return embedded_docs
