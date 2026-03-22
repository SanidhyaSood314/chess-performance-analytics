import streamlit as st


def render_move_classification(classification, move_display):

    classification_ui = {
        "brilliant": ("🔥 Brilliant Move", "#2ecc71"),
        "best": ("💎 Best Move", "#16a085"),
        "great": ("⭐ Great Move", "#27ae60"),
        "normal": ("✓ Normal Move", "#95a5a6"),
        "inaccurate": ("⚠ Inaccuracy", "#f1c40f"),
        "mistake": ("⚠ Mistake", "#e67e22"),
        "blunder": ("❌ Blunder", "#e74c3c"),
    }

    if classification not in classification_ui:
        return

    label, color = classification_ui[classification]

    st.markdown(
        f"""
        <div style="
            margin-top:15px;
            padding:10px;
            border-radius:8px;
            background-color:{color};
            color:white;
            font-weight:bold;
            text-align:center;
            font-size:18px;
        ">
            {move_display} — {label}
        </div>
        """,
        unsafe_allow_html=True
    )