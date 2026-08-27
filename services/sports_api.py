import requests


class SportsAPIClient:
	"""Connect to TheSportsDB API."""

	def __init__(self, api_key):
		self.api_key = api_key
		self.base_url = "https://www.thesportsdb.com/api/v1/json"
