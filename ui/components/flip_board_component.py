import streamlit as st


def render_flip_button():

    if "board_flipped" not in st.session_state:
        st.session_state.board_flipped = False

    if st.button("🔄 Flip Board"):
        st.session_state.board_flipped = not st.session_state.board_flipped

    return st.session_state.board_flipped