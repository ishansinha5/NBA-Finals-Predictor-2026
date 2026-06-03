import streamlit as st
from utils.navigation import apply_global_styles, render_navigation

st.set_page_config(page_title="Design Journey", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")
apply_global_styles()
render_navigation()

st.header("The Architectural Evolution: V1 vs. V2")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Legacy V1 Paradigm: The Proof of Concept")
    st.markdown("""
    * **Restricted Data Footprint:** Evaluated only two years of data.
    * **Linguistic Truncation:** Used basic hard truncation, which missed context.
    * **Tabular Blind Spot:** Lacked granular multi-role separation.
    * **Survival Bias:** Only trained on Finals teams, missing early exit dynamics.
    """)

with col2:
    st.markdown("### Upgraded V2 Framework: The Production Pipeline")
    st.markdown("""
    * **Preservation of the Score Filter:** I removed clinching game celebrations to maintain baseline integrity.
    * **Tri-Tier Role Isolation:** The feature matrix now separates unique team dynamics across three distinct roles.
    * **Multi-Season Historical Scaling:** The pipeline includes older seasons to broaden baselines.
    * **Dual Hybrid Processing:** Integrated a generative RAG pipeline alongside a dedicated opponent model.
    """)