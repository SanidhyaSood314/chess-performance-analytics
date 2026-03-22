# ui/components/board_component.py

import streamlit as st


def render_chessboard(svg_board: str):
    """
    Render precomputed SVG board.
    """

    st.markdown(
        f"""
        <div style="display:flex; justify-content:center;">
            {svg_board}
        </div>
        """,
        unsafe_allow_html=True
    )