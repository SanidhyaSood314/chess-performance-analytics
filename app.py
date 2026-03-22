import sys
import asyncio

# -------------------------------------------------
# Windows asyncio fix for python-chess engine
# Must run BEFORE Streamlit starts the app
# -------------------------------------------------
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st

from config import USERNAME, APP_TITLE, APP_DESCRIPTION, PAGE_CONFIG
from core.data.pgn_parser import parse_pgn
from core.data.feature_engineering import engineer_features
from ui.views.filters import apply_filters
from ui.views.dashboard import render_dashboard
from ui.views.titles import render_app_header
from services.chesscom_api import fetch_all_pgn, ChessComAPIError


def main():

    st.set_page_config(**PAGE_CONFIG)

    if "raw_df" not in st.session_state:
        st.session_state.raw_df = None

    if "active_username" not in st.session_state:
        st.session_state.active_username = USERNAME

    render_app_header(APP_TITLE, APP_DESCRIPTION)

    st.markdown("## Data Source")

    data_source = st.radio(
        "Choose Data Source",
        ["Upload PGN", "Fetch from Chess.com"]
    )

    if data_source == "Upload PGN":

        uploaded_file = st.file_uploader("Upload PGN File", type=["pgn"])

        if uploaded_file is not None:
            st.session_state.raw_df = parse_pgn(uploaded_file)
            st.session_state.active_username = USERNAME

    elif data_source == "Fetch from Chess.com":

        username_input = st.text_input("Enter Chess.com Username")

        if st.button("Fetch Games") and username_input:

            try:
                with st.spinner("Fetching games..."):
                    pgn_string = fetch_all_pgn(username_input)

                if pgn_string:
                    st.session_state.raw_df = parse_pgn(pgn_string)
                    st.session_state.active_username = username_input
                else:
                    st.warning("No games found.")

            except ChessComAPIError as e:
                st.error(str(e))

    if (
        st.session_state.raw_df is not None
        and not st.session_state.raw_df.empty
    ):

        features_df = engineer_features(
            st.session_state.raw_df,
            st.session_state.active_username
        )

        filtered_df = apply_filters(features_df)

        render_dashboard(filtered_df, features_df)


if __name__ == "__main__":
    main()