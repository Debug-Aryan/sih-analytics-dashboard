"""Data loading & preparation.

Rules:
- No Streamlit calls at import time.
- Caching is applied on the function that reads from disk.
"""

from __future__ import annotations

import warnings
import numpy as np
import pandas as pd
import streamlit as st


warnings.filterwarnings("ignore")


@st.cache_data
def load_data(filepath: str) -> pd.DataFrame:
    """Load and prepare the SIH dataset."""
    df = pd.read_csv(filepath)

    # Strip whitespace from string-like columns (preserve NaN; avoid forcing numeric dtypes to string)
    obj_cols = df.select_dtypes(include=["object"]).columns
    for col in obj_cols:
        df[col] = df[col].where(df[col].isna(), df[col].astype(str).str.strip())

    # Normalize common string placeholders to missing (only for object columns)
    if len(obj_cols) > 0:
        df[obj_cols] = df[obj_cols].replace({"nan": np.nan, "": np.nan})

    # Convert edition_year to int (guard if column is missing)
    if "edition_year" in df.columns:
        df["edition_year"] = pd.to_numeric(df["edition_year"], errors="coerce").fillna(0).astype(int)
    else:
        df["edition_year"] = 0

    # Parse total_submission (e.g., '500/500' -> submissions_received, submissions_limit)
    if "total_submission" in df.columns:
        split = df["total_submission"].astype(str).str.split("/", expand=True)
        if split.shape[1] >= 2:
            df[["submissions_received", "submissions_limit"]] = split.iloc[:, :2]
            df["submissions_received"] = (
                pd.to_numeric(df["submissions_received"], errors="coerce").fillna(0).astype(int)
            )
            df["submissions_limit"] = (
                pd.to_numeric(df["submissions_limit"], errors="coerce").fillna(0).astype(int)
            )

    # Fill missing values for display (object columns only; keep numeric columns numeric)
    obj_cols = df.select_dtypes(include=["object"]).columns
    if len(obj_cols) > 0:
        df[obj_cols] = df[obj_cols].fillna("Unknown")

    return df


def validate_required_columns(df: pd.DataFrame, required: set[str]) -> set[str]:
    """Return missing required columns."""
    return required - set(df.columns)
