import streamlit as st

st.set_page_config(page_title="2026 NBA Finals Predictor", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

# Clean, dynamic basketball banner
st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop", use_container_width=True)

st.title("2026 NBA Finals NLP Predictor")
st.subheader("Predicting the Larry O'Brien Trophy through Press Conference NLP")

st.markdown("""
### The Question: Can we mathematically quantify a "Championship Mindset"?

I love basketball, and I love predicting who takes home the championship. I’ve run the traditional statistical models—box scores, true shooting percentages, plus-minus ratings—but I wanted to build something different. Something that captures the *human* element of a playoff run. 

I built this Natural Language Processing (NLP) pipeline to branch out from traditional data science. I wanted to see if the emotional language used in post-game press conferences could reveal a team's psychological readiness to win a ring.

### The Constraint: Sustainable, Lean Computing
A massive priority for this build was architectural efficiency. Instead of brute-forcing transcripts through expensive cloud APIs or massive, energy-intensive LLMs, this pipeline runs entirely on sustainable, locally executed small-parameter models (like `roberta-base-go_emotions`). It is computationally lean without sacrificing predictive power.

### How it Works
This project scrapes YouTube closed captions of the 2026 Final Four (Knicks, Cavaliers, Spurs, Thunder), scores the transcripts across 7 distinct emotions using RoBERTa, and maps those feature vectors against a historical Random Forest model trained on the 2024 and 2025 NBA Finals.

**(Use the sidebar `>` on the top left to navigate the dashboard.)**
""")