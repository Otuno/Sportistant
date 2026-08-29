import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiService:
    """Connect to the Gemini API."""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set.")

        self.client = genai.Client(api_key=api_key)

    def generate_response(self, prompt):
        """Generate a response using Gemini."""
        try:
            response = self.client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
            )
            return response.text
        except Exception as error:
            print(f"Gemini request failed: {error}")
            return None
