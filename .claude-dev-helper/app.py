"""
LIQID Prototype — Entry point
Runs: streamlit run .claude-dev-helper/app.py
"""
import streamlit as st

st.set_page_config(
    page_title="Smart Minds. Smart Money. | LIQID",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

pg = st.navigation(
    [
        st.Page("home.py",    title="LIQID",             url_path="",                 default=True),
        st.Page("analyse.py", title="Portfolio-Analyse", url_path="portfolio-analyse"),
    ],
    position="hidden",
)
pg.run()
