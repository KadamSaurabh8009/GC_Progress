from RAG.retriver.retriver import RecipeRetriever
from app.services.llm_service import GeminiLLMService
from app.utils.utils import RAG_PROMPT


class QueryService:
    """
    Orchestrates the complete RAG + LLM flow.
    """

    def __init__(self, top_k: int = 5):
        self.retriever = RecipeRetriever(top_k=top_k)
        self.llm = GeminiLLMService()

    def _build_context(self, retrieved_docs: list) -> str:
        """
        Convert retrieved recipe documents into a clean context
        for the LLM.
        """
        context_blocks = []

        for idx, doc in enumerate(retrieved_docs, start=1):
            block = f"""
Recipe {idx}:
Name: {doc.get("recipe_name")}
Cuisine: {doc.get("cuisine")}
Total Time: {doc.get("total_time")} minutes

Recipe Details:
{doc.get("text", "")}
"""
            context_blocks.append(block.strip())

        return "\n\n".join(context_blocks)

    def process_query(
        self,
        query: str,
        cuisine: str = "Any",
        max_time: int | None = None,
        veg_only: bool = False,
    ) -> str:
        """
        Main entry point used by API.
        Currently filters are accepted but not applied yet.
        """

        # 1. Retrieve relevant recipes (semantic search)
        retrieved_docs = self.retriever.retrieve(
            query=query,
            cuisine=cuisine,
            max_time=max_time,
            veg_only=veg_only,
            )

        if not retrieved_docs:
            return "Sorry, I could not find any relevant recipes."

        # 2. Build context for LLM
        context = self._build_context(retrieved_docs)

        # 3. Build final prompt
        prompt = RAG_PROMPT.format(
            query=query,
            context=context
        )

        # 4. Generate answer using Gemini
        return self.llm.generate(prompt)
