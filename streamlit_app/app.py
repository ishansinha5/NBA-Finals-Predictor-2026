import streamlit as st

st.set_page_config(page_title="2026 NBA Finals Predictor", page_icon="🏀", layout="wide")

st.title("2026 NBA Finals NLP Predictor")
st.subheader("Predicting Championship Mindsets through Press Conference NLP")

st.markdown("""
Welcome to the MVP release of the NBA Finals NLP prediction pipeline. 

This project explores a psychological hypothesis: **Can we predict an NBA Championship by analyzing the emotional signals of a team's press conferences?**

Using a custom Natural Language Processing (NLP) pipeline, this project scrapes YouTube closed captions, scores the transcripts across 7 distinct emotions using a RoBERTa model, and maps those feature vectors against a historical Random Forest model trained on the 2024 and 2025 NBA Finals.

### How to use this dashboard:
Use the sidebar on the left to navigate:
- **Methodology:** A deeper dive into how the pipeline ingests, scores, and predicts.
- **Matchups:** Interactive dashboards displaying the emotional profile of the 2026 Final Four (Knicks, Cavaliers, Spurs, Thunder) and the algorithm's predictions for every possible head-to-head permutation.
""")