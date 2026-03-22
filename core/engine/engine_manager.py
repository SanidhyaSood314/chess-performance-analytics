import chess.engine
import streamlit as st


# -------------------------------------------------
# Engine Manager
# -------------------------------------------------

@st.cache_resource
def get_engine():
    """
    Start Stockfish engine with multiple fallback paths.
    Ensures compatibility across environments.
    """

    possible_paths = [
        "stockfish",              # default (expected)
        "/usr/games/stockfish",   # common Linux path
        "/usr/bin/stockfish",     # alternative Linux path
    ]

    for path in possible_paths:
        try:
            return chess.engine.SimpleEngine.popen_uci(path)
        except Exception:
            continue

    # If all fail → show error
    st.error("❌ Stockfish engine not found on server.")
    st.error("Tried paths: " + ", ".join(possible_paths))

    raise RuntimeError("Stockfish initialization failed")
