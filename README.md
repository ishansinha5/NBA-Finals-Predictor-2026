# 2026 NBA Finals NLP Prediction Pipeline

**Live App:** [Insert your Streamlit Cloud link here]

## Overview
An end-to-end Machine Learning pipeline that predicts NBA playoff outcomes by analyzing the emotional state of teams during post-game press conferences. 

## Architecture
- **Data Ingestion (`scripts/data_ingestion.py`):** Automated scraping of YouTube closed captions. Includes a resilient checkpointing system and a Hugging Face `faster-whisper` patch for headless videos.
- **NLP Scoring (`scripts/sentiment_engine.py`):** Processes transcripts through a local Hugging Face `SamLowe/roberta-base-go_emotions` model to generate feature vectors across 7 emotion categories. 
- **Visualization (`scripts/visualization.py`):** Matplotlib/Seaborn module mapping emotional trajectories across playoff stages.
- **ML Prediction (`scripts/predictor.py`):** A Random Forest Classifier trained on 2024/2025 historical data outputs championship probability metrics for the 2026 live run.
- **Deployment (`streamlit_app/`):** Python-native Streamlit dashboard.

## Next Steps (V2)
- **Dual-Engine Architecture:** Build an automated pipeline to handle live daily ingestion for ongoing series.
- **Enhanced ML:** Expand the historical dataset to address the "Confidence Bias" discovered in the 2024/2025 training loop.