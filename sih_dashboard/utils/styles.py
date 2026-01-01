"""Styling helpers.

No Streamlit calls at import time. Call `inject_global_css()` from `app.py`.
"""

import streamlit as st


def inject_global_css() -> None:
    st.markdown(
        """
        <style>

        /* Inline code styling (avoid overriding code blocks). */
        .stMarkdown :not(pre) > code {
            background-color: rgba(255, 255, 255, 0.01);
            padding: 1px 5px;
            border-radius: 3px;
            font-weight: 600;
            color: #FF6FAE; /* A nice pinkish-red for IDs */
        }

        /* Reduce padding */
        .block-container {
            padding-top: 2rem;
            /* Add bottom padding so pages have breathing room at the bottom */
            padding-bottom: 3rem;
        }

        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}

        /* Improve metric styling */
        [data-testid="stMetricValue"] {
            font-size: 28px;
        }

        /* Better tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 10px 20px;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )
