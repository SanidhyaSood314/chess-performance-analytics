import streamlit as st


def render_engine_line(move_data):

    if move_data is None:
        return

    best_move = move_data.best_move

    if best_move is None:
        return

    st.markdown("### Engine Suggestion")

    st.write(f"Best Move: **{best_move}**")