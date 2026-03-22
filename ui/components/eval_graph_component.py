import streamlit as st
import plotly.graph_objects as go


def render_eval_graph(analysis_data, pgn_string):

    # ---------------------------------
    # Cache (already in your system)
    # ---------------------------------
    graph_cache = st.session_state.setdefault("eval_graph_cache", {})

    if pgn_string not in graph_cache:

        # ---------------------------------
        # Build evaluation list
        # ---------------------------------
        evals = [0]

        for move in analysis_data:
            evals.append(move.eval_after / 100)

        # ---------------------------------
        # FIX: Convert index → move labels
        # ---------------------------------
        x_labels = ["Start"]

        for i in range(1, len(evals)):
            move_number = (i + 1) // 2
            side = "W" if i % 2 == 1 else "B"
            x_labels.append(f"{move_number}{side}")

        # ---------------------------------
        # Create graph
        # ---------------------------------
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x_labels,
                y=evals,
                mode="lines+markers"
            )
        )

        # ---------------------------------
        # Layout
        # ---------------------------------
        fig.update_layout(
            height=300,
            title="Evaluation Over Time",
            xaxis_title="Move",
            yaxis_title="Evaluation (Pawns)",
            template="plotly_dark"
        )

        # Zero line (equal position)
        fig.add_hline(y=0)

        # ---------------------------------
        # Cache result
        # ---------------------------------
        graph_cache[pgn_string] = fig

    # ---------------------------------
    # Render
    # ---------------------------------
    st.plotly_chart(
        graph_cache[pgn_string],
        use_container_width=True
    )