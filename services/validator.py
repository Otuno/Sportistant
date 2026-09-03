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

	
		@staticmethod
		def is_valid_team_name(name: str) -> bool:
			"""Uses Regex to validate team names (letters, numbers, spaces, hyphens; min 2 chars)."""
			if not name or not isinstance(name, str):
				return False
			pattern = r"^[A-Za-z0-9\s\-]{2,50}$"
			return bool(re.match(pattern, name.strip()))
	 
		@staticmethod
		def parse_score(score_str: str) -> tuple:
			"""Uses Regex to extract numerical scores from strings like '2-1' or '3:0'."""
			match = re.search(r"^(\d+)\s*[-:]\s*(\d+)$", score_str.strip())
			if match:
				return int(match.group(1)), int(match.group(2))
			return None
	
		@staticmethod
		def is_valid_date(date_str: str) -> bool:
			"""Uses Regex to validate ISO dates (YYYY-MM-DD)."""
			pattern = r"^\d{4}-\d{2}-\d{2}$"
			return bool(re.match(pattern, date_str.strip()))
