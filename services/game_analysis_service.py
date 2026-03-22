# services/game_analysis_service.py

import streamlit as st

from core.engine.game_analyzer import GameAnalyzer


@st.cache_resource
def get_analyzer():
    """
    Create a single GameAnalyzer instance.
    """
    return GameAnalyzer(depth=12)


def analyze_game_once(pgn_string: str):
    """
    Run engine analysis exactly once per game
    and store result inside session_state.
    """

    cache = st.session_state.setdefault("game_analysis_cache", {})

    if pgn_string not in cache:

        analyzer = get_analyzer()

        cache[pgn_string] = analyzer.analyze_game(pgn_string)

    return cache[pgn_string]