# Execution Scripts

This module contains the object-oriented Python classes that drive the pipeline.

## 1. `data_ingestion.py` (`TranscriptIngestor`)
* **Role:** Interfaces with YouTube to extract closed captions.
* **Logic:** Attempts standard `youtube-transcript-api` extraction. If blocked or captions are disabled, it reroutes the audio via `yt-dlp` to a remote Gradio Space running `faster-whisper` for headless transcription. Implements a sleep-delay loop to bypass IP rate limiting.

## 2. `sentiment_engine.py` (`SentimentEngine`)
* **Role:** NLP Feature Extraction.
* **Logic:** Initializes the Hugging Face `roberta-base-go_emotions` pipeline. 
* **Optimization:** Implements head-truncation on transcripts (hardcapped at 2500 characters). This prevents context window overflow and ensures the model scores the immediate, raw emotional response of the player/coach, filtering out long-winded media questions.

## 3. `visualization.py` (`EmotionVisualizer`)
* **Role:** Data translation and visual mapping.
* **Logic:** Uses Seaborn's `darkgrid` style to map emotional trajectories. Includes a custom string parsing loop to clean messy regular season data identifiers (e.g., converting "Reg Season - Magic (Opponent)" to "Regular Season (Opp: Magic)") for readable X-axis plotting.

## 4. `predictor.py` (`PlayoffPredictor`)
* **Role:** ML Inference and output generation.
* **Logic:** Loads the `.pkl` model, aggregates live team feature vectors via `mean()`, and extracts class probabilities. Includes defensive programming to bypass `IndexError` crashes if the model is accidentally corrupted with single-class data, utilizing raw RoBERTa Confidence scores as a tie-breaking fallback.