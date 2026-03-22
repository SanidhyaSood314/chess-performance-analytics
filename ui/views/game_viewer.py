import streamlit as st
import chess
import chess.svg
import time

from services.game_state_service import (
    build_game_labels,
    load_game_state
)

from ui.components.board_component import render_chessboard
from ui.components.eval_bar_component import render_eval_bar
from ui.components.eval_graph_component import render_eval_graph
from ui.components.move_navigation_component import render_move_navigation
from ui.components.classification_component import render_move_classification
from ui.components.move_list_component import render_move_list
from ui.components.flip_board_component import render_flip_button
from ui.components.pv_line_component import render_engine_line

from core.analytics.accuracy_calculator import calculate_separate_accuracy
from core.analytics.blunder_explainer import explain_move
from core.data.opening_detector import detect_opening
from core.intelligence.pattern_detector import detect_error_patterns
from core.intelligence.insight_generator import generate_insights
from core.intelligence.phase_analyzer import analyze_phase_accuracy
from core.intelligence.recommendation_engine import generate_recommendations
from core.intelligence.report_generator import generate_game_report


def render_game_viewer(filtered_df):

    start_time = time.time()

    st.markdown("## ♟ Game Viewer")

    if filtered_df.empty:
        st.info("No games available.")
        return

    flipped = render_flip_button()

    game_labels, game_indices = build_game_labels(filtered_df)

    selected_label = st.selectbox("Select Game", game_labels)

    game_index = game_indices[game_labels.index(selected_label)]

    pgn_string = filtered_df.loc[game_index]["PGN"]
    player_color = filtered_df.loc[game_index]["PlayerColor"]

    load_game_state(pgn_string)

    moves = st.session_state.moves
    boards = st.session_state.boards
    analysis_data = st.session_state.analysis_data

    opening_name, variation = detect_opening(pgn_string)

    if variation:
        st.markdown(f"**Opening:** {opening_name} — {variation}")
    else:
        st.markdown(f"**Opening:** {opening_name}")
    st.markdown(f"**Analyzing as:** {player_color}")
    move_index = render_move_navigation(moves)

    board = boards[move_index]

    last_move = None
    arrows = []

    current_eval = 0
    current_classification = None
    move_display = "Starting Position"

    move_data = None

    if move_index > 0:

        move_data = analysis_data[move_index - 1]

        last_move = moves[move_index - 1]

        best_move = move_data.best_move

        arrows = [
            chess.svg.Arrow(
                best_move.from_square,
                best_move.to_square,
                color="#1f77b4"
            )
        ]

        current_eval = move_data.eval_after
        current_classification = move_data.classification

        move_number = move_data.move_number
        side = "White" if move_data.is_white_move else "Black"
        move_display = f"Move {move_number} ({side})"

    svg_board = chess.svg.board(
        board=board,
        lastmove=last_move,
        arrows=arrows,
        size=520,
        flipped=flipped
    )

    col_eval, col_board, col_moves = st.columns([1, 5, 3])

    with col_eval:
        render_eval_bar(current_eval, flipped)

    with col_board:
        render_chessboard(svg_board)

    with col_moves:
        render_move_list(moves,boards ,analysis_data)

    render_move_classification(current_classification, move_display)

    render_engine_line(move_data)

    if move_data:

        explanation = explain_move(
            board,
            last_move,
            move_data.eval_before,
            move_data.eval_after
        )

        if explanation:
            st.info(explanation)

    st.divider()

    render_eval_graph(analysis_data, pgn_string)

    white_acc, black_acc = calculate_separate_accuracy(analysis_data)

    st.markdown(
        f"""
        **White Accuracy:** {white_acc}%  
        **Black Accuracy:** {black_acc}%
        """
    )

    patterns = detect_error_patterns(analysis_data, player_color)

    st.markdown("### 🧠 Error Patterns")

    for phase, data in patterns["phases"].items():
        st.write(
            f"**{phase.capitalize()}** — "
            f"Inaccuracies: {data['inaccurate']}, "
            f"Mistakes: {data['mistake']}, "
            f"Blunders: {data['blunder']}"
        )
    st.markdown("---")

    insights = generate_insights(patterns)

    st.markdown("### 💡 Key Insights")

    for insight in insights:
        st.write(f"- {insight}")
    st.markdown("---")

    phase_analysis = analyze_phase_accuracy(analysis_data, player_color)

    st.markdown("### 📊 Phase Performance")

    for phase in ["opening", "middlegame", "endgame"]:

        acc = phase_analysis["accuracy"][phase]
        strength = phase_analysis["strength"][phase]

        if acc is None:
            st.write(f"**{phase.capitalize()}** — No data")
        else:
            st.write(
                f"**{phase.capitalize()}** — Accuracy: {acc}% ({strength})"
            )
    st.markdown("---")
    
    
    recommendations = generate_recommendations(patterns, phase_analysis)

    st.markdown("### 🎯 Recommendations")

    for rec in recommendations:
        st.markdown(f"- {rec}")

    report = generate_game_report(
        player_color,
        phase_analysis,
        insights,
        recommendations
    )

    st.markdown("### 🧠 Game Summary")

    st.success(report)

    st.write("TOTAL RERUN TIME:", round(time.time() - start_time, 4))