from services.gemini_service import GeminiService


class AIPredictor:
	"""Generate AI-based sports insights from team form and statistics."""

	def __init__(self, gemini_service: GeminiService):
		"""Store the Gemini service used to generate insights."""
		self.gemini_service = gemini_service

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

		response = self.gemini_service.generate_response(prompt)
		if response is None:
			return "AI insight is currently unavailable."

		return response
