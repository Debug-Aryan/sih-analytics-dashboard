"""Smart India Hackathon Dashboard (modular).

Entry point only:
- Page config + global CSS
- Data load + validation
- Sidebar filters
- Tab routing

Run:
  streamlit run app.py
"""

from __future__ import annotations

import streamlit as st

from sih_dashboard.tabs import (
    about_dataset,
    data_explorer,
    institutes_geography,
    overview,
    problem_statements,
    teams_status,
)
from sih_dashboard.utils.config import DATA_PATH
from sih_dashboard.utils.data import load_data, validate_required_columns
from sih_dashboard.utils.filters import render_sidebar_filters
from sih_dashboard.utils.styles import inject_global_css


st.set_page_config(
    page_title="Smart India Hackathon — Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)


def main() -> None:
    inject_global_css()

    st.title("🏆 Smart India Hackathon — Analytics Dashboard")
    st.markdown("**Analytical insights into problem statements, team participation, and competition outcomes**")
    st.divider()

    try:
        df = load_data(DATA_PATH)
    except Exception as exc:
        st.error(f"Failed to load dataset. Details: {exc}")
        return

    # Expanded required columns to safely support all tabs
    required_columns = {
        "edition_year",
        "ps_id",
        "problem_statement_title",
        "category",
        "theme",
        "organization",
        "department",
        "team_id",
        "status",
        "prize_money",
        "total_submission",
        "max_submission",
        "institute_name",
        "institute_city",
        "institute_state",
    }

    missing = validate_required_columns(df, required_columns)
    if missing:
        st.error(f"The dataset is missing required columns needed for analysis: {missing}")

        return

    filtered_df = render_sidebar_filters(df)

    # Correct winner logic (status-based, not prize_money-based)
    winner_count = filtered_df[
        filtered_df["status"].isin(['Winner', 'Joint Winner', 'Consolation Prize', 'Third Prize',
       'Second Prize', 'Future Innovators Award', 'First Prize',
       'Girls Achiever Award', 'Quantum Frontier Award'])
    ].shape[0]

    st.markdown(
        f"""
        **Current Dataset Context:**  
        - Total Team Submissions: `{len(filtered_df)}`  
        - Participating Institutes: `{filtered_df['institute_name'].nunique()}`  
        - Teams with Declared Awards: `{winner_count}`
        """
    )
    st.divider()

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "📊 Overview",
            "🧩 Problem Statements",
            "🏫 Institutes & Geography",
            "👥 Teams & Outcomes",
            "🔬 Data Explorer",
            "📖 About Dataset",
        ]
    )

    with tab1:
        overview.render(filtered_df)

    with tab2:
        problem_statements.render(filtered_df)

    with tab3:
        institutes_geography.render(filtered_df)

    with tab4:
        teams_status.render(filtered_df)

    with tab5:
        data_explorer.render(filtered_df)

    with tab6:
        about_dataset.render()


if __name__ == "__main__":
    main()
