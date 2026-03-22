# core/analytics/analytics.py

import pandas as pd


# ---------------------------
# Overall Stats
# ---------------------------

def compute_overall_stats(df: pd.DataFrame) -> dict:

    total_games = len(df)
    total_score = df["Score"].sum()

    wins = (df["Score"] == 1.0).sum()
    draws = (df["Score"] == 0.5).sum()
    losses = (df["Score"] == 0.0).sum()

    win_rate = wins / total_games if total_games > 0 else 0
    average_score = total_score / total_games if total_games > 0 else 0

    return {
        "total_games": total_games,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "win_rate": round(win_rate, 3),
        "average_score": round(average_score, 3),
    }


# ---------------------------
# Grouped Performance
# ---------------------------

def performance_by_color(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("PlayerColor")["Score"]\
        .agg(games="count", average_score="mean")\
        .reset_index()


def performance_by_format(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("Format")["Score"]\
        .agg(games="count", average_score="mean")\
        .reset_index()


# ---------------------------
# Rating Band Analysis
# ---------------------------

def performance_by_rating_band(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df["RatingDiff"] = df["PlayerElo"] - df["OpponentElo"]

    def classify(diff):
        if pd.isna(diff):
            return "Unknown"
        if diff <= -200:
            return "Much Higher Opponent"
        if diff < -50:
            return "Slightly Higher Opponent"
        if diff <= 50:
            return "Equal Strength"
        if diff < 200:
            return "Slightly Lower Opponent"
        return "Much Lower Opponent"

    df["RatingBand"] = df["RatingDiff"].apply(classify)

    return df.groupby("RatingBand")["Score"]\
        .agg(games="count", average_score="mean")\
        .reset_index()


# ---------------------------
# Rolling Performance
# ---------------------------

def rolling_performance(df: pd.DataFrame, window: int = 50) -> pd.DataFrame:
    df_sorted = df.sort_values("DateTime").reset_index(drop=True)
    df_sorted["RollingScore"] = df_sorted["Score"].rolling(window=window).mean()
    return df_sorted[["DateTime", "RollingScore"]]


# ---------------------------
# Rating Progression
# ---------------------------

def rating_progression(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns rating progression over time.
    """

    df_sorted = df.sort_values("DateTime").reset_index(drop=True)

    return df_sorted[["DateTime", "PlayerElo"]]


# ---------------------------
# Opening Risk Profile
# ---------------------------

def opening_risk_profile(
    df: pd.DataFrame,
    color: str,
    min_games: int = 15
) -> pd.DataFrame:
    """
    Win/Draw/Loss breakdown per opening for a specific color.
    """

    df_color = df[df["PlayerColor"] == color].copy()

    if df_color.empty:
        return pd.DataFrame()

    df_color["ResultType"] = df_color["Score"].map({
        1.0: "Win",
        0.5: "Draw",
        0.0: "Loss"
    })

    grouped = df_color.groupby(["Opening", "ResultType"])\
        .size()\
        .unstack(fill_value=0)

    grouped["games"] = grouped.sum(axis=1)

    grouped = grouped[grouped["games"] >= min_games]

    if grouped.empty:
        return pd.DataFrame()

    grouped["Win%"] = grouped.get("Win", 0) / grouped["games"]
    grouped["Draw%"] = grouped.get("Draw", 0) / grouped["games"]
    grouped["Loss%"] = grouped.get("Loss", 0) / grouped["games"]

    grouped["AverageScore"] = (
        grouped.get("Win", 0) * 1 +
        grouped.get("Draw", 0) * 0.5
    ) / grouped["games"]

    grouped = grouped.reset_index()

    return grouped.sort_values("AverageScore", ascending=False)