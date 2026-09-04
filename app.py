import streamlit as st
from services.sports_api import SportsAPIClient
from services.match_analyzer import MatchAnalyzer
from services.validator import Validator
from storage.json_storage import JSONStorage
from services.gemini_service import GeminiService
from services.ai_predictor import AIPredictor

# 1. Page Configuration
st.set_page_config(page_title="Sportistant", page_icon="⚽", layout="wide")
st.title("⚽ Sportistant — AI Sports Intelligence")

# 2. Service Initialization with Defensive Error Handling
api_client = SportsAPIClient()
storage = JSONStorage()

try:
    gemini = GeminiService()
    ai_predictor = AIPredictor(gemini)
except Exception:
    ai_predictor = None

# 3. Sidebar Configuration
st.sidebar.header("⭐ Favorite Teams")
try:
    favorites = storage.get_favorite_teams()
    for fav in favorites:
        st.sidebar.write(f"- **{fav.get('name')}**")
except Exception:
    st.sidebar.warning("Unable to load saved favorites.")

POPULAR = ["Arsenal", "Real Madrid", "Barcelona", "Chelsea", "Liverpool", "Manchester City"]

# 4. Search Input Form
with st.form("search_form"):
    col1, col2 = st.columns([3, 1])
    with col1:
        team_input = st.selectbox("Search Team:", options=POPULAR, accept_new_options=True)
    with col2:
        st.write("")
        st.write("")
        submitted = st.form_submit_button("Search")

# 5. Search Logic, Input Sanitization, & UI Rendering
if submitted and team_input:
    clean_name = team_input.strip().title()

    # Step A: Validate input using Regex via Validator class
    if not Validator.is_valid_team_name(clean_name):
        st.error("Invalid team name. Please enter 2 to 50 valid alphanumeric characters.")
    else:
        # Step B: Safe API call to search team
        try:
            team = api_client.search_team(clean_name)
        except Exception:
            team = None
            st.error("A network error occurred while fetching team data.")

        if not team:
            st.error("Team not found. Please check spelling and try again.")
        else:
            # Render Team Profile Header
            c1, c2 = st.columns([1, 4])
            with c1:
                if team.logo_url:
                    st.image(team.logo_url, width=120)
            with c2:
                st.subheader(team.name)
                st.write(f"🏆 {team.league} | 🌍 {team.country} | 🏟️ {team.stadium}")
                if st.button("⭐ Save Favorite"):
                    if storage.add_favorite({"name": team.name, "league": team.league}):
                        st.success("Saved to favorites!")
                    else:
                        st.info("Team is already in your favorites.")

            # Step C: Safe API call to fetch recent matches & render metrics
            try:
                matches = api_client.get_recent_matches(team.team_id)
            except Exception:
                matches = []
                st.warning("Could not retrieve recent match records.")

            if matches:
                analyzer = MatchAnalyzer(matches)
                form_list = analyzer.get_form(team.name)
                win_pct = analyzer.win_percentage(team.name)
                counts = analyzer.count_results(team.name)

                # Render Metric Cards
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Win Rate", f"{win_pct}%")
                m2.metric("Wins", counts["wins"])
                m3.metric("Draws", counts["draws"])
                m4.metric("Losses", counts["losses"])

                # Render AI Tactical Commentary
                if ai_predictor:
                    try:
                        commentary = ai_predictor.analyze_team_outlook(team.name, form_list, win_pct)
                        st.info(commentary)
                    except Exception:
                        st.warning("AI commentary unavailable at this moment.")

                # Render Scorecards
                st.subheader("🏟️ Recent Fixture Scorecards")
                for match in matches:
                    st.markdown(
                        f"**{match.date}** | {match.home_team} "
                        f"**{match.home_score} - {match.away_score}** "
                        f"{match.away_team}"
                    )
