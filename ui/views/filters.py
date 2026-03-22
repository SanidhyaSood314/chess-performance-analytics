import streamlit as st
import pandas as pd


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render sidebar filters and return filtered dataframe.
    """

    st.sidebar.header("Filters")

    min_date = df["DateTime"].min()
    max_date = df["DateTime"].max()

    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date.date(), max_date.date())
    )

    selected_formats = st.sidebar.multiselect(
        "Select Formats",
        options=sorted(df["Format"].unique()),
        default=sorted(df["Format"].unique())
    )

    selected_colors = st.sidebar.multiselect(
        "Select Colors",
        options=["White", "Black"],
        default=["White", "Black"]
    )

    filtered_df = df[
        (df["DateTime"].dt.date >= date_range[0]) &
        (df["DateTime"].dt.date <= date_range[1]) &
        (df["Format"].isin(selected_formats)) &
        (df["PlayerColor"].isin(selected_colors))
    ]

    return filtered_df