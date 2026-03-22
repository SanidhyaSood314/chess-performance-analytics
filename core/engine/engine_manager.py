import chess.engine
import streamlit as st


# -------------------------------------------------
# Engine Manager
# -------------------------------------------------

@st.cache_resource
def get_engine():
    """
    Start Stockfish engine safely for deployment.

    Uses system-installed Stockfish (via packages.txt).
    Cached to avoid restarting engine multiple times.
    """

    try:
        # Primary: Streamlit Cloud / Linux environment
        engine = chess.engine.SimpleEngine.popen_uci("stockfish")
        return engine

    except Exception as e:
        # Graceful error for debugging
        st.error("❌ Stockfish engine could not be started.")
        st.error("Make sure 'stockfish' is installed via packages.txt.")

        raise RuntimeError("Stockfish initialization failed") from e
