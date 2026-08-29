# ⚽ Sportistant — AI Sports Intelligence Companion

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B.svg?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Gemini AI](https://img.shields.io/badge/Google%20Gemini-AI-8E44AD.svg?style=flat&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Sportistant** is a modern, responsive web application built with Python, Streamlit, and Google Gemini AI. It provides real-time sports team lookup, match result analytics, form tracking, AI-generated match commentary, and local favorites management.

---

## 🌟 Key Features

* **🔍 Team Search & Autocomplete:** Search major global sports teams with case-insensitive fuzzy matching and instant auto-suggestions.
* **📊 Match Analytics Engine:** Calculates win/draw/loss distribution, win percentages, and color-coded recent form indicators (`W` / `D` / `L`).
* **🤖 Gemini AI Commentary:** Dynamically generates tactical match outlooks and expert analyst insights based on team form.
* **🏟️ Official Crests & Scorecards:** Displays high-resolution team badges, stadium details, and clean match result scorecards.
* **⭐ Favorites Management:** Bookmark favorite teams to persistent JSON storage for instant access across user sessions.
* **🧪 Comprehensive Unit Tests:** Robust test suite covering validation logic and statistical match analysis engine.

---

## 🛠️ Architecture & Tech Stack

```text
Sportistant/
├── analysis/
│   ├── __init__.py
│   └── predictor.py          # Rule-based prediction logic
├── data/
│   └── favorites.json        # Persistent JSON storage file
├── models/
│   ├── __init__.py
│   ├── match.py              # Match data class model
│   └── team.py               # Team profile data class model
├── services/
│   ├── __init__.py
│   ├── ai_predictor.py       # AI insight generation coordinator
│   ├── gemini_service.py     # Gemini API integration service
│   ├── match_analyzer.py     # Match stats & form calculation engine
│   ├── sports_api.py         # TheSportsDB API client wrapper
│   └── validator.py          # Input validation & sanitization
├── storage/
│   ├── __init__.py
│   └── json_storage.py       # JSON storage persistence implementation
├── tests/
│   ├── test_match_analyzer.py # Unit tests for MatchAnalyzer
│   └── test_validator.py     # Unit tests for Validator service
├── .env                      # Environment variables configuration
├── .gitignore                # Git ignore rules for editor files
├── app.py                    # Streamlit GUI main entry point
├── requirements.txt          # Python project dependencies
└── README.md                 # Project documentation
```

### Key Technologies Used
* **Frontend / GUI:** [Streamlit](https://streamlit.io/) (Wide layout, metric cards, custom CSS styling)
* **AI Engine:** [Google Gemini API](https://ai.google.dev/) (`google-genai` / `google-generativeai`)
* **Sports API:** [TheSportsDB REST API](https://www.thesportsdb.com/)
* **Persistence:** JSON File Storage Engine
* **Testing:** Python standard `unittest` framework

---

## ⚙️ Quickstart Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/Sportistant.git
cd Sportistant
```

### 2. Create and Activate Virtual Environment
```bash
# On macOS / Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```bash
touch .env
```

Add your Gemini API Key into `.env`:
```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"
```

### 5. Launch the Streamlit App
```bash
streamlit run app.py
```
*The web app will automatically launch in your browser at `http://localhost:8501`.*

---

## 🧪 Running Unit Tests

Run all unit tests using Python's built-in `unittest` runner:

```bash
python -m unittest discover tests
```

Expected output:
```text
......
----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK
```

---

## 👥 Authors & Team Contributions

Cohort 37 - Group 7 - Python Advanced Class
