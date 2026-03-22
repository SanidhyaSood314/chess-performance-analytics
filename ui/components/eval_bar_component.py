# ui/components/eval_bar_component.py

import streamlit as st


def render_eval_bar(score: float, flipped: bool = False):
    """
    Render vertical evaluation bar.

    Positive score → White advantage
    Negative score → Black advantage

    If flipped=True, the bar orientation is reversed
    so it matches the flipped board perspective.
    """

    # Clamp extreme values
    score = max(-1000, min(1000, score))

    # Convert score to percentage
    percentage = 50 + (score / 1000) * 50
    percentage = max(0, min(100, percentage))

    # Format score display
    if score > 0:
        display_score = f"+{score/100:.2f}"
    else:
        display_score = f"{score/100:.2f}"

    # Flip gradient direction if board is flipped
    if flipped:
        gradient = f"""
        linear-gradient(
            to bottom,
            white {percentage}%,
            black {percentage}%
        )
        """
    else:
        gradient = f"""
        linear-gradient(
            to top,
            white {percentage}%,
            black {percentage}%
        )
        """

    st.markdown(
        f"""
        <div style="
            height:520px;
            width:45px;
            background:{gradient};
            border-radius:6px;
            border:1px solid #888;
            position:relative;
            display:flex;
            align-items:center;
            justify-content:center;
            font-weight:bold;
            color:red;
        ">
            <span style="
                position:absolute;
                top:10px;
                background:rgba(255,255,255,0.7);
                padding:2px 4px;
                border-radius:4px;
                font-size:14px;
            ">
                {display_score}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )