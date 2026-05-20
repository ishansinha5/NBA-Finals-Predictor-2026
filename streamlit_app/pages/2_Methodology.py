import streamlit as st
import os

st.set_page_config(page_title="Methodology", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

st.title("System Architecture & Methodology")

st.markdown("""
### 1. Data Ingestion (The Whisper Pipeline)
Traditional stats are easy to scrape; raw audio is not. This pipeline utilizes the `youtube-transcript-api` to pull closed captions from official NBA pressers. For channels that disable captions, the pipeline proxies the video audio through a remote `faster-whisper` model to generate headless transcriptions. 

### 2. Emotional Scoring (RoBERTa)
Raw transcripts are processed through `SamLowe/roberta-base-go_emotions`, a locally executed Hugging Face transformer. 
* **Signal Maintenance (Head-Truncation):** Transcripts are hardcapped at 2500 characters. This prevents the model's context window from overflowing and ensures it scores the *player's* immediate emotional response, filtering out the long-winded, noisy questions from the media.
* **The 7 Features:** Every press conference is scored from 0.0 to 1.0 across: *Confidence, Contentment, Neutrality, Frustration, Upset, Anxiety, and Surprise*.
""")

# Example image of a trajectory
example_img = "streamlit_app/assets/Knicks_sentiment_trajectory.png"
if os.path.exists(example_img):
    st.image(example_img, caption="Example: Transforming raw text into chronological emotional trajectories.", use_container_width=True)

st.markdown("""
### 3. Inference (Random Forest)
A Random Forest Classifier was trained on the 2024 (Celtics/Mavericks) and 2025 (Thunder/Pacers) playoff runs. The model learned that "Championship Mindsets" are typically highly neutral and content. Teams that display erratic emotional spikes or raw, arrogant "Confidence" often trigger losing profiles in the algorithm.
""")