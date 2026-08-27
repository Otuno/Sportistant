class Match:
	"""Represent one sports match and its basic information."""

	def __init__(
		self,
		match_id,
		home_team,
		away_team,
		date,
		time,
		league=None,
		venue=None,
		home_score=None,
		away_score=None,
		status=None,
	):
		self.match_id = match_id
		self.home_team = home_team
		self.away_team = away_team
		self.date = date
		self.time = time
		self.league = league
		self.venue = venue
		self.home_score = home_score
		self.away_score = away_score
		self.status = status

	def display_info(self):
		info = (
			f"Home team: {self.home_team}\n"
			f"Away team: {self.away_team}\n"
			f"Date: {self.date}\n"
			f"Time: {self.time}\n"
			f"League: {self.league}\n"
			f"Venue: {self.venue}"
		)

		if self.home_score is not None and self.away_score is not None:
			info += f"\nScore: {self.home_score} - {self.away_score}"

		if self.status is not None:
			info += f"\nStatus: {self.status}"

		return info
