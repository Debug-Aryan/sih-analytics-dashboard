from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Modern color schemes
COLOR_SCHEMES = {
    'gradient_blue': ['#667eea', '#764ba2'],
    'gradient_teal': ['#11998e', '#38ef7d'],
    'vibrant': ['#fdbb2d', '#22c1c3'],
}

def truncate_text(text: str, max_length: int = 40) -> str:
    """Truncate long text and add ellipsis."""
    text_str = str(text)
    if len(text_str) > max_length:
        return text_str[:max_length] + "..."
    return text_str

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
    'margin': {'l': 60, 'r': 40, 't': 60, 'b': 40},
    # ⬇ FIX: Dark theme hover
    'hoverlabel': {
        'bgcolor': 'rgba(15, 23, 42, 0.95)',
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
    color_scheme='gradient_blue'
):
    """Create a bar chart with safe margins and unclipped labels."""

    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES['gradient_blue'])
    n_bars = len(data)

    bar_colors = (
        colors[:n_bars]
        if n_bars <= len(colors)
        else [colors[i % len(colors)] for i in range(n_bars)]
    )

    fig = go.Figure()

    if orientation == 'h':
        # Truncate long labels for y-axis
        display_labels = [truncate_text(label, 45) for label in data[y]]

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
                hovertemplate=(
                    "<b>%{customdata}</b><br><br>"
                    "Teams:&nbsp;&nbsp;%{x:,}"
                    "<extra></extra>"
                ),
                customdata=data[y],  # Full text for hover
            )
        )

        max_val = data[x].max()

        fig.update_layout(
            **CHART_LAYOUT,
            title=dict(text=title, font=dict(size=16, weight='bold'), x=0),
            showlegend=False,
            height=500,
        )

        # ⬇ FIX: Axis padding so numbers never hit edge
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


def render(df: pd.DataFrame) -> None:
    st.header("🏫 Institutional Participation & Geographic Distribution")

    if df.empty:
        st.warning("No institute-level records match the current filter criteria.")
        return

    # ---- Enhanced Metrics with Gradient Cards ----
    col1, col2, col3, col4 = st.columns(4)

    avg_teams = df.groupby("institute_name")["team_id"].count().mean()

    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(5, 150, 105, 0.25);">
                <div style="font-size: 2rem;">🏫</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df["institute_name"].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Participating Institutes</div>
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
                <div style="font-size: 2rem;">🏙️</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df["institute_city"].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Participating Cities</div>
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
                <div style="font-size: 2rem;">🗺️</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df["institute_state"].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Participating States</div>
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
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Average Teams per Institute</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    # ---- Enhanced Charts ----
    col1, col2 = st.columns(2)

    with col1:
        inst_counts = (
            df.groupby("institute_name")["team_id"]
            .count()
            .sort_values(ascending=False)
            .head(15)
            .reset_index(name="Teams")
        )

        fig1 = create_gradient_bar_chart(
            inst_counts,
            x="Teams",
            y="institute_name",
            title="🏆 Top 15 Institutes by Submissions Volume",
            orientation='h',
            color_scheme='gradient_blue'
        )
        st.plotly_chart(fig1, width="stretch")

    with col2:
        state_counts = (
            df.groupby("institute_state")["team_id"]
            .count()
            .sort_values(ascending=False)
            .head(15)
            .reset_index(name="Teams")
        )

        fig2 = create_gradient_bar_chart(
            state_counts,
            x="Teams",
            y="institute_state",
            title="🗺️ Top 15 States by Submissions Volume",
            orientation='h',
            color_scheme='gradient_teal'
        )
        st.plotly_chart(fig2, width="stretch")

    st.divider()

    # ---- Enhanced Normalized Category Distribution ----
    st.subheader("📊 Normalized Category Distribution Across Top States")

    
    top_states = state_counts["institute_state"].head(10)

    state_cat = (
        df[df["institute_state"].isin(top_states)]
        .groupby(["institute_state", "category"])
        .size()
        .reset_index(name="count")
    )

    state_totals = state_cat.groupby("institute_state")["count"].transform("sum")
    state_cat["share"] = state_cat["count"] / state_totals

    fig3 = go.Figure()

    categories = state_cat["category"].unique()
    colors_list = COLOR_SCHEMES['vibrant'] * (len(categories) // len(COLOR_SCHEMES['vibrant']) + 1)

    for i, category in enumerate(categories):
        cat_data = state_cat[state_cat["category"] == category]
        fig3.add_trace(go.Bar(
            x=cat_data["institute_state"],
            y=cat_data["share"],
            name=category,
            marker=dict(color=colors_list[i]),
            hovertemplate='<b>%{x}</b><br>Category: ' + category + '<br>Share: %{y:.1%}<extra></extra>'
        ))

    fig3.update_layout(
        **CHART_LAYOUT,
        title=dict(text="🎨 Category Share by Top 10 States (Percentage Distribution)", font=dict(size=16, weight='bold'), x=0),
        barmode='stack',
        yaxis=dict(
            tickformat='.0%',
            title='Category Share (%)',
            showgrid=True,
            gridcolor='rgba(128,128,128,0.1)'
        ),
        xaxis=dict(
            title=None,
            showgrid=False
        ),
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
            font=dict(size=10)
        ),
        height=450,
    )

    st.plotly_chart(fig3, width="stretch")

    st.divider()

    # ---- Enhanced Institute Summary Table ----
    st.subheader("📋 Institute-Level Participation & Performance Summary")

    # Add search/filter option
    col_search, col_sort = st.columns([3, 1])
    
    with col_search:
        search_inst = st.text_input(
            "🔎 Search Institutes",
            placeholder="Type to filter institutes...",
            help="Search by institute name"
        )
    
    with col_sort:
        sort_by = st.selectbox(
            "Sort by",
            options=["teams", "unique_ps", "winners", "win_rate"],
            format_func=lambda x: {
                "teams": "Total Teams",
                "unique_ps": "Unique Problem Statements",
                "winners": "Winners",
                "win_rate": "Win Rate (%)"
            }[x]
        )

    inst_summary = (
        df.groupby(
            ["institute_name", "institute_city", "institute_state"],
            as_index=False,
        )
        .agg(
            teams=("team_id", "count"),
            unique_ps=("ps_id", "nunique"),
            winners=("status", lambda x: x.isin(["Winner", "Joint Winner"]).sum()),
        )
    )

    inst_summary["win_rate"] = inst_summary["winners"] / inst_summary["teams"]
    
    # Apply search filter
    if search_inst:
        inst_summary = inst_summary[
            inst_summary["institute_name"].str.contains(search_inst, case=False, na=False)
        ]
    
    # Sort by selected column
    inst_summary = inst_summary.sort_values(sort_by, ascending=False)

    # Truncate long institute names for display
    display_summary = inst_summary.copy()
    display_summary["institute_name"] = display_summary["institute_name"].apply(lambda x: truncate_text(x, 50))
    display_summary["institute_city"] = display_summary["institute_city"].apply(lambda x: truncate_text(x, 25))

    st.dataframe(
        display_summary,
        width="stretch",
        height=400,
        column_config={
            "institute_name": st.column_config.TextColumn(
                "Institute Name",
                width="large",
                help="Truncated for display. Hover to see more."
            ),
            "institute_city": st.column_config.TextColumn(
                "City",
                width="medium"
            ),
            "institute_state": st.column_config.TextColumn(
                "State",
                width="small"
            ),
            "teams": st.column_config.NumberColumn(
                "Total Teams",
                format="%d",
                width="small"
            ),
            "unique_ps": st.column_config.NumberColumn(
                "Unique Problem Statements",
                format="%d",
                width="small"
            ),
            "winners": st.column_config.NumberColumn(
                "Winning Teams",
                format="%d",
                width="small"
            ),
            "win_rate": st.column_config.NumberColumn(
                "Win Rate (%)",
                format="%.1f%%",
                width="small",
                help="Percentage of teams from the institute that achieved a winning outcome"
            ),
        },
        hide_index=True,
    )

    # Summary info and download
    col_info, col_download = st.columns([3, 1])
    
    with col_info:
        st.info(f"📊 Displaying **{len(inst_summary):,}** institutes based on current filters")
    
    with col_download:
        csv = inst_summary.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Institute-Level Summary (CSV)",
            data=csv,
            file_name="institute_summary.csv",
            mime="text/csv",
            width="stretch"
        )