from models.match import Match


class MatchAnalyzer:
	"""Analyze completed matches for a team."""

	def __init__(self, matches: list[Match]):
		self.matches = matches

	def get_result(self, match: Match, team_name):
		"""Return W, D, or L for a team in a completed match."""
		if match.home_score is None or match.away_score is None:
			return None

		if team_name == match.home_team:
			if match.home_score > match.away_score:
				return "W"
			if match.home_score == match.away_score:
				return "D"
			return "L"

		if team_name == match.away_team:
			if match.away_score > match.home_score:
				return "W"
			if match.away_score == match.home_score:
				return "D"
			return "L"

		return None

	def get_form(self, team_name):
		"""Return completed match results for a team."""
		form = []

		for match in self.matches:
			result = self.get_result(match, team_name)
			if result is not None:
				form.append(result)

		return form

	def count_results(self, team_name):
		"""Count wins, draws, and losses for a team."""
		form = self.get_form(team_name)
		results = {
			"wins": 0,
			"draws": 0,
			"losses": 0,
		}

		for result in form:
			if result == "W":
				results["wins"] += 1
			elif result == "D":
				results["draws"] += 1
			elif result == "L":
				results["losses"] += 1

		return results

	def win_percentage(self, team_name):
		"""Return the team's win percentage in completed matches."""
		form = self.get_form(team_name)

		if len(form) == 0:
			return 0

		results = self.count_results(team_name)
		return results["wins"] / len(form) * 100
