import re


class Validator:
	"""Validate team names and match notes."""

	def is_valid_team_name(self, team_name):
		if not isinstance(team_name, str):
			return False

		team_name = team_name.strip()
		if not team_name:
			return False

		pattern = r"^[A-Za-z0-9 .'-]+$"
		return re.fullmatch(pattern, team_name) is not None

	def is_valid_note(self, note):
		if not isinstance(note, str):
			return False

		note = note.strip()
		if not note or len(note) > 500:
			return False

		return re.search(r"\S", note) is not None
