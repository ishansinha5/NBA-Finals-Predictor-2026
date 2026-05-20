# 2026 NBA Finals NLP Prediction Pipeline

**Live Dashboard:** [Insert Streamlit Link Here]

## The Question: Can we mathematically quantify a "Championship Mindset"?

I love basketball, and I’m obsessed with predicting who takes home the Larry O'Brien trophy. I’ve run the traditional statistical models—box scores, true shooting percentages, plus-minus ratings—but I wanted to build something different. Something that captures the *human* element. 

I built this Natural Language Processing (NLP) pipeline to branch out from traditional data science. I wanted to see if the emotional language used in post-game press conferences could reveal a team's psychological readiness to win a ring. 

![Knicks Trajectory](streamlit_app/assets/Knicks_sentiment_trajectory.png)

## Sustainable & Lean Engineering
A massive priority for this build was architectural efficiency. Instead of brute-forcing transcripts through expensive cloud APIs or massive, energy-intensive LLMs, this pipeline runs entirely on sustainable, locally executed small-parameter models (like `roberta-base-go_emotions`). It is computationally lean, highly cost-effective, and proves you don't need a massive cloud cluster to run powerful NLP.

## Core Architecture
This operates on a 4-phase pipeline, transitioning unstructured audio/video data into a predictive probability matrix:

1. **Automated Ingestion:** Headless scraping of YouTube closed captions via `youtube-transcript-api`. *(Note: Overcoming channels that disable closed captions—specifically the San Antonio Spurs media team—required custom audio-extraction and localized whisper transcription patching).*
2. **Sentiment Extraction (NLP):** Processing text through a local Hugging Face transformer to generate 7-dimensional emotional feature vectors.
3. **Data Visualization:** Generation of chronological emotion-state trajectories using Seaborn and Matplotlib.
4. **Machine Learning Inference:** A Random Forest Classifier trained on historical 2024/2025 playoff data to identify "Championship Mindsets" and predict series winners.