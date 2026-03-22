# core/data/feature_engineering.py

import pandas as pd
from typing import Optional


# ---------------------------------
# Core Helpers
# ---------------------------------

def determine_player_color(row: pd.Series, username: str) -> Optional[str]:
    if row["White"] == username:
        return "White"
    if row["Black"] == username:
        return "Black"
    return None


def compute_score(result: str, player_color: str) -> float:
    if result == "1-0":
        return 1.0 if player_color == "White" else 0.0
    if result == "0-1":
        return 1.0 if player_color == "Black" else 0.0
    if result == "1/2-1/2":
        return 0.5
    return 0.0


def categorize_time_control(time_control: str) -> str:
    if not time_control or time_control == "-":
        return "Unknown"

    try:
        if "/" in time_control:
            return "Daily"

        base = int(time_control.split("+")[0])
        minutes = base / 60

        if minutes < 3:
            return "Bullet"
        if minutes <= 8:
            return "Blitz"
        if minutes <= 25:
            return "Rapid"
        return "Classical"

    except Exception:
        return "Unknown"


# ---------------------------------
# Opening Processing
# ---------------------------------

def extract_opening_name(row):
    """
    Get full readable opening name.
    Prefer Opening header.
    Fallback to ECOUrl.
    """
    if isinstance(row["Opening"], str) and row["Opening"] != "Unknown":
        return row["Opening"]

    eco_url = row.get("ECOUrl")
    if isinstance(eco_url, str) and "openings" in eco_url:
        name_part = eco_url.split("/")[-1]
        return name_part.replace("-", " ")

    return "Unknown"


def extract_opening_family(opening_name: str) -> str:
    """
    Simplify opening into first 2 words.
    Example:
        'Sicilian Defense Najdorf Variation'
        -> 'Sicilian Defense'
    """
    if not isinstance(opening_name, str):
        return "Unknown"

    words = opening_name.split()

    if len(words) >= 2:
        return " ".join(words[:2])

    return opening_name


# ---------------------------------
# Main Feature Engineering
# ---------------------------------

def engineer_features(df: pd.DataFrame, username: str) -> pd.DataFrame:

    df = df.copy()

    # Player Color
    df["PlayerColor"] = df.apply(
        lambda row: determine_player_color(row, username),
        axis=1
    )

    df = df[df["PlayerColor"].notnull()]

    # Ratings
    df["PlayerElo"] = df.apply(
        lambda row: row["WhiteElo"] if row["PlayerColor"] == "White"
        else row["BlackElo"],
        axis=1
    )

    df["OpponentElo"] = df.apply(
        lambda row: row["BlackElo"] if row["PlayerColor"] == "White"
        else row["WhiteElo"],
        axis=1
    )

    df["PlayerElo"] = pd.to_numeric(df["PlayerElo"], errors="coerce")
    df["OpponentElo"] = pd.to_numeric(df["OpponentElo"], errors="coerce")

    # Score
    df["Score"] = df.apply(
        lambda row: compute_score(row["Result"], row["PlayerColor"]),
        axis=1
    )

    # Format
    df["Format"] = df["TimeControl"].apply(categorize_time_control)

    # DateTime
    date_part = df["UTCDate"].fillna(df["Date"]).fillna("")
    time_part = df["UTCTime"].fillna("00:00:00")

    df["DateTime"] = pd.to_datetime(
        date_part + " " + time_part,
        errors="coerce"
    )

    # Opening Full Name
    df["Opening"] = df.apply(extract_opening_name, axis=1)

    # Opening Family (2-word simplification)
    df["OpeningFamily"] = df["Opening"].apply(extract_opening_family)

    df["ECO"] = df["ECO"].fillna("Unknown")

    return df[
        [
            "DateTime",
            "PlayerColor",
            "PlayerElo",
            "OpponentElo",
            "Result",
            "Score",
            "Format",
            "Opening",
            "OpeningFamily",
            "ECO",
            "PGN",
        ]
    ].reset_index(drop=True)