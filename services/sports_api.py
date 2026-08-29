import requests

from models.match import Match
from models.team import Team


class SportsAPIClient:
	"""Connect to TheSportsDB API."""

	def __init__(self, api_key):
		self.api_key = api_key
		self.base_url = "https://www.thesportsdb.com/api/v1/json"

	def search_team(self, team_name):
		url = f"{self.base_url}/{self.api_key}/searchteams.php"

		try:
			response = requests.get(url, params={"t": team_name}, timeout=10)
			response.raise_for_status()
			return response.json()
		except requests.exceptions.RequestException as error:
			print(f"API request failed: {error}")
			return None
		except ValueError as error:
			print(f"Invalid JSON response: {error}")
			return None

	def get_team(self, team_name):
		result = self.search_team(team_name)

		if not result or not result.get("teams"):
			return None

		team_data = result["teams"][0]
		return Team(
			team_id=team_data.get("idTeam"),
			name=team_data.get("strTeam"),
			sport=team_data.get("strSport"),
			league=team_data.get("strLeague"),
			country=team_data.get("strCountry"),
			city=team_data.get("strLocation"),
			stadium=team_data.get("strStadium"),
			logo_url=team_data.get("strBadge"),
		)

	def get_upcoming_matches(self, team_id):
		url = f"{self.base_url}/{self.api_key}/eventsnext.php?id={team_id}"

		try:
			response = requests.get(url, timeout=10)
			response.raise_for_status()
			result = response.json()
		except requests.exceptions.RequestException as error:
			print(f"API request failed: {error}")
			return []
		except ValueError as error:
			print(f"Invalid JSON response: {error}")
			return []

		events = result.get("results") if result else None
		if not events:
			return []

		matches = []
		for event in events:
			matches.append(
				Match(
					match_id=event.get("idEvent"),
					home_team=event.get("strHomeTeam"),
					away_team=event.get("strAwayTeam"),
					date=event.get("dateEvent"),
					time=event.get("strTime"),
					league=event.get("strLeague"),
					venue=event.get("strVenue"),
					home_score=int(event["intHomeScore"]) if event.get("intHomeScore") is not None else None,
					away_score=int(event["intAwayScore"]) if event.get("intAwayScore") is not None else None,
					status=event.get("strStatus"),
				)
			)

		return matches

	def get_previous_matches(self, team_id):
		url = f"{self.base_url}/{self.api_key}/eventslast.php?id={team_id}"

		try:
			response = requests.get(url, timeout=10)
			response.raise_for_status()
			result = response.json()
		except requests.exceptions.RequestException as error:
			print(f"API request failed: {error}")
			return []
		except ValueError as error:
			print(f"Invalid JSON response: {error}")
			return []

		events = result.get("results") if result else None
		if not events:
			return []

		matches = []
		for event in events:
			matches.append(
				Match(
					match_id=event.get("idEvent"),
					home_team=event.get("strHomeTeam"),
					away_team=event.get("strAwayTeam"),
					date=event.get("dateEvent"),
					time=event.get("strTime"),
					league=event.get("strLeague"),
					venue=event.get("strVenue"),
					home_score=int(event["intHomeScore"]) if event.get("intHomeScore") is not None else None,
					away_score=int(event["intAwayScore"]) if event.get("intAwayScore") is not None else None,
					status=event.get("strStatus"),
				)
			)

		return matches
