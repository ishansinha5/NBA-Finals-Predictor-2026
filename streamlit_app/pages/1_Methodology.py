import streamlit as st

st.title("System Architecture & Methodology")

st.markdown("""
### 1. Data Ingestion
The pipeline utilizes the `youtube-transcript-api` to scrape closed captions from official NBA press conferences. For channels that disable captions, a custom patch script proxies the video through a Hugging Face Gradio Space running `faster-whisper`.

### 2. Emotional Scoring (RoBERTa)
Raw transcripts are processed through `SamLowe/roberta-base-go_emotions`, a locally executed Hugging Face transformer. 
* **Signal Maintenance:** The script truncates texts at the 2500-character mark (approx. 400 words) to ensure the model analyzes the core sentiment of the player/coach, rather than getting noisy signals from long, meandering media questions.
* **The 7 Features:** The text is scored from 0.0 to 1.0 across: *Confidence, Contentment, Neutrality, Frustration, Upset, Anxiety, and Surprise*.

### 3. Inference (Random Forest)
A Random Forest Classifier was trained on the 2024 (Celtics/Mavericks) and 2025 (Thunder/Pacers) playoff runs. The model learned that "Championship Mindsets" are typically highly neutral and content, while raw "Confidence" often correlates with losing profiles. 
""")