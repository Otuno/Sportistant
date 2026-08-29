import requests
from models.match import Match
from models.team import Team


class SportsAPIClient:
    """Connect to TheSportsDB API."""

    def __init__(self, api_key: str = "3"):
        self.api_key = api_key
        # Note: Use key '3' or '2' for free tier testing
        self.base_url = f"https://www.thesportsdb.com/api/v1/json/{self.api_key}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

    def search_team(self, team_name: str) -> dict | None:
        """Search for team data by name."""
        try:
            url = f"{self.base_url}/searchteams.php"
            response = requests.get(
                url, params={"t": team_name}, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print(f"API request failed: {e}")
            return None

    def get_team(self, team_name: str) -> Team | None:
        """Fetch team object by team name."""
        data = self.search_team(team_name)
        if not data or not data.get("teams"):
            return None

        raw_team = data["teams"][0]
        return Team(
            team_id=raw_team.get("idTeam"),
            name=raw_team.get("strTeam"),
            sport=raw_team.get("strSport"),
            league=raw_team.get("strLeague"),
            country=raw_team.get("strCountry"),
            city=raw_team.get("strStadiumLocation"),
            stadium=raw_team.get("strStadium"),
            logo_url=raw_team.get("strBadge"),
        )

    def get_previous_matches(self, team_id: str) -> list[Match]:
        """Fetch recent completed matches for a team."""
        try:
            url = f"{self.base_url}/eventslast.php"
            response = requests.get(
                url, params={"id": team_id}, headers=self.headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            results = data.get("results") or []

            matches = []
            for item in results:
                match = Match(
                    match_id=item.get("idEvent"),
                    home_team=item.get("strHomeTeam"),
                    away_team=item.get("strAwayTeam"),
                    date=item.get("dateEvent"),
                    time=item.get("strTime"),
                    league=item.get("strLeague"),
                    venue=item.get("strVenue"),
                    home_score=str(item.get("intHomeScore", "")),
                    away_score=str(item.get("intAwayScore", "")),
                    status=item.get("strStatus"),
                )
                matches.append(match)
            return matches
        except Exception as e:
            print(f"Failed to fetch previous matches: {e}")
            return []