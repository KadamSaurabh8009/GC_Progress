import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GroqLLMService:
    """
    Handles interaction with Groq LLM.
    """

    def __init__(self, model_name: str = "llama-3.1-8b-instant"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")

        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        messages = []

        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })

        messages.append({
            "role": "user",
            "content": prompt
        })

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )

        return response.choices[0].message.content


# ✅ Example usage
if __name__ == "__main__":
    llm = GroqLLMService()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = llm.generate(
            prompt=user_input,
            system_prompt="You are a helpful AI assistant."
        )

        print("AI:", response)