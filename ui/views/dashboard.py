# ui/views/dashboard.py

import streamlit as st
import plotly.express as px
import time

from core.analytics.performance_metrics import (
    compute_overall_stats,
    performance_by_color,
    performance_by_format,
    performance_by_rating_band,
    rolling_performance,
    rating_progression,
    opening_risk_profile,
)

from ui.views.game_viewer import render_game_viewer
from ui.views.scorecard import render_scorecard


def render_dashboard(filtered_df, features_df):

    dashboard_start = time.time()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Performance",
        "📈 Trends",
        "📚 Openings",
        "♟ Game Viewer",
        "📋 Scorecard"
    ])

    # ==========================================
    # 📊 PERFORMANCE TAB
    # ==========================================
    with tab1:

        t0 = time.time()
        stats = compute_overall_stats(filtered_df)
        st.write("compute_overall_stats:", round(time.time() - t0, 4), "seconds")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Games", stats["total_games"])
        col2.metric("Wins", stats["wins"])
        col3.metric("Draws", stats["draws"])
        col4.metric("Losses", stats["losses"])
        col5.metric("Win Rate", f"{stats['win_rate']*100:.1f}%")

        st.divider()

        colA, colB = st.columns(2)

        with colA:

            t0 = time.time()
            df_format = performance_by_format(filtered_df)
            st.write("performance_by_format:", round(time.time() - t0, 4), "seconds")

            st.subheader("Performance by Format")
            st.dataframe(df_format, use_container_width=True)

        with colB:

            t0 = time.time()
            df_color = performance_by_color(filtered_df)
            st.write("performance_by_color:", round(time.time() - t0, 4), "seconds")

            st.subheader("Performance by Color")
            st.dataframe(df_color, use_container_width=True)

        st.divider()

        t0 = time.time()
        df_rating = performance_by_rating_band(filtered_df)
        st.write("performance_by_rating_band:", round(time.time() - t0, 4), "seconds")

        st.subheader("Performance by Rating Band")
        st.dataframe(df_rating, use_container_width=True)

    # ==========================================
    # 📈 TRENDS TAB
    # ==========================================
    with tab2:

        t0 = time.time()
        rolling_df = rolling_performance(filtered_df)
        st.write("rolling_performance:", round(time.time() - t0, 4), "seconds")

        fig_roll = px.line(
            rolling_df,
            x="DateTime",
            y="RollingScore",
            title="Rolling Average Score (50 Games)"
        )

        st.plotly_chart(fig_roll, use_container_width=True)

        st.divider()

        selected_format = st.selectbox(
            "Select Format",
            sorted(filtered_df["Format"].unique())
        )

        t0 = time.time()
        rating_df = rating_progression(
            filtered_df[filtered_df["Format"] == selected_format]
        )
        st.write("rating_progression:", round(time.time() - t0, 4), "seconds")

        fig_rating = px.line(
            rating_df,
            x="DateTime",
            y="PlayerElo",
            title=f"{selected_format} Rating Over Time"
        )

        st.plotly_chart(fig_rating, use_container_width=True)

    # ==========================================
    # 📚 OPENINGS TAB
    # ==========================================
    with tab3:

        st.subheader("Opening Family Frequency")

        t0 = time.time()
        opening_freq = (
            filtered_df["OpeningFamily"]
            .value_counts()
            .reset_index()
        )
        st.write("opening frequency computation:", round(time.time() - t0, 4), "seconds")

        opening_freq.columns = ["Opening Family", "Games"]

        st.dataframe(opening_freq, use_container_width=True)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("White — Opening Risk Profile")

            t0 = time.time()
            white_profile = opening_risk_profile(
                filtered_df,
                color="White",
                min_games=10
            )
            st.write("white opening_risk_profile:", round(time.time() - t0, 4), "seconds")

            if not white_profile.empty:
                white_profile = white_profile.rename(
                    columns={"Opening": "OpeningFamily"}
                )

            st.dataframe(white_profile, use_container_width=True)

        with col2:

            st.subheader("Black — Opening Risk Profile")

            t0 = time.time()
            black_profile = opening_risk_profile(
                filtered_df,
                color="Black",
                min_games=10
            )
            st.write("black opening_risk_profile:", round(time.time() - t0, 4), "seconds")

            if not black_profile.empty:
                black_profile = black_profile.rename(
                    columns={"Opening": "OpeningFamily"}
                )

            st.dataframe(black_profile, use_container_width=True)

    # ==========================================
    # ♟ GAME VIEWER TAB
    # ==========================================
    with tab4:

        t0 = time.time()
        render_game_viewer(filtered_df)
        st.write("render_game_viewer:", round(time.time() - t0, 4), "seconds")


    # ==========================================
    # 📋 SCORECARD TAB
    # ==========================================
    with tab5:

        t0 = time.time()
        render_scorecard(filtered_df)
        st.write("render_scorecard:", round(time.time() - t0, 4), "seconds")

    # ==========================================
    # TOTAL DASHBOARD TIME
    # ==========================================

    st.sidebar.markdown("### ⏱ Dashboard Performance")

    total_time = time.time() - dashboard_start

    st.sidebar.write("Total dashboard render time:", round(total_time, 4), "seconds")