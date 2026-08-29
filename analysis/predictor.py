class Predictor:
	"""Make a simple prediction from a team's recent form."""

	def predict(self, form):
		if not form:
			return {
				"prediction": "Not enough data",
				"confidence": 0,
			}

		wins = form.count("W")
		draws = form.count("D")
		losses = form.count("L")
		total_matches = len(form)
		win_percentage = wins / total_matches * 100

		if win_percentage >= 60:
			prediction = "Likely to win"
		elif win_percentage >= 40:
			prediction = "Competitive"
		else:
			prediction = "Likely to lose"

		return {
			"prediction": prediction,
			"confidence": round(win_percentage, 2),
			"wins": wins,
			"draws": draws,
			"losses": losses,
		}
