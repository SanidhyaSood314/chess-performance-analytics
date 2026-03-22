# core/engine/engine_analysis.py

import chess
import chess.engine
import os
import sys
import asyncio
import streamlit as st


# -------------------------------------------------
# 🔥 Windows Fix for Async Subprocess Issue
# -------------------------------------------------
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


# -------------------------------------------------
# Engine Path Configuration
# -------------------------------------------------
ENGINE_PATH = os.path.join(
    os.getcwd(),
    "engines",
    "stockfish.exe"
)


# -------------------------------------------------
# Raw Engine Evaluation (NO caching here)
# -------------------------------------------------
def evaluate_position(board: chess.Board, depth: int = 12) -> float:
    """
    Evaluate a chess position using Stockfish.

    Returns:
        Centipawn score (positive = White advantage)
    """

    if not os.path.exists(ENGINE_PATH):
        raise FileNotFoundError(
            f"Stockfish not found at path: {ENGINE_PATH}"
        )

    with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:

        info = engine.analyse(
            board,
            chess.engine.Limit(depth=depth)
        )

        score = info["score"].white()

        # Handle mate score
        if score.is_mate():
            mate_value = score.mate()
            return 10000 if mate_value > 0 else -10000

        return score.score()


# -------------------------------------------------
# Cached Wrapper (UI calls THIS function)
# -------------------------------------------------
@st.cache_data(show_spinner=False)
def evaluate_position_cached(fen: str, depth: int = 12) -> float:
    """
    Cached evaluation based on FEN.
    Prevents repeated engine calls when slider moves.
    """

    board = chess.Board(fen)
    return evaluate_position(board, depth)


def analyze_with_multipv(board: chess.Board, depth: int = 14, multipv: int = 3):
    with chess.engine.SimpleEngine.popen_uci(ENGINE_PATH) as engine:

        info = engine.analyse(
            board,
            chess.engine.Limit(depth=depth),
            multipv=multipv
        )

    return info