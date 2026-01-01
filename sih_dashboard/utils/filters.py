"""Sidebar filters.

Note: session_state is global in Streamlit; shared keys work across tabs.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from .config import FILTER_STATE_KEYS


FILTER_DEFAULTS: dict[str, object] = {
    "year": [],
    "cat": [],
    "theme": [],
    "org": [],
    "dept": [],
    "status": [],
    "state": [],
    "city": [],
    "ps": "",
    "inst": "",
}


def reset_filters() -> None:
    # Setting explicit defaults clears the frontend "tag" UI reliably.
    # Deleting keys can be repopulated from the browser widget state on rerun.
    for key in FILTER_STATE_KEYS:
        st.session_state[key] = FILTER_DEFAULTS.get(key, None)


def _coerce_multiselect_state_to_options(key: str, options: list) -> None:
    """Ensure stored multiselect values are valid for current options.

    Streamlit multiselect can behave oddly when options are dynamic; keeping
    session_state values in-sync avoids stale "tag" chips.
    """
    if key not in st.session_state:
        return
    current = st.session_state.get(key)
    if not current:
        return
    if not isinstance(current, list):
        current = [current]
    options_set = set(options)
    cleaned = [v for v in current if v in options_set]
    if cleaned != current:
        st.session_state[key] = cleaned


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("🔍 Filters")

    st.sidebar.button(
        "🔄 Reset Filters",
        width="stretch",
        on_click=reset_filters,
    )

    filtered_df = df.copy()

    # ---- Core Filters ----
    st.sidebar.subheader("📌 Core")

    years = sorted(filtered_df["edition_year"].unique())
    if len(years) <= 1:
        # With a single available year, a multiselect can look "stuck".
        # Show an indicator instead (no tags), and treat it as unfiltered.
        st.sidebar.selectbox(
            "Edition Year",
            years,
            index=0 if years else None,
            disabled=True,
            key="_year_single",
        )
        selected_years: list = []
    else:
        _coerce_multiselect_state_to_options("year", years)
        selected_years = st.sidebar.multiselect("Edition Year", years, key="year")
        if selected_years:
            filtered_df = filtered_df[filtered_df["edition_year"].isin(selected_years)]

    categories = sorted(filtered_df["category"].unique())
    _coerce_multiselect_state_to_options("cat", categories)
    selected_categories = st.sidebar.multiselect("Category", categories, key="cat")
    if selected_categories:
        filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

    themes = sorted(filtered_df["theme"].unique())
    _coerce_multiselect_state_to_options("theme", themes)
    selected_themes = st.sidebar.multiselect("Theme", themes, key="theme")
    if selected_themes:
        filtered_df = filtered_df[filtered_df["theme"].isin(selected_themes)]

    # ---- Organization ----
    st.sidebar.subheader("🏛 Organization")

    organizations = sorted(filtered_df["organization"].unique())
    _coerce_multiselect_state_to_options("org", organizations)
    selected_orgs = st.sidebar.multiselect("Organization", organizations, key="org")
    if selected_orgs:
        filtered_df = filtered_df[filtered_df["organization"].isin(selected_orgs)]

    departments = sorted(filtered_df["department"].unique())
    _coerce_multiselect_state_to_options("dept", departments)
    selected_depts = st.sidebar.multiselect("Department", departments, key="dept")
    if selected_depts:
        filtered_df = filtered_df[filtered_df["department"].isin(selected_depts)]

    # ---- Outcome ----
    st.sidebar.subheader("🏆 Outcome")

    statuses = sorted(filtered_df["status"].unique())
    _coerce_multiselect_state_to_options("status", statuses)
    selected_statuses = st.sidebar.multiselect("Status", statuses, key="status")
    if selected_statuses:
        filtered_df = filtered_df[filtered_df["status"].isin(selected_statuses)]

    # ---- Geography ----
    st.sidebar.subheader("🌍 Geography")

    states = sorted(filtered_df["institute_state"].unique())
    _coerce_multiselect_state_to_options("state", states)
    selected_states = st.sidebar.multiselect("Institute State", states, key="state")
    if selected_states:
        filtered_df = filtered_df[filtered_df["institute_state"].isin(selected_states)]

    cities = sorted(filtered_df["institute_city"].unique())
    _coerce_multiselect_state_to_options("city", cities)
    selected_cities = st.sidebar.multiselect("Institute City", cities, key="city")
    if selected_cities:
        filtered_df = filtered_df[filtered_df["institute_city"].isin(selected_cities)]

    # ---- Search ----
    st.sidebar.subheader("🔎 Search")

    ps_search = st.sidebar.text_input("Problem Statement Title", key="ps")
    if ps_search:
        filtered_df = filtered_df[
            filtered_df["problem_statement_title"].str.contains(ps_search, case=False, na=False)
        ]

    institute_search = st.sidebar.text_input("Institute Name", key="inst")
    if institute_search:
        filtered_df = filtered_df[
            filtered_df["institute_name"].str.contains(institute_search, case=False, na=False)
        ]

    st.sidebar.divider()
    st.sidebar.metric("📊 Filtered Records", f"{len(filtered_df):,}")

    return filtered_df
