class MatchAnalyzer:
    def __init__(self, matches: list):
        self.matches = matches

    def calculate_goal_difference(self, team_name: str) -> int:
        """OOP Method: Encapsulates goal differential calculation across match objects."""
        total_gf = 0
        total_ga = 0
        for m in self.matches:
            if m.home_team.lower() == team_name.lower():
                total_gf += int(m.home_score or 0)
                total_ga += int(m.away_score or 0)
            elif m.away_team.lower() == team_name.lower():
                total_gf += int(m.away_score or 0)
                total_ga += int(m.home_score or 0)
        return total_gf - total_ga
