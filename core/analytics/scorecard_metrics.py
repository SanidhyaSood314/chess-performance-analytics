from datetime import datetime,timedelta
import pandas as pd


def compute_scorecard(df: pd.DataFrame):

    if df.empty:
        return {}

    total_games = len(df)

    # -----------------------------------
    # Results (using Score column)
    # -----------------------------------
    wins = len(df[df["Score"] == 1])
    draws = len(df[df["Score"] == 0.5])
    losses = len(df[df["Score"] == 0])

    # -----------------------------------
    # Average opponent rating
    # -----------------------------------
    avg_opponent_rating = df["OpponentElo"].mean()

    # -----------------------------------
    # Performance rating (simple estimate)
    # -----------------------------------
    score_sum = df["Score"].sum()
    expected = total_games / 2

    performance_rating = avg_opponent_rating + ((score_sum - expected) * 40)

    # -----------------------------------
    # Color breakdown
    # -----------------------------------
    white_games = df[df["PlayerColor"] == "White"]
    black_games = df[df["PlayerColor"] == "Black"]

    white_score = {
        "wins": len(white_games[white_games["Score"] == 1]),
        "draws": len(white_games[white_games["Score"] == 0.5]),
        "losses": len(white_games[white_games["Score"] == 0]),
    }

    black_score = {
        "wins": len(black_games[black_games["Score"] == 1]),
        "draws": len(black_games[black_games["Score"] == 0.5]),
        "losses": len(black_games[black_games["Score"] == 0]),
    }

    return {
        "total_games": total_games,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "avg_opponent_rating": round(avg_opponent_rating, 0),
        "performance_rating": round(performance_rating, 0),
        "white_score": white_score,
        "black_score": black_score,
    }


def apply_time_filter(df: pd.DataFrame, time_range: str) -> pd.DataFrame:
    """
    Filter games based on selected time range.
    """

    if df.empty or "DateTime" not in df.columns:
        return df

    now = datetime.now()

    # Normalize DateTime
    df = df.copy()
    df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")

    if time_range == "All":
        return df

    # ---------------------------------
    # Today
    # ---------------------------------
    if time_range == "Today":
        start = datetime(now.year, now.month, now.day)
        return df[df["DateTime"] >= start]

    # ---------------------------------
    # This Week (Monday start)
    # ---------------------------------
    if time_range == "This Week":
        start = now - timedelta(days=now.weekday())
        start = datetime(start.year, start.month, start.day)
        return df[df["DateTime"] >= start]

    # ---------------------------------
    # This Month
    # ---------------------------------
    if time_range == "This Month":
        start = datetime(now.year, now.month, 1)
        return df[df["DateTime"] >= start]

    return df