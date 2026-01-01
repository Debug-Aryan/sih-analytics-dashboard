from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Modern color schemes
COLOR_SCHEMES = {
    'status': ['#667eea', '#f093fb', '#ffeaa7', '#ff6b6b', '#4ecdc4'],
    'gradient_gold': ['#f7b733', '#fc4a1a'],
    'gradient_teal': ['#11998e', '#38ef7d'],
    'vibrant': ['#f857a6', '#ff5858', '#fdbb2d', '#22c1c3', '#667eea'],
}

DONUT_COLORS = [
    "#2563EB",  # Blue
    "#7C3AED",  # Purple
    "#10B981",  # Emerald
    "#F59E0B",  # Amber
    "#EF4444",  # Red
    "#0EA5E9",  # Sky
    "#14B8A6",  # Teal
]

# Chart layout template
CHART_LAYOUT = {
    # Transparent backgrounds (blend with Streamlit dark UI)
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',

    # Global font (dark-theme readable)
    'font': {
        'family': 'Inter, system-ui, sans-serif',
        'size': 12,
        'color': '#E6F1FF'
    },

    # ⬇ Increased right margin to avoid number clipping
    'margin': {
        'l': 60,
        'r': 140,   # FIX: was too small (40)
        't': 60,
        'b': 40},

    # ⬇ Dark-theme hover tooltip (NO white box)
    'hoverlabel': {
        'bgcolor': 'rgba(15, 23, 42, 0.95)',  # dark navy
        'bordercolor': '#4DA3FF',             # subtle accent
        'font': {
            'family': 'Inter, system-ui, sans-serif',
            'size': 13,
            'color': '#E6F1FF'
        }
    },
}



def truncate_text(text: str, max_length: int = 40) -> str:
    """Truncate long text and add ellipsis."""
    text_str = str(text)
    if len(text_str) > max_length:
        return text_str[:max_length] + "..."
    return text_str


