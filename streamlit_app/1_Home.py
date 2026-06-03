import streamlit as st
import sys
import os
sys.path.append(os.getcwd())
from utils.navigation import apply_global_styles, render_navigation

st.set_page_config(page_title="2026 NBA Finals NLP Predictor", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")
apply_global_styles()
render_navigation()

st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop", width="stretch")

st.markdown("## Project Motivation")
st.markdown("Standard basketball analytics focus on box score statistics. While those numbers show what happened on the court, they cannot capture the mental mindset of a locker room dealing with playoff intensity.")
st.markdown("I wanted to find a new angle by looking at text data from post-game podium press conferences. This project converts those transcripts into emotional scores to discover if steady linguistic composure acts as an indicator for tracking championship runs.")

st.markdown("## Core Project Steps")
st.markdown("""
### Phase 1: Tabular Sentiment and Predictive Analysis
* **Transcript Ingestion:** The pipeline maps game indexes to video tags, pulling available text tracks or sending media audio streams directly into a local speech to text model.
* **Linguistic Feature Extraction:** The system breaks down post-game statements to measure precise readings for emotions, including confidence, contentment, neutrality, frustration, upset, anxiety, and surprise.
* **The Scoring Filter Boundary:** To protect the models, I stop collecting transcript data exactly one game before a series is decided. This prevents the highly celebratory emotional spikes of a clinching game from poisoning our regular series indicators.
* **Roster Layer Classification:** The data is flattened independently across coaches, franchise stars, and teammates to see how aligned a group stays during a series.
""")