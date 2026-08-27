# Sportistant Project Instructions

You are assisting with a student Advanced Python project called Sportistant.

Sportistant is a Sports Companion Application.

TECHNOLOGY:
- Python
- Streamlit
- Requests
- JSON
- datetime
- Regular Expressions
- Object-Oriented Programming
- Exception Handling
- Gemini API
- TheSportsDB API

REQUIRED CLASSES:
- Team
- Match
- SportsAPIClient
- MatchAnalyzer

CORE FEATURES:
1. Search for a team.
2. Display team information.
3. Display upcoming fixtures.
4. Display previous results.
5. Display match details.
6. Generate AI pre-match previews.
7. Generate AI post-match summaries.
8. Generate team trivia.
9. Generate fan-friendly analysis.
10. Bookmark favorite teams.
11. Save match notes using JSON.
12. Provide a simple recent-form match prediction.

The prediction must clearly state:
"For fun only — not betting advice."

IMPORTANT DEVELOPMENT RULE:

DO NOT BUILD THE ENTIRE PROJECT AT ONCE.

Build one component at a time.

Recommended order:

1. Project setup
2. Team class
3. Match class
4. SportsAPIClient
5. Test TheSportsDB connection
6. Team search
7. Match retrieval
8. Match details
9. JSON storage
10. Bookmarks
11. Match notes
12. MatchAnalyzer
13. Prediction
14. Gemini integration
15. Streamlit integration
16. Error handling review
17. Testing
18. Documentation

After completing each task:

1. Explain what was built.
2. Explain the important code.
3. Give testing instructions.
4. STOP and wait for confirmation.

CODE STYLE:

Keep the code beginner-friendly.

Do not over-engineer the project.

Do not introduce unnecessary design patterns or advanced concepts.

Do not rewrite working code unnecessarily.

The student must be able to understand and explain the code to a lecturer.

OOP REQUIREMENTS:

Use the required classes meaningfully.

Do not create classes simply to make the project appear more advanced.

FILE HANDLING:

Use JSON files for bookmarks and match notes.

EXCEPTION HANDLING:

Handle realistic errors such as:

- API connection failures
- HTTP errors
- Invalid JSON
- Missing files
- File errors
- Invalid user input
- Gemini API failures
- Missing API data

Prefer specific exceptions instead of unnecessarily using:
except Exception:

REGEX:

Regex must have a meaningful purpose, such as validating user input.

DATETIME:

Use datetime meaningfully for match dates, upcoming fixtures, previous results, and date comparisons.

SECURITY:

Never hard-code API keys.

Use .env.

Never expose API keys in source code.

DEBUGGING:

When code fails:

1. Identify the exact problem.
2. Explain the cause.
3. Make the smallest appropriate fix.
4. Explain why it works.
5. Explain how to test it.

Do not rewrite the entire application to fix a small error.

TESTING:

Test normal cases as well as:

- Empty input
- Invalid input
- Missing data
- API failure
- Invalid JSON
- File errors
- Gemini failure
- Completed matches
- Upcoming matches

PRIORITY:

Functionality > visual complexity

Understanding > code volume

Simple working code > unnecessarily advanced code

Do not claim a feature is complete until it has been tested.