def render(df: pd.DataFrame) -> None:
    """Render Teams & Outcome analysis tab (dataset-aligned)."""

    st.header("👥 Teams & Outcomes — Performance Analysis")

    if df.empty:
        st.warning("No team records match the current filter criteria.")
        return

    df = df.copy()

    # ---- Canonical outcome definition ----
    df["is_winner"] = df["status"].isin(['Winner', 'Joint Winner', 'Consolation Prize', 'Third Prize', 'Second Prize', 'Future Innovators Award', 'First Prize',
       'Girls Achiever Award', 'Quantum Frontier Award'])

    total_teams = df["team_id"].nunique()
    winning_teams = df[df["is_winner"]]["team_id"].nunique()
    win_rate = (winning_teams / total_teams) * 100 if total_teams else 0

    total_prize = df.loc[df["is_winner"], "prize_money"].sum(skipna=True)

    # ---- Enhanced Top-level metrics with gradient cards ----
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(5, 150, 105, 0.25);">
                <div style="font-size: 2rem;">👥</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{total_teams:,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Total Participating Teams</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #4C1D95 0%, #7C3AED 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(124, 58, 237, 0.25);">
                <div style="font-size: 2rem;">🏆</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{winning_teams:,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Teams With Declared Awards</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25);">
                <div style="font-size: 2rem;">📊</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{win_rate:.2f}%</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Award Conversion Rate</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #78350F 0%, #D97706 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(217, 119, 6, 0.25);">
                <div style="font-size: 2rem;">🏦</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">₹{total_prize:,.0f}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Total Prize Amount Distributed</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    # ---- Enhanced Charts ----
    col1, col2 = st.columns(2)

    with col1:
        # ---- Status Distribution (Absolute Count Bar Chart) ----
        status_counts = (
            df["status"]
            .value_counts()
            .reset_index(name="Teams")
            .rename(columns={"status": "Status"})
        )

        # Prize amount per status (if applicable). Most statuses should map to a single prize value;
        # if multiple values exist, we pick the maximum (still useful and deterministic).
        prize_money_numeric = pd.to_numeric(df["prize_money"], errors="coerce")
        status_prize = (
            prize_money_numeric.groupby(df["status"], dropna=False)
            .max()
            .reset_index()
            .rename(columns={"status": "Status", "prize_money": "Prize"})
        )

        status_counts = status_counts.merge(status_prize, on="Status", how="left")
        status_counts["PrizeLabel"] = status_counts["Prize"].apply(
            lambda v: f"₹{v:,.0f}" if pd.notna(v) else "None"
        )

        # Define the exact order based on your actual status values
        STATUS_ORDER = [
            "Winner",
            "Joint Winner",
            "First Prize",
            "Second Prize",
            "Third Prize",
            "Consolation Prize",
            "Future Innovators Award",
            "Girls Achiever Award",  # Note: "Achiever" not "Achievers"
            "Quantum Frontier Award",
            "Shortlisted",
            "Waitlist",
        ]

        # Normalize labels to handle inconsistencies
        status_counts["Status"] = (
            status_counts["Status"].fillna("Unknown").astype(str).str.strip()
        )

        # Keep your preferred order, but include any extra statuses present in data
        observed = (
            status_counts.sort_values("Teams", ascending=False)["Status"].tolist()
        )
        observed_unique: list[str] = []
        for s in observed:
            if s not in observed_unique:
                observed_unique.append(s)

        categories = [s for s in STATUS_ORDER if s in observed_unique] + [
            s for s in observed_unique if s not in STATUS_ORDER
        ]
        status_counts["Status"] = pd.Categorical(
            status_counts["Status"],
            categories=categories,
            ordered=True,
        )
        status_counts = status_counts.sort_values("Teams", ascending=False)

        # Color mapping for each status
        STATUS_COLORS = {
            "Winner": "#FACC15",              # Gold
            "Joint Winner": "#FB7185",        # Pink-red
            "First Prize": "#22C55E",         # Green
            "Second Prize": "#38BDF8",        # Sky blue
            "Third Prize": "#A78BFA",         # Purple
            "Consolation Prize": "#F59E0B",   # Amber
            "Future Innovators Award": "#0EA5E9",  # Cyan
            "Girls Achiever Award": "#EC4899",     # Pink
            "Quantum Frontier Award": "#14B8A6",   # Teal
            "Shortlisted": "#4F6BED",         # Blue
            "Waitlist": "#F472B6",            # Light pink
        }

        fig = go.Figure(
            go.Bar(
                y=status_counts["Status"],
                x=status_counts["Teams"],
                orientation="h",
                marker=dict(
                    color=[STATUS_COLORS.get(s, "#94A3B8") for s in status_counts["Status"]],
                    line=dict(color="rgba(255,255,255,0.15)", width=1),
                ),
                text=status_counts["Teams"],
                textposition="outside",
                textfont=dict(size=11, color='#E6F1FF'),
                cliponaxis=False,
                customdata=status_counts["PrizeLabel"],
                hovertemplate=(
                    "<b>%{y}</b><br><br>"
                    "Teams:&nbsp;&nbsp;%{x:,}"
                    "<br>Prize:&nbsp;&nbsp;%{customdata}"
                    "<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            title=dict(
                text="📊 Distribution of Teams by Final Status",
                font=dict(size=16, weight='bold'),
                x=0,
            ),
            **CHART_LAYOUT,
            xaxis=dict(
                title="Teams Count",
                showgrid=True,
                gridcolor="rgba(128,128,128,0.1)",
                tickmode="linear",
                tick0=0,
                dtick=200,
                rangemode="tozero",
            ),
            yaxis=dict(
                title=None,
                categoryorder="total ascending",
                tickfont=dict(size=11),
            ),
            height=450,
            showlegend=False,
        )

        st.plotly_chart(fig, width="stretch")

    with col2:
        # ---- Prize Money Distribution (Discrete Horizontal Bar Chart) ----
        prize_df = df[df["is_winner"] & df["prize_money"].notna()]

        if not prize_df.empty:
            prize_counts = (
                prize_df["prize_money"]
                .astype(int)
                .value_counts()
                .sort_index(ascending=False)  # Highest prize first
                .reset_index(name="Teams")
                .rename(columns={"prize_money": "Prize Amount"})
            )

            # Create gradient colors based on prize amount (higher = more golden)
            max_prize = prize_counts["Prize Amount"].max()
            colors_gradient = []
            for prize in prize_counts["Prize Amount"]:
                ratio = prize / max_prize
                # Gradient from teal (low) to gold (high)
                if ratio > 0.7:
                    colors_gradient.append("#FACC15")  # Gold
                elif ratio > 0.4:
                    colors_gradient.append("#F59E0B")  # Amber
                else:
                    colors_gradient.append("#38BDF8")  # Blue

            fig2 = go.Figure(
                go.Bar(
                    y=[f"₹{v:,.0f}" for v in prize_counts["Prize Amount"]],
                    x=prize_counts["Teams"],
                    orientation="h",
                    marker=dict(
                        color=colors_gradient,
                        line=dict(color="rgba(255,255,255,0.2)", width=1),
                    ),
                    text=prize_counts["Teams"],
                    textposition="outside",
                    textfont=dict(size=11, color='#E6F1FF'),
                    cliponaxis=False,
                    hovertemplate=(
                        "<b>Prize:</b> ₹%{customdata:,.0f}<br>"
                        "<b>Teams:</b> %{x}<extra></extra>"
                    ),
                    customdata=prize_counts["Prize Amount"]
                )
            )

            fig2.update_layout(
                title=dict(
                    text="💰 Prize Amount Distribution Across Awarded Teams",
                    font=dict(size=16, weight="bold"),
                    x=0,
                ),
                **CHART_LAYOUT,
                xaxis=dict(
                    title="Number of Awarded Teams",
                    showgrid=True,
                    gridcolor="rgba(128,128,128,0.1)",
                    tickmode="linear",
                    tick0=0,
                    dtick=30,
                    rangemode="tozero",
                ),
                yaxis=dict(
                    title="Prize Amount (INR)",
                    categoryorder="total ascending",
                    tickfont=dict(size=11),
                ),
                height=450,
                showlegend=False,
            )

            st.plotly_chart(fig2, width="stretch")

        else:
            st.info("No prize money data available for winning teams.")

    st.divider()

    # ---- Enhanced Detailed Teams Table ----
    st.subheader("🔍 Team-Level Details & Outcomes")


    # Search box with better styling
    search = st.text_input(
        "🔎 Search by Team Name or Team Leader",
        placeholder="Type to search...",
        help="Search is case-insensitive and applies to visible records"
    )

    teams_df = df[
        [
            "team_id",
            "team_name",
            "team_leader_name",
            "status",
            "ps_id",
            "problem_statement_title",
            "category",
            "theme",
            "prize_money",
            "institute_name",
            "institute_state",
        ]
    ].copy()

    # Apply search filter
    if search:
        teams_df = teams_df[
            teams_df["team_name"].str.contains(search, case=False, na=False)
            | teams_df["team_leader_name"].str.contains(search, case=False, na=False)
        ]

    # Sort by prize money
    teams_df = teams_df.sort_values(
        by=["prize_money"],
        ascending=False,
        na_position="last",
    )

    # Truncate long text columns for better display
    display_df = teams_df.copy()
    display_df["team_name"] = display_df["team_name"].apply(lambda x: truncate_text(x, 30))
    display_df["team_leader_name"] = display_df["team_leader_name"].apply(lambda x: truncate_text(x, 25))
    display_df["problem_statement_title"] = display_df["problem_statement_title"].apply(lambda x: truncate_text(x, 50))
    display_df["institute_name"] = display_df["institute_name"].apply(lambda x: truncate_text(x, 40))

    # Enhanced dataframe display with better column configuration
    st.dataframe(
        display_df,
        width="stretch",
        height=500,
        column_config={
            "team_id": st.column_config.NumberColumn(
                "Team ID",
                format="%d",
                width="small"
            ),
            "team_name": st.column_config.TextColumn(
                "Team Name",
                width="medium",
                help="Truncated for display. Full name in original data."
            ),
            "team_leader_name": st.column_config.TextColumn(
                "Team Leader Name",
                width="medium",
                help="Truncated for display. Full name in original data."
            ),
            "final_status": st.column_config.TextColumn(
                "Final Status",
                width="small"
            ),
            "ps_id": st.column_config.TextColumn(
                "PS ID",
                width="small"
            ),
            "problem_statement_title": st.column_config.TextColumn(
                "Problem Statement Title",
                width="large",
                help="Truncated for display. Full title in original data."
            ),
            "category": st.column_config.TextColumn(
                "Category",
                width="medium"
            ),
            "theme": st.column_config.TextColumn(
                "Theme",
                width="medium"
            ),
            "prize_money": st.column_config.NumberColumn(
                "Prize Amount (INR)",
                format="₹%,.0f",
                width="medium"
            ),
            "institute_name": st.column_config.TextColumn(
                "Institute Name",
                width="large",
                help="Truncated for display. Full name in original data."
            ),
            "institute_state": st.column_config.TextColumn(
                "Institute State",
                width="small"
            ),
        },
        hide_index=True,
    )

    # Download button for full data
    col_info, col_download = st.columns([3, 1])
    
    with col_info:
        st.info(
            f"📊 Displaying **{len(teams_df):,}** teams based on current filters "
            f"out of **{total_teams:,}** total participating teams"
        )    
    with col_download:
        csv = teams_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Team-Level Dataset (CSV)",
            data=csv,
            file_name="teams_data.csv",
            mime="text/csv",
            width="stretch"
        )