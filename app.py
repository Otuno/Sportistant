import streamlit as st  # type: ignore[import-not-found]
from dotenv import load_dotenv

from analysis.predictor import Predictor
from services.ai_predictor import AIPredictor
from services.gemini_service import GeminiService
from services.match_analyzer import MatchAnalyzer
from services.sports_api import SportsAPIClient
from services.validator import Validator
from storage.json_storage import JSONStorage

st.set_page_config(page_title="Sportistant", page_icon="⚽")

load_dotenv()

# Initialize services
api_client = SportsAPIClient("2")
storage = JSONStorage("data/favorites.json")
validator = Validator()
predictor = Predictor()

try:
    gemini = GeminiService()
    ai_predictor = AIPredictor(gemini)
except Exception:
    ai_predictor = None

st.title("⚽ Sportistant")
st.write("Your personal sports companion.")

page = st.sidebar.radio(
    "Navigate",
    ["🔍 Search & Analyze", "⭐ Favorite Teams"],
)

if page == "🔍 Search & Analyze":
    team_name = st.text_input("Enter Team Name")

    if st.button("Search"):
        if not validator.is_valid_team_name(team_name):
            st.warning("Please enter a valid team name.")
            st.session_state["searched_team"] = None
        else:
            team = api_client.get_team(team_name.strip())
            if team is None:
                st.error("Team not found.")
                st.session_state["searched_team"] = None
            else:
                st.session_state["searched_team"] = team

    # Render searched team data from session state
    if "searched_team" in st.session_state and st.session_state["searched_team"] is not None:
        team = st.session_state["searched_team"]
        st.subheader(team.name)
        info_columns = st.columns(5)

        with info_columns[0]:
            if team.logo_url:
                st.image(team.logo_url, width=100)
        with info_columns[1]:
            st.write(f"**Name**  \n{team.name}")
        with info_columns[2]:
            st.write(f"**League**  \n{team.league or 'Unknown'}")
        with info_columns[3]:
            st.write(f"**Country**  \n{team.country or 'Unknown'}")
        with info_columns[4]:
            st.write(f"**Stadium**  \n{team.stadium or 'Unknown'}")

        if st.button("Add to Favorites"):
            storage.add_favorite_team(team)
            st.success(f"{team.name} added to favorites!")

        st.markdown("---")
        matches = api_client.get_previous_matches(team.team_id)
        if matches:
            analyzer = MatchAnalyzer(matches)
            form = analyzer.get_form(team.name)
            stats = analyzer.count_results(team.name)
            stats["win_percentage"] = analyzer.win_percentage(team.name)
            prediction = predictor.predict(form)

            st.write("### Form & Stats")
            metrics = st.columns(4)
            metrics[0].metric("Win %", f"{stats['win_percentage']:.2f}%")
            metrics[1].metric("Wins", stats["wins"])
            metrics[2].metric("Draws", stats["draws"])
            metrics[3].metric("Losses", stats["losses"])

            st.write("### AI Match Insight")
            if ai_predictor is not None:
                insight = ai_predictor.generate_ai_insight(
                    team.name,
                    form,
                    prediction,
                )
                st.info(insight)
            else:
                st.warning("AI commentary is unavailable.")
        else:
            st.info("No previous matches found.")

else:
    st.subheader("Favorite Teams")
    favorites = storage.get_favorite_teams()

    if not favorites:
        st.info("No favorite teams saved yet.")
    else:
        for favorite in favorites:
            if not isinstance(favorite, dict):
                continue

            columns = st.columns([1, 4, 1])
            with columns[0]:
                if favorite.get("logo_url"):
                    st.image(favorite["logo_url"], width=70)
            with columns[1]:
                st.write(f"**{favorite.get('name', 'Unknown team')}**")
                st.write(
                    f"{favorite.get('league') or 'Unknown league'} | "
                    f"{favorite.get('country') or 'Unknown country'}"
                )
            with columns[2]:
                if st.button("Remove", key=f"remove_{favorite.get('team_id')}"):
                    storage.remove_favorite_team(favorite.get("team_id"))
                    st.success("Team removed from favorites.")
                    st.rerun()