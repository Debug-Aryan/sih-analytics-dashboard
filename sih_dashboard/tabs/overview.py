from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Modern color schemes
COLOR_SCHEMES = {
    'gradient_blue': ['#667eea', '#764ba2'],
    'gradient_purple': ['#f093fb', '#4facfe'],
    'gradient_orange': ['#ff9a56', '#ff6a88', '#feca57'],
    'gradient_green': ['#56ab2f', '#a8e063'],
    'vibrant': ['#f857a6', '#ff5858', '#fdbb2d', '#22c1c3', '#667eea', '#f093fb'],
    'ocean': ['#2E3192', '#1BFFFF', '#4facfe'],
    'sunset': ['#ff6e7f', '#bfe9ff', '#ffeaa7'],
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
        'color': '#E6F1FF'  # better for dark theme
    },
    # ⬇ Increased right margin to avoid text cutoff
    'margin': {'l': 60, 'r': 120, 't': 60, 'b': 40},
    'hoverlabel': {
        'bgcolor': '#0F172A',        # dark background
        'bordercolor': '#4DA3FF',    # subtle blue border
        'font': {
            'family': 'Inter, system-ui, sans-serif',
            'size': 13,
            'color': '#E6F1FF'        # readable light text
        }
    },

}


def create_gradient_bar_chart(
    data,
    x,
    y,
    title,
    orientation='v',
    color_scheme='gradient_blue'
):
    """Create a modern bar chart with safe label rendering (no clipping)."""

    colors = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES['gradient_blue'])
    n_bars = len(data)

    bar_colors = (
        colors[:n_bars]
        if n_bars <= len(colors)
        else [colors[i % len(colors)] for i in range(n_bars)]
    )

    fig = go.Figure()

    # =========================
    # Horizontal Bar Chart
    # =========================
    if orientation == 'h':
        display_labels = [truncate_text(label, 35) for label in data[y]]

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
                cliponaxis=False,  # ✅ CRITICAL FIX
                hovertemplate='<b>%{customdata}</b><br>total Teams: %{x:,}<extra></extra>',
                customdata=data[y],
            )
        )

        max_val = data[x].max()

        fig.update_layout(
            **CHART_LAYOUT,
            title=dict(text=title, font=dict(size=16, weight='bold'), x=0),
            showlegend=False,
            height=350,
        )

        # ⬇ Add axis padding so labels never touch edge
        fig.update_xaxes(
            range=[0, max_val * 1.12],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.1)',
            title=None
        )

        fig.update_yaxes(
            showgrid=False,
            title=None,
            categoryorder='total ascending'
        )

    # =========================
    # Vertical Bar Chart
    # =========================
    else:
        display_labels = [truncate_text(label, 20) for label in data[x]]

        fig.add_trace(
            go.Bar(
                x=display_labels,
                y=data[y],
                marker=dict(
                    color=bar_colors,
                    line=dict(color='rgba(255,255,255,0.2)', width=1),
                ),
                text=data[y],
                textposition='outside',
                textfont=dict(size=11, color='#E6F1FF'),
                cliponaxis=False,  # ✅ CRITICAL FIX
                hovertemplate='<b>%{customdata}</b><br>Teams: %{y:,}<extra></extra>',
                customdata=data[x],
            )
        )

        max_val = data[y].max()

        fig.update_layout(
            **CHART_LAYOUT,
            title=dict(text=title, font=dict(size=16, weight='bold'), x=0),
            showlegend=False,
            height=350,
        )

        fig.update_yaxes(
            range=[0, max_val * 1.12],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.1)',
            title=None
        )

        fig.update_xaxes(
            showgrid=False,
            title=None
        )

    return fig



def truncate_text(text: str, max_length: int = 30) -> str:
    """Truncate long text and add ellipsis."""
    if len(str(text)) > max_length:
        return str(text)[:max_length] + "..."
    return str(text)



def render(df: pd.DataFrame) -> None:
    st.header("📊 SIH 2025 — Submission & Results Overview")

    if df.empty:
        st.warning("No records match the current filter selection.")
        return

    # --- Notice (static disclaimer, not logic) ---
    with st.expander("ℹ️ Official Notice — Data Clarification", expanded=True):
        st.markdown(
            """
            <div style="padding: 12px 18px;
                        border-left: 5px solid #007bff;
                        background: linear-gradient(135deg, rgba(0,123,255,0.08) 0%, rgba(0,123,255,0.02) 100%);
                        border-radius: 8px;
                        line-height: 1.6;
                        margin-bottom: 12px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                <span style="font-size: 0.95rem; color: #E6F1FF;">
                    <strong style="color: #007bff;">📢 Announcement:</strong>
                        Based on the official SIH results, no teams were declared winners for the following
                        Problem Statement IDs:
                        <code>SIH25056</code>, <code>SIH25199</code>, <code>SIH25214</code>
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.write("")

    # --- Enhanced Key Metrics with Icons and Colors ---
    col1, col2, col3, col4, col5 = st.columns(5)

    winning_teams = df[df["status"].isin(["Winner", "Joint Winner"])].shape[0]

    with col1:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #064E3B 0%, #059669 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(5, 150, 105, 0.25);">
                <div style="font-size: 2rem;">👥</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{len(df):,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Total Team Submissions</div>
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
                <div style="font-size: 2rem;">🧩</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df['ps_id'].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Unique Problem Statements</div>
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
                <div style="font-size: 2rem;">🏫</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df['institute_name'].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Participating Institutes</div>
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
                <div style="font-size: 2rem;">📍</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{df['institute_state'].nunique():,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Participating States</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, #422006 0%, #B45309 100%);
       padding: 20px; border-radius: 10px; text-align: center;
       box-shadow: 0 10px 30px rgba(180, 83, 9, 0.25);">
                <div style="font-size: 2rem;">🏆</div>
                <div style="color: white; font-size: 1.8rem; font-weight: bold; margin: 5px 0;">{winning_teams:,}</div>
                <div style="color: rgba(255,255,255,0.9); font-size: 0.85rem;">Declared Winning Teams</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.divider()

    # --- Enhanced Charts ---
    col1, col2 = st.columns(2)

    with col1:
        year_counts = (
            df["edition_year"]
            .value_counts()
            .sort_index()
            .reset_index(name="Teams")
            .rename(columns={"edition_year": "Edition Year"})
        )

        fig1 = create_gradient_bar_chart(
            year_counts,
            x="Edition Year",
            y="Teams",
            title="📅 Team Submissions Across SIH Editions",
            orientation='v',
            color_scheme='gradient_blue'
        )
        st.plotly_chart(fig1, width="stretch")

    with col2:
        cat_counts = (
            df["category"]
            .value_counts()
            .reset_index(name="Teams")
        )
    
        fig2 = px.pie(
            cat_counts,
            names="category",
            values="Teams",
            hole=0.5,
            title="🍩 Distribution of Team Submissions by Category",
            labels={"category": "Category", "Teams": "Teams"},
            color_discrete_sequence=DONUT_COLORS,  # ⬅ FIX
        )

        fig2.update_traces(
            textinfo="percent+label",
            textposition="inside",
            textfont=dict(
                color="#FFFFFF",   # ⬅ force white text
                size=12,
                family="Inter, system-ui, sans-serif",
            ),
            insidetextorientation="auto",  # ⬅ avoids overlap
        )

        fig2.update_layout(
            height=400,
            showlegend=True,
            legend_title_text="Category",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )

    
        st.plotly_chart(fig2, width="stretch")


    col3, col4 = st.columns(2)

    with col3:
        theme_counts = (
            df["theme"]
            .value_counts()
            .head(10)
            .reset_index(name="Teams")
            .rename(columns={"theme": "Theme"})
        )

        fig3 = create_gradient_bar_chart(
            theme_counts,
            x="Teams",
            y="Theme",
            title="🎨 Top 10 Themes by Submission Volume",
            orientation='h',
            color_scheme='gradient_orange'
        )
        st.plotly_chart(fig3, width="stretch")

    with col4:
        state_counts = (
            df["institute_state"]
            .value_counts()
            .head(10)
            .reset_index(name="Teams")
            .rename(columns={"institute_state": "State"})
        )

        fig4 = create_gradient_bar_chart(
            state_counts,
            x="Teams",
            y="State",
            title="🗺️ Top 10 States by Participation Volume",
            orientation='h',
            color_scheme='gradient_green'
        )
        st.plotly_chart(fig4, width="stretch")