from PIL import Image
import google.generativeai as genai
from app.config.settings import settings


class GeminiVisionService:
    """
    Uses Gemini Vision to convert a food image into a textual description.
    """

    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-3-flash-preview")

    def describe_image(self, image: Image.Image) -> str:
        """
        Takes a PIL image and returns a natural language description.
        """
        prompt = (
            "Describe this food dish in detail. "
            "Mention ingredients, cuisine type, and cooking style. "
            "Keep it concise but informative."
        )

        response = self.model.generate_content([prompt, image])

        return response.text.strip()
