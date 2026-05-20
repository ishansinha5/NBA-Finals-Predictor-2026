# Execution Scripts

This module contains the object-oriented Python classes that drive the pipeline.

## 1. `data_ingestion.py` (`TranscriptIngestor`)
Traditional stats are easy to scrape; raw audio is not. The `TranscriptIngestor` class interfaces with YouTube to extract closed captions. 

**The Spurs Dilemma:** A significant engineering challenge occurred during ingestion. While most NBA teams provide auto-captions, the San Antonio Spurs media channels aggressively disable them. Because a core constraint of this project was keeping the compute cost low and the architecture lean, I engineered a lightweight patch to extract the raw audio stream via `yt-dlp` and transcribe it locally, bypassing the need for expensive third-party transcription APIs.

## 2. `sentiment_engine.py` (`SentimentEngine`)
The NLP Feature Extractor. It initializes the Hugging Face `roberta-base-go_emotions` pipeline locally. 
* **The Truncation Strategy:** Transcripts are hardcapped at 2500 characters. This prevents context window overflow and ensures the model scores the immediate, raw emotional response of the player/coach, filtering out media noise.

## 3. `visualization.py` (`EmotionVisualizer`)
Data translation and visual mapping. Includes a custom string parsing loop to clean messy regular season data identifiers for readable X-axis plotting.

## 4. `predictor.py` (`PlayoffPredictor`)
The ML Inference engine. It loads the compiled `.pkl` Random Forest model, aggregates live team feature vectors via `mean()` pooling, and extracts class probabilities.