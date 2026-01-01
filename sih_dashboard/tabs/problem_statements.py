from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Modern color schemes
COLOR_SCHEMES = {
    'gradient_purple': ['#667eea', '#764ba2', '#f093fb'],
    'gradient_orange': ['#ff9a56', '#ff6a88', '#feca57'],
    'gradient_teal': ['#11998e', '#38ef7d'],
    'gradient_pink': ['#f857a6', '#ff5858'],
    'vibrant': ['#f857a6', '#ff5858', '#fdbb2d', '#22c1c3', '#667eea', '#f093fb'],
}

import plotly.graph_objects as go

# =========================
# Chart layout template
# =========================
CHART_LAYOUT = {
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'font': {
        'family': 'Inter, system-ui, sans-serif',
        'size': 12,
        'color': '#E6F1FF'
    },
    # ⬇ FIX: Increased right margin
    'margin': {'l': 60, 'r': 80, 't': 60, 'b': 40},
    'hoverlabel': {
        'bgcolor': '#0F172A',
        'bordercolor': '#4DA3FF',
        'font': {
            'family': 'Inter, system-ui, sans-serif',
            'size': 13,
            'color': '#E6F1FF'
        }
    },
}


def create_gradient_bar_chart(
    data,
    x,
    y,
    title,
    orientation='h',
    color_scheme='gradient_purple',
    hover_data=None
):
    """Create a bar chart with safe right margin and unclipped labels."""

    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES['gradient_purple'])
    n_bars = len(data)

    bar_colors = (
        colors[:n_bars]
        if n_bars <= len(colors)
        else [colors[i % len(colors)] for i in range(n_bars)]
    )

    fig = go.Figure()

    if orientation == 'h':
        display_labels = [truncate_text(label, 40) for label in data[y]]

        # ---- Hover template ----
        if hover_data:
            hover_text = "<b>%{customdata[0]}</b><br><br>Teams:&nbsp;&nbsp;%{x:,}"
            customdata_list = [[row[y]] + [row[hd] for hd in hover_data] for _, row in data.iterrows()]
            for hd in hover_data:
                hover_text += f"<br>{hd}: %{{customdata[{hover_data.index(hd) + 1}]}}"
            hover_text += "<extra></extra>"
        else:
            hover_text = "<b>%{customdata}</b><br><br>Teams:&nbsp;&nbsp;%{x:,}<extra></extra>"
            customdata_list = data[y]

        fig.add_trace(
            go.Bar(
                y=display_labels,
                x=data[x],
                orientation='h',
                marker=dict(
                    color=bar_colors,
                    line=dict(color='rgba(255,255,255,0.2)', width=1),
                ),
                text=data[x],
                textposition='outside',
                textfont=dict(size=11, color='#E6F1FF'),
                cliponaxis=False,   # ⬅ CRITICAL FIX
                hovertemplate=hover_text,
                customdata=customdata_list,
            )
        )

        max_val = data[x].max()

        fig.update_layout(
            **CHART_LAYOUT,
            title=dict(text=title, font=dict(size=16, weight='bold'), x=0),
            showlegend=False,
            height=500,
        )

        # ⬇ FIX: Axis padding so labels never hit edge
        fig.update_xaxes(
            range=[0, max_val * 1.15],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.1)',
            title=None
        )

        fig.update_yaxes(
            showgrid=False,
            title=None,
            categoryorder='total ascending'
        )

    return fig



def truncate_text(text: str, max_length: int = 40) -> str:
    """Truncate long text and add ellipsis."""
    text_str = str(text)
    if len(text_str) > max_length:
        return text_str[:max_length] + "..."
    return text_str


def render(df: pd.DataFrame) -> None:
    st.header("🧩 Problem Statements — Participation & Outcome Analysis")

    if df.empty:
        st.warning("No problem statement records match the current filter criteria.")
        return

    # ---- Enhanced High-level metrics with Gradient Cards ----
    col1, col2, col3, col4 = st.columns(4)

    avg_teams = df.groupby("ps_id")["team_id"].count().mean()

    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(5, 150, 105, 0.25);">
                <div style="font-size: 2rem;">🧩</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df["ps_id"].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Unique Problem Statements</div>
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
                <div style="font-size: 2rem;">🏢</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df["organization"].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Participating Organizations</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #78350F 0%, #D97706 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(217, 119, 6, 0.25);">
                <div style="font-size: 2rem;">🏛️</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df["department"].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Participating Departments</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(37, 99, 235, 0.25);">
                <div style="font-size: 2rem;">📊</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{avg_teams:.1f}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Average Teams per Problem Statement</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    # ---- Enhanced Charts ----
    col1, col2 = st.columns(2)

    with col1:
        ps_counts = (
            df.groupby(["ps_id", "problem_statement_title"])["team_id"]
            .count()
            .sort_values(ascending=False)
            .head(20)
            .reset_index(name="Teams")
        )

        fig1 = create_gradient_bar_chart(
            ps_counts,
            x="Teams",
            y="ps_id",
            title="🏆 Top 20 Problem Statements by Submission Volume",
            orientation='h',
            color_scheme='gradient_purple',
            hover_data=["problem_statement_title"]
        )
        st.plotly_chart(fig1, width="stretch")

    with col2:
        org_counts = (
            df["organization"]
            .value_counts()
            .head(15)
            .reset_index(name="Teams")
            .rename(columns={"organization": "Organization"})
        )

        fig2 = create_gradient_bar_chart(
            org_counts,
            x="Teams",
            y="Organization",
            title="🏢 Top 15 Organizations by Submission Volume",
            orientation='h',
            color_scheme='gradient_orange'
        )
        st.plotly_chart(fig2, width="stretch")

    # ---- Departments Chart ----
    dept_counts = (
        df["department"]
        .value_counts()
        .head(15)
        .reset_index(name="Teams")
        .rename(columns={"department": "Department"})
    )

    fig3 = create_gradient_bar_chart(
        dept_counts,
        x="Teams",
        y="Department",
        title="🏛️ Top 15 Departments by Submission Volume",
        orientation='h',
        color_scheme='gradient_teal'
    )
    fig3.update_layout(height=450)
    st.plotly_chart(fig3, width="stretch")

    st.divider()

    # ---- Enhanced PS Summary Table ----
    st.subheader("📋 Problem Statement-Level Summary Metrics")

    # Add search and sort controls
    col_search, col_sort = st.columns([3, 1])
    
    with col_search:
        search_ps = st.text_input(
            "🔎 Search Problem Statement",
            placeholder="Filter by Problem Statement ID or title",
            help="Filter by problem statement ID or title"
        )
    
    with col_sort:
        sort_by = st.selectbox(
            "Sort by",
            options=["teams", "institutes", "states", "winners", "submission_ratio"],
            format_func=lambda x: {
                "teams": "Total Teams",
                "institutes": "Participating Institutes",
                "states": "Participating States",
                "winners": "Winning Teams",
                "submission_ratio": "Submission Utilization Ratio"
            }[x]
        )

    ps_summary = (
        df.groupby(
            [
                "ps_id",
                "problem_statement_title",
                "category",
                "theme",
                "organization",
                "department",
            ],
            as_index=False,
        )
        .agg(
            teams=("team_id", "count"),
            institutes=("institute_name", "nunique"),
            states=("institute_state", "nunique"),
            winners=("status", lambda x: x.isin(["Winner", "Joint Winner","First Prize",
                        "Second Prize",
                        "Third Prize",
                        "Consolation Prize",
                        "Future Innovators Award",
                        "Girls Achiever Award",  
                        "Quantum Frontier Award",]).sum()),
            total_submission=("total_submission", "max"),
            max_submission=("max_submission", "max"),
        )
    )

    ps_summary["submission_ratio"] = (
        ps_summary["total_submission"] / ps_summary["max_submission"].replace(0, pd.NA)
    )

    # Apply search filter
    if search_ps:
        ps_summary = ps_summary[
            ps_summary["ps_id"].str.contains(search_ps, case=False, na=False) |
            ps_summary["problem_statement_title"].str.contains(search_ps, case=False, na=False)
        ]

    # Sort by selected column
    ps_summary = ps_summary.sort_values(sort_by, ascending=False)

    # Truncate long text for display
    display_summary = ps_summary.copy()
    display_summary["problem_statement_title"] = display_summary["problem_statement_title"].apply(lambda x: truncate_text(x, 60))
    display_summary["organization"] = display_summary["organization"].apply(lambda x: truncate_text(x, 35))
    display_summary["department"] = display_summary["department"].apply(lambda x: truncate_text(x, 35))

    st.dataframe(
        display_summary,
        width="stretch",
        height=400,
        column_config={
            "ps_id": st.column_config.TextColumn(
                "PS ID",
                width="small"
            ),
            "problem_statement_title": st.column_config.TextColumn(
                "Problem Statement Title",
                width="large",
                help="Truncated for display. Hover to see more."
            ),
            "category": st.column_config.TextColumn(
                "Category",
                width="medium"
            ),
            "theme": st.column_config.TextColumn(
                "Theme",
                width="medium"
            ),
            "organization": st.column_config.TextColumn(
                "Organization",
                width="medium",
                help="Truncated for display. Full name in original data."
            ),
            "department": st.column_config.TextColumn(
                "Department",
                width="medium",
                help="Truncated for display. Full name in original data."
            ),
            "teams": st.column_config.NumberColumn(
                "Teams",
                format="%d",
                width="small"
            ),
            "institutes": st.column_config.NumberColumn(
                "Institutes",
                format="%d",
                width="small"
            ),
            "states": st.column_config.NumberColumn(
                "States",
                format="%d",
                width="small"
            ),
            "winners": st.column_config.NumberColumn(
                "Winners",
                format="%d",
                width="small"
            ),
            "total_submission": st.column_config.NumberColumn(
                "Total Sub",
                format="%d",
                width="small"
            ),
            "max_submission": st.column_config.NumberColumn(
                "Max Sub",
                format="%d",
                width="small"
            ),
            "submission_ratio": st.column_config.NumberColumn(
                "Submission Utilization Ratio",
                format="%.2f",
                width="small",
                help="Actual submissions divided by maximum allowed submissions"
            ),
        },
        hide_index=True,
    )

    # Info and download
    col_info, col_download = st.columns([3, 1])
    
    with col_info:
        st.info(f"📊 Displaying **{len(ps_summary):,}** problem statements based on current filters")
    
    with col_download:
        csv = ps_summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name="problem_statements_summary.csv",
            mime="text/csv",
            width="stretch"
        )

    # ---- Enhanced Detailed PS View ----
    st.divider()
    st.subheader("🔍 Problem Statement — Detailed Breakdown")

    selected_ps = st.selectbox(
        "Select a Problem Statement for Detailed Analysis",
        sorted(df["ps_id"].unique()),
    )
    ps_df = df[df["ps_id"] == selected_ps]

    # Enhanced detail display with better formatting
    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%); 
                    padding: 20px; border-radius: 10px; border-left: 5px solid #667eea; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #667eea;">📄 {selected_ps}</h4>
            <p style="margin: 5px 0;"><strong>Problem Statement Title:</strong> {ps_df['problem_statement_title'].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Category:</strong> {ps_df['category'].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Theme:</strong> {ps_df['theme'].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Owning Organization:</strong> {ps_df['organization'].iloc[0]}</p>
            <p style="margin: 5px 0;"><strong>Responsible Department:</strong> {ps_df['department'].iloc[0]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    winning_teams = ps_df["status"].isin(["Winner", "Joint Winner"]).sum()
    
    with col1:
        st.metric("👥 Total Teams", len(ps_df))
    with col2:
        st.metric("🏫 Participating Institutes", ps_df["institute_name"].nunique())
    with col3:
        st.metric("🗺️ Participating States", ps_df["institute_state"].nunique())
    with col4:
        st.metric("🏆 Declared Winners", winning_teams)

    st.write("")

    # State distribution chart
    state_dist = (
        ps_df["institute_state"]
        .value_counts()
        .reset_index(name="Teams")
        .rename(columns={"institute_state": "State"})
    )

    fig = create_gradient_bar_chart(
        state_dist,
        x="Teams",
        y="State",
        title=f"🗺️ Geographic Distribution of Teams — {selected_ps}",
        orientation='h',
        color_scheme='gradient_pink'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width="stretch")