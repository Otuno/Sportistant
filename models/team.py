class Team:
	"""Represent a sports team and its basic information."""

	def __init__(
		self,
		team_id,
		name,
		sport,
		league=None,
		country=None,
		city=None,
		stadium=None,
		logo_url=None,
	):
		self.team_id = team_id
		self.name = name
		self.sport = sport
		self.league = league
		self.country = country
		self.city = city
		self.stadium = stadium
		self.logo_url = logo_url

	def display_info(self):
		return (
			f"Team: {self.name}\n"
			f"Sport: {self.sport}\n"
			f"League: {self.league}\n"
			f"Country: {self.country}\n"
			f"Stadium: {self.stadium}"
		)
