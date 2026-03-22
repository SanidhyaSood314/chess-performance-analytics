import streamlit as st


def render_move_navigation(moves):

    col_prev, col_next, col_jump = st.columns([1, 1, 3])

    with col_prev:
        if st.button("⏮ Previous Move"):
            st.session_state.move_index = max(
                0,
                st.session_state.move_index - 1
            )

    with col_next:
        if st.button("Next Move ⏭"):
            st.session_state.move_index = min(
                len(moves),
                st.session_state.move_index + 1
            )

    with col_jump:

        st.session_state.move_index = st.number_input(
            "Jump to Move",
            min_value=0,
            max_value=len(moves),
            value=st.session_state.move_index
        )

    return st.session_state.move_index