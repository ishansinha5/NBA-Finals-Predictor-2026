import streamlit as st

st.set_page_config(
    page_title="2026 NBA Finals Predictor", 
    page_icon="🏀", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Clean, dynamic basketball banner
st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop", use_container_width=True)

st.title("2026 NBA Finals NLP Predictor")
st.subheader("Predicting the Larry O'Brien Trophy through Press Conference NLP")

st.markdown("""
I love basketball, and I’m obsessed with predicting who takes home the championship. I’ve run the traditional statistical models—box scores, true shooting percentages, plus-minus ratings—but I wanted to build something different. Something that captures the *human* element of a playoff run. 

I built this Natural Language Processing (NLP) pipeline to branch out from traditional data science and learn something new. I wanted to see if the emotional language used in post-game press conferences could actually reveal a team's championship mindset.

### What is this?
This project scrapes YouTube closed captions of the 2026 Final Four (Knicks, Cavaliers, Spurs, Thunder), scores the transcripts across 7 distinct emotions using a Hugging Face RoBERTa model, and maps those feature vectors against a historical Machine Learning model trained on the 2024 and 2025 NBA Finals.

**Use the sidebar (`>`) on the top left to navigate through the methodology, historical data, and live 2026 matchups.**
""")