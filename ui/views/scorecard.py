import streamlit as st
import pandas as pd

from core.analytics.scorecard_metrics import apply_time_filter


def render_scorecard(df: pd.DataFrame):

    st.markdown("## 📊 Scorecard")

    # ---------------------------------
    # Time Range Filter
    # ---------------------------------
    time_range = st.selectbox(
        "Select Time Range",
        ["All", "Today", "This Week", "This Month"]
    )

    # Apply filter
    df = apply_time_filter(df, time_range)

    # ---------------------------------
    # Handle Empty Data
    # ---------------------------------
    if df.empty:
        st.warning("No games available for selected time range.")
        return

    # ---------------------------------
    # Basic Metrics
    # ---------------------------------
    total_games = len(df)

    wins = (df["Score"] == 1).sum()
    draws = (df["Score"] == 0.5).sum()
    losses = (df["Score"] == 0).sum()

    win_rate = round((wins / total_games) * 100, 2)

    # ---------------------------------
    # Display Metrics
    # ---------------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Games", total_games)
    col2.metric("Wins", wins)
    col3.metric("Draws", draws)
    col4.metric("Losses", losses)

    st.markdown(f"### Win Rate: {win_rate}%")

    # ---------------------------------
    # Performance by Color
    # ---------------------------------
    st.markdown("### 🎨 Performance by Color")

    white_df = df[df["PlayerColor"] == "White"]
    black_df = df[df["PlayerColor"] == "Black"]

    def calc_win_rate(sub_df):
        if len(sub_df) == 0:
            return 0
        return round((sub_df["Score"].sum() / len(sub_df)) * 100, 2)

    white_wr = calc_win_rate(white_df)
    black_wr = calc_win_rate(black_df)

    col1, col2 = st.columns(2)
    col1.metric("White Win %", f"{white_wr}%")
    col2.metric("Black Win %", f"{black_wr}%")

    # ---------------------------------
    # Performance Rating
    # ---------------------------------
    st.markdown("### 📈 Performance Rating")

    avg_opponent = df["OpponentElo"].mean()
    score_ratio = df["Score"].mean()

    performance = avg_opponent + 400 * (score_ratio - 0.5)
    performance = round(performance, 0)

    st.metric("Performance Rating", int(performance))

    # ---------------------------------
    # Average Ratings
    # ---------------------------------
    st.markdown("### 📊 Ratings")

    avg_player_elo = round(df["PlayerElo"].mean(), 0)
    avg_opponent_elo = round(df["OpponentElo"].mean(), 0)

    col1, col2 = st.columns(2)
    col1.metric("Your Avg Rating", int(avg_player_elo))
    col2.metric("Opponent Avg Rating", int(avg_opponent_elo))