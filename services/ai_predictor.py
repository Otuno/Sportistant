import os
from datetime import datetime

from services.gemini_service import GeminiService


class AIPredictor:
    """Generate AI-based sports insights from team form and statistics."""

    def __init__(self, gemini_service: GeminiService):
        self.gemini_service = gemini_service
        self.log_file = "data/ai_responses.log"

    def _log_ai_response(self, team_name, form, stat_prediction, response):
        os.makedirs("data", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(self.log_file, "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] Team: {team_name}\n")
            file.write(f"Form: {form}\n")
            file.write(f"Prediction: {stat_prediction}\n")
            file.write(f"AI Response: {response}\n")
            file.write("-" * 50 + "\n")

    def _log_ai_error(self, team_name, error_message):
        os.makedirs("data", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("data/ai_errors.log", "a", encoding="utf-8") as file:
            file.write(f"[{timestamp}] Team: {team_name}\n")
            file.write(f"Error: {error_message}\n")
            file.write("-" * 50 + "\n")

    def generate_ai_insight(
        self,
        team_name: str,
        form: list[str],
        stat_prediction: dict,
    ) -> str:
        """Generate concise commentary about a team's recent form."""
        prompt = (
            f"You are a sports analyst. Provide concise commentary in 2-3 sentences "
            f"about {team_name}'s momentum and upcoming outlook.\n"
            f"Recent form: {form}\n"
            f"Statistical prediction: {stat_prediction}\n"
            "Summarize the team's momentum and likely outlook in a clear, "
            "fan-friendly way."
        )

        try:
            response = self.gemini_service.generate_response(prompt)

            if response is None:
                self._log_ai_error(team_name, "Gemini was unable to return response.")
                return "AI insight is currently unavailable, try again later."

            self._log_ai_response(team_name, form, stat_prediction, response)
            return response

        except OSError as error:
            print(f"Could not write AI response log: {error}")
            return response if "response" in locals() and response else "AI insight is currently unavailable."
        except Exception as error:
            self._log_ai_error(team_name, str(error))
            print(f"AI insight generation failed: {error}")
            return "AI insight is currently unavailable."
