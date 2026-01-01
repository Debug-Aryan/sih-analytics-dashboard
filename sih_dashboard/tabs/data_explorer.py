from __future__ import annotations

import pandas as pd
import streamlit as st


def render(df: pd.DataFrame) -> None:
    """Render the Data Explorer tab for flexible, user-driven exploration."""

    st.header("🔬 Interactive Data Explorer")


    if df.empty:
        st.warning("No records match the current filter configuration.")
        return

    st.info(f"**Current Dataset View:** {len(df):,} records × {len(df.columns)} attributes")

    all_columns = df.columns.tolist()
    default_columns = [
        "edition_year",
        "ps_id",
        "problem_statement_title",
        "category",
        "team_name",
        "status",
        "prize_money",
        "institute_name",
        "institute_state",
    ]
    default_columns = [c for c in default_columns if c in all_columns]

    selected_columns = st.multiselect(
        "Select Data Attributes to Display",
        options=all_columns,
        default=default_columns,
    )

    if not selected_columns:
        st.warning("At least one data attribute must be selected for display.")
        return

    display_df = df[selected_columns].copy()

    st.divider()

    # ---------------- Row-level Filters ----------------
    col1, col2 = st.columns(2)

    with col1:
        status_order = ["Winner", "Joint Winner", "Shortlisted", "Waitlist"]
        available_status = [s for s in status_order if s in df["status"].unique()]

        status_filter = st.multiselect(
            "Filter by Team Status",
            options=available_status,
            default=[],
        )

    with col2:
        if "prize_money" in display_df.columns:
            min_prize = st.number_input(
                "Minimum Prize Amount (₹) — Awarded Teams Only",
                min_value=0,
                value=0,
                step=50000,
            )
        else:
            min_prize = None

    if status_filter:
        display_df = display_df[display_df["status"].isin(status_filter)]

    if min_prize is not None and "prize_money" in display_df.columns:
        display_df = display_df[
            (display_df["prize_money"].fillna(0) >= min_prize)
        ]

    st.divider()

    # ---------------- Sorting ----------------
    col1, col2 = st.columns([3, 1])

    with col1:
        sort_column = st.selectbox("Sort Records By", options=selected_columns)

    with col2:
        sort_order = st.radio(
            "Sort Order",
            options=["Ascending", "Descending"],
            horizontal=True,
        )

    ascending = sort_order == "Ascending"

    if sort_column:
        display_df = display_df.sort_values(
            by=sort_column,
            ascending=ascending,
            na_position="last",
        )

    st.subheader("📄 Filtered Dataset Preview")

    # ---------------- Display ----------------
    st.dataframe(
        display_df,
        width="stretch",
        height=520,
        column_config={
            "prize_money": st.column_config.NumberColumn(
                "Prize Money (₹)", format="₹%,.0f"
            )
        }
        if "prize_money" in display_df.columns
        else None,
    )

    # ---------------- Download ----------------
    st.divider()

    csv = display_df.to_csv(index=False).encode("utf-8")

    years = sorted(df["edition_year"].unique()) if "edition_year" in df.columns else []
    year_part = (
        f"{years[0]}-{years[-1]}" if len(years) > 1 else str(years[0]) if years else "unknown"
    )

    filename = f"sih_{year_part}_filtered_dataset_{len(display_df)}_records.csv"

    st.download_button(
        "📥 Download Filtered Dataset (CSV)",
        data=csv,
        file_name=filename,
        mime="text/csv",
        width="stretch",
    )
