import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiLLMService:
    """
    Handles interaction with Gemini LLM.
    """

    def __init__(self, model_name: str = "gemini-3-flash-preview"):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
