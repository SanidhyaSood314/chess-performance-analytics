import streamlit as st


def render_app_header(title: str, description: str):
    """
    Render application title and description.
    """

    st.title(title)
    st.markdown(description)