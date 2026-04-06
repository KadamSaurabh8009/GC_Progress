from PIL import Image
import ollama


class VisionService:
    """
    Uses Ollama (LLaVA) to convert a food image into a textual description.
    """

    def __init__(self, model_name: str = "llava"):
        self.model_name = model_name

    def describe_image(self, image: Image.Image) -> str:
        """
        Takes a PIL image and returns a natural language description.
        """

        prompt = (
            "Describe this food dish in detail. "
            "Mention ingredients, cuisine type, and cooking style. "
            "Keep it concise but informative."
        )

        # Convert PIL image to bytes
        import io
        img_bytes = io.BytesIO()
        image.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        response = ollama.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                    "images": [img_bytes]
                }
            ]
        )

        return response["message"]["content"]