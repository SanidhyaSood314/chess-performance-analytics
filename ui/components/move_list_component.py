import streamlit as st
import chess

ICON_MAP = {
    "brilliant": "🔥",
    "best": "✓",
    "great": "⭐",
    "normal": "",
    "inaccurate": "⚠",
    "mistake": "⚠",
    "blunder": "❌",
}


def render_move_list(moves, boards, analysis_data):

    st.markdown("### Moves")

    html = """
    <div style="
        height:520px;
        overflow-y:auto;
        border:1px solid #444;
        border-radius:6px;
        padding:8px;
        font-family: monospace;
    ">
    """

    for i in range(0, len(moves), 2):

        move_number = i // 2 + 1

        html += f"<b>{move_number}.</b> "

        # White move
        if i < len(moves):

            board = boards[i]
            move = moves[i]

            san = board.san(move)

            classification = analysis_data[i].classification
            icon = ICON_MAP.get(classification, "")

            html += f'<a href="?move={i+1}">{san}</a>{icon} '

        # Black move
        if i + 1 < len(moves):

            board = boards[i + 1]
            move = moves[i + 1]

            san = board.san(move)

            classification = analysis_data[i + 1].classification
            icon = ICON_MAP.get(classification, "")

            html += f'<a href="?move={i+2}">{san}</a>{icon} '

        html += "<br>"

    html += "</div>"

    st.markdown(html, unsafe_allow_html=True)

    params = st.query_params

    if "move" in params:

        try:
            st.session_state.move_index = int(params["move"])
        except:
            pass