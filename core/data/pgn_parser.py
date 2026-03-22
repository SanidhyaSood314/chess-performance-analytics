# core/data/pgn_parser.py

import chess.pgn
import pandas as pd
import io
from typing import Union


def parse_pgn(source: Union[str, object]) -> pd.DataFrame:
    """
    Parse PGN from:
    - Raw PGN string
    - Streamlit uploaded file object

    Returns DataFrame with game metadata + full PGN.
    """

    if isinstance(source, str):
        string_io = io.StringIO(source)
    else:
        string_io = io.StringIO(source.getvalue().decode("utf-8"))

    games_data = []

    while True:
        game = chess.pgn.read_game(string_io)
        if game is None:
            break

        headers = game.headers

        games_data.append({
            "Event": headers.get("Event"),
            "Date": headers.get("Date"),
            "UTCDate": headers.get("UTCDate"),
            "UTCTime": headers.get("UTCTime"),
            "White": headers.get("White"),
            "Black": headers.get("Black"),
            "WhiteElo": headers.get("WhiteElo"),
            "BlackElo": headers.get("BlackElo"),
            "Result": headers.get("Result"),
            "TimeControl": headers.get("TimeControl"),
            "Opening": headers.get("Opening"),
            "ECO": headers.get("ECO"),
            "ECOUrl": headers.get("ECOUrl"),
            "PGN": str(game)
        })

    return pd.DataFrame(games_data)