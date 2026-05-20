# 2026 NBA Finals NLP Prediction Pipeline

An end-to-end Natural Language Processing (NLP) and Machine Learning pipeline designed to predict NBA Championship outcomes by analyzing the emotional and psychological state of teams during post-game press conferences. 

**Live Dashboard:** [Insert Streamlit Link Here]

## Core Architecture

This project operates on a 4-phase pipeline, transitioning unstructured audio/video data into a predictive probability matrix:

1. **Automated Ingestion:** Headless scraping of YouTube closed captions via `youtube-transcript-api` and `faster-whisper`.
2. **Sentiment Extraction (NLP):** Processing text through a locally hosted Hugging Face transformer (`SamLowe/roberta-base-go_emotions`) to generate 7-dimensional feature vectors.
3. **Data Visualization:** Generation of chronological emotion-state trajectories using Seaborn and Matplotlib.
4. **Machine Learning Inference:** A Random Forest Classifier trained on historical 2024/2025 playoff data to identify "Championship Mindsets" and predict series winners.

## System Requirements

- Python 3.10+
- `ffmpeg` (required for Whisper audio processing)
- Minimum 8GB RAM (16GB recommended for RoBERTa local execution)

## Setup & Execution

```bash
# 1. Clone the repository
git clone [https://github.com/ishansinha5/nba-finals-sentiment-analysis-2026.git](https://github.com/ishansinha5/nba-finals-sentiment-analysis-2026.git)
cd nba-finals-sentiment-analysis-2026

# 2. Establish Virtual Environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Dependencies
pip install -r requirements.txt

# 4. Execute the Pipeline
python main.py