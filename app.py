import traceback
import streamlit as st  # type: ignore[import-not-found]
from dotenv import load_dotenv

from analysis.predictor import Predictor
from services.ai_predictor import AIPredictor
from services.gemini_service import GeminiService
from services.match_analyzer import MatchAnalyzer
from services.sports_api import SportsAPIClient
from services.validator import Validator
from storage.json_storage import JSONStorage

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sportistant — Live Match Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- MODERN SPORTS UI CSS ---
st.markdown("""
<style>
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 26px !important;
        font-weight: 700 !important;
        color: #0d6efd !important;
    }
    
    /* Match Scorecard Container */
    .match-card {
        background-color: #f8f9fa;
        border-left: 4px solid #0d6efd;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }
    
    /* Form Badges */
    .badge-w { background-color: #198754; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-d { background-color: #ffc107; color: black; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
    .badge-l { background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- CACHED SERVICES ---
load_dotenv()

@st.cache_resource
def get_services():
    api_client = SportsAPIClient("3")
    storage = JSONStorage("data/favorites.json")
    validator = Validator()
    predictor = Predictor()
    try:
        gemini = GeminiService()
        ai_predictor = AIPredictor(gemini)
    except Exception:
        ai_predictor = None
    return api_client, storage, validator, predictor, ai_predictor

api_client, storage, validator, predictor, ai_predictor = get_services()

# --- SIDEBAR BRANDING ---
with st.sidebar:
    st.markdown("## ⚽ **Sportistant**")
    st.caption("Real-Time AI Sports Companion")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🔍 Team & Match Center", "⭐ Favorite Teams"],
        index=0
    )
    st.markdown("---")
    st.caption("Powered by TheSportsDB & Gemini AI")

# --- POPULAR CLUBS AUTO-SUGGEST LIST ---
POPULAR_TEAMS = [
    "Arsenal", "Aston Villa", "Atlanta United", "Atletico Madrid",
    "Barcelona", "Bayern Munich", "Boca Juniors", "Borussia Dortmund",
    "Chelsea", "Everton", "Flamengo", "Inter Milan", "Juventus",
    "LA Galaxy", "Lazio", "Leicester City", "Liverpool", "Manchester City",
    "Manchester United", "AC Milan", "Napoli", "Newcastle United",
    "Paris Saint-Germain", "Porto", "Real Madrid", "River Plate",
    "Roma", "Sevilla", "Tottenham Hotspur", "Valencia", "Villarreal"
]

# --- MAIN VIEW: TEAM & MATCH CENTER ---
if page == "🔍 Team & Match Center":
    st.title("⚽ Match Center & AI Analytics")
    
    # Selectbox acts as an auto-suggest text input
    # index=None keeps the field empty initially
    selected_team = st.selectbox(
        "Search or select a team",
        options=POPULAR_TEAMS,
        index=None,
        placeholder="Type or select a team name (e.g. arsenal, real madrid...)",
        accept_new_options=True  # Allows users to type custom teams not in the list!
    )

    if selected_team:
        # CASE & WHITESPACE EXCEPTION HANDLING:
        # Convert user input (e.g. "arsenal" or "REAL MADRID") into standard Title Case ("Arsenal", "Real Madrid")
        formatted_team_name = selected_team.strip().title()

        if not validator.is_valid_team_name(formatted_team_name):
            st.warning("Please enter a valid team name.")
            st.session_state["searched_team"] = None
        else:
            # Check if we already loaded this team to avoid duplicate API calls
            if (
                "searched_team" not in st.session_state 
                or st.session_state["searched_team"] is None
                or st.session_state["searched_team"].name.lower() != formatted_team_name.lower()
            ):
                with st.spinner(f"Fetching records for {formatted_team_name}..."):
                    team = api_client.get_team(formatted_team_name)
                    if team is None:
                        st.error("Team not found. Please check spelling.")
                        st.session_state["searched_team"] = None
                    else:
                        st.session_state["searched_team"] = team
    # RENDER TEAM PROFILE & MATCHES
    if "searched_team" in st.session_state and st.session_state["searched_team"] is not None:
        team = st.session_state["searched_team"]
        
        st.markdown("---")
        
        # Header Layout with Official Crest
        col_badge, col_info, col_fav = st.columns([1, 3, 1])
        
        with col_badge:
            if team.logo_url:
                st.image(team.logo_url, width=110)
            else:
                st.markdown("🛡️")
                
        with col_info:
            st.subheader(team.name)
            st.markdown(f"**League:** {team.league or 'N/A'} | **Country:** {team.country or 'N/A'}")
            st.caption(f"📍 **Stadium:** {team.stadium or 'N/A'}")
            
        with col_fav:
            if st.button("⭐ Save Team", use_container_width=True):
                storage.add_favorite_team(team)
                st.toast(f"{team.name} saved to favorites!", icon="⭐")

        st.markdown("---")
        
        # Fetch Recent Matches
        with st.spinner("Loading recent fixtures and computing AI insights..."):
            matches = api_client.get_previous_matches(team.team_id)
            
            if matches:
                analyzer = MatchAnalyzer(matches)
                form = analyzer.get_form(team.name)
                stats = analyzer.count_results(team.name)
                stats["win_percentage"] = analyzer.win_percentage(team.name)
                prediction = predictor.predict(form)

                # Performance Metrics Overview
                st.markdown("### 📊 Form & Statistical Overview")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Win Rate", f"{stats['win_percentage']:.1f}%")
                m2.metric("Wins", stats["wins"])
                m3.metric("Draws", stats["draws"])
                m4.metric("Losses", stats["losses"])

                # Form Badges
                st.markdown("**Recent Form:**")
                form_html = " ".join([
                    f"<span class='badge-w'>W</span>" if item == "W" else
                    f"<span class='badge-d'>D</span>" if item == "D" else
                    f"<span class='badge-l'>L</span>" for item in form
                ])
                st.markdown(form_html, unsafe_allow_html=True)

                st.markdown("---")

                # AI Analysis Callout
                st.markdown("### 🧠 AI Match Analyst Commentary")
                if ai_predictor is not None:
                    insight = ai_predictor.generate_ai_insight(team.name, form, prediction)
                    st.info(insight, icon="🤖")
                else:
                    st.warning("AI commentary unavailable. Check GEMINI_API_KEY environment variable.")

                st.markdown("---")

                # Match History Cards
                st.markdown("### 🏟️ Recent Match Results")
                for m in matches[:5]:
                    score_str = f"{m.home_score} - {m.away_score}" if m.home_score and m.away_score else "VS"
                    st.markdown(
                        f"<div class='match-card'>"
                        f"<strong>{m.home_team}</strong> &nbsp;<code>{score_str}</code>&nbsp; <strong>{m.away_team}</strong><br/>"
                        f"<small style='color: #6c757d;'>📅 {m.date or 'Recent'} | 🏆 {m.league or 'League Match'}</small>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("No recent completed match records found.")

# --- FAVORITES PAGE ---
else:
    st.title("⭐ Favorite Teams")
    favorites = storage.get_favorite_teams()

    if not favorites:
        st.info("No teams saved to favorites yet.")
    else:
        for favorite in favorites:
            if not isinstance(favorite, dict):
                continue

            col_img, col_info, col_btn = st.columns([1, 4, 1])
            with col_img:
                if favorite.get("logo_url"):
                    st.image(favorite["logo_url"], width=60)
            with col_info:
                st.markdown(f"**{favorite.get('name', 'Unknown')}**")
                st.caption(f"{favorite.get('league', 'N/A')} • {favorite.get('country', 'N/A')}")
            with col_btn:
                if st.button("Remove", key=f"remove_{favorite.get('team_id')}"):
                    storage.remove_favorite_team(favorite.get("team_id"))
                    st.toast("Team removed.")
                    st.rerun()
            st.divider()