"""Configuration constants.

Keep this file side-effect free (no Streamlit calls).
"""

DATA_PATH = "data/sih_2025_problem_statements_team_outcomes.csv"

# Session-state keys used by sidebar filters.
FILTER_STATE_KEYS = [
    "year",
    "cat",
    "theme",
    "org",
    "dept",
    "status",
    "state",
    "city",
    "ps",
    "inst",
]
