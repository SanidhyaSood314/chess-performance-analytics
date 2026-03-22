import streamlit as st

from core.data.board_builder import (
    load_game_from_pgn,
    extract_mainline_moves,
    build_all_boards
)

from services.game_analysis_service import analyze_game_once


@st.cache_data
def build_game_labels(df):

    labels = []
    indices = []

    for idx, row in df.iterrows():

        pgn_string = row["PGN"]
        game = load_game_from_pgn(pgn_string)

        headers = game.headers

        white = headers.get("White", "White")
        black = headers.get("Black", "Black")
        result = headers.get("Result", "")
        time_control = headers.get("TimeControl", "")

        label = f"{white} vs {black} | {result} | {time_control}"

        labels.append(label)
        indices.append(idx)

    return labels, indices


def load_game_state(pgn_string):

    if (
        "current_game_pgn" in st.session_state
        and st.session_state.current_game_pgn == pgn_string
    ):
        return

    st.session_state.current_game_pgn = pgn_string

    st.session_state.moves = extract_mainline_moves(pgn_string)

    st.session_state.boards = build_all_boards(pgn_string)

    st.session_state.analysis_data = analyze_game_once(pgn_string)

    st.session_state.move_index = 0