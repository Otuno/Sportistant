import json
import os


class JSONStorage:
	"""Store favorite teams in a JSON file."""

	def __init__(self, filename):
		self.filename = filename

	def _load_data(self):
		if not os.path.exists(self.filename):
			return {}

		try:
			with open(self.filename, "r") as file:
				return json.load(file)
		except json.JSONDecodeError:
			return {}
		except OSError:
			return {}

	def _save_data(self, data):
		try:
			with open(self.filename, "w") as file:
				json.dump(data, file, indent=4)
		except OSError as error:
			print(f"Error saving data: {error}")

	def add_favorite_team(self, team):
		favorite_team = {
			"team_id": team.team_id,
			"name": team.name,
			"sport": team.sport,
			"league": team.league,
			"country": team.country,
			"city": team.city,
			"stadium": team.stadium,
			"logo_url": team.logo_url,
		}

		data = self._load_data()
		if not isinstance(data, dict):
			data = {}

		favorites = data.get("favorites", [])
		if not isinstance(favorites, list):
			favorites = []

		for favorite in favorites:
			if favorite.get("team_id") == team.team_id:
				return

		favorites.append(favorite_team)
		data["favorites"] = favorites
		self._save_data(data)

	def get_favorite_teams(self):
		data = self._load_data()
		if not isinstance(data, dict):
			return []

		favorites = data.get("favorites", [])
		if not isinstance(favorites, list):
			return []

		return favorites

	def remove_favorite_team(self, team_id):
		data = self._load_data()
		if not isinstance(data, dict):
			data = {}

		favorites = data.get("favorites", [])
		if not isinstance(favorites, list):
			favorites = []

		remaining_favorites = []
		for favorite in favorites:
			if favorite.get("team_id") != team_id:
				remaining_favorites.append(favorite)

		data["favorites"] = remaining_favorites
		self._save_data(data)

	def save_match_note(self, match_id, note):
		data = self._load_data()
		if not isinstance(data, dict):
			data = {}

		notes = data.get("notes", {})
		if not isinstance(notes, dict):
			notes = {}

		match_id = str(match_id)
		if match_id not in notes:
			notes[match_id] = []

		notes[match_id].append(note)
		data["notes"] = notes
		self._save_data(data)

	def get_match_notes(self, match_id):
		data = self._load_data()
		if not isinstance(data, dict):
			return []

		notes = data.get("notes", {})
		if not isinstance(notes, dict):
			return []

		match_notes = notes.get(str(match_id), [])
		if not isinstance(match_notes, list):
			return []

		return match_notes
