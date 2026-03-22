import chess.engine
import streamlit as st

from config.settings import ENGINE_PATH


# -------------------------------------------------
# Engine Manager
# -------------------------------------------------

@st.cache_resource
def get_engine():
    """
    Start Stockfish engine once per Streamlit session.

    st.cache_resource keeps the engine alive and reusable.
    """

    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

    return engine