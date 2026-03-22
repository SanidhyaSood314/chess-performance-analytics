# core/data/board_builder.py

import chess
import chess.pgn
import chess.svg
import io
import streamlit as st


def load_game_from_pgn(pgn_string: str):
    return chess.pgn.read_game(io.StringIO(pgn_string))


@st.cache_data
def extract_mainline_moves(pgn_string: str):

    game = chess.pgn.read_game(io.StringIO(pgn_string))

    return list(game.mainline_moves())


@st.cache_data
def build_all_boards(pgn_string: str):

    game = chess.pgn.read_game(io.StringIO(pgn_string))

    moves = list(game.mainline_moves())

    board = chess.Board()

    boards = [board.copy()]

    for move in moves:

        board.push(move)

        boards.append(board.copy())

    return boards


@st.cache_data
def build_all_board_svgs(pgn_string: str):

    boards = build_all_boards(pgn_string)

    svgs = []

    for board in boards:

        svg = chess.svg.board(
            board=board,
            size=520,
            coordinates=True
        )

        svgs.append(svg)

    return svgs