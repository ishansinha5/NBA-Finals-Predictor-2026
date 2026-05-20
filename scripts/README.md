# Execution Scripts

This module contains the object-oriented Python classes that drive the pipeline.

## 1. `data_ingestion.py` 
Traditional stats are easy to scrape; raw audio is not. The `TranscriptIngestor` class interfaces with YouTube to extract closed captions. It implements a resilient checkpointing system (`.ingestion_checkpoint`) to prevent duplicate API calls and uses sleep-delay logic to handle YouTube's strict rate-limiting during large data pulls.

## 2. `sentiment_engine.py` 
The NLP Feature Extractor. It initializes the Hugging Face `roberta-base-go_emotions` pipeline. 
* **The Truncation Strategy:** Transcripts are hardcapped at 2500 characters. This is a critical engineering decision. It prevents context window overflow and ensures the model scores the immediate, raw emotional response of the player/coach, actively filtering out the long-winded, noisy questions from the media.

## 3. `visualization.py` 
Data translation and visual mapping. Uses Seaborn's `darkgrid` style to map emotional trajectories. Includes a custom string parsing loop to clean messy regular season data identifiers (e.g., converting "Reg Season - Magic (Opponent)" to "Regular Season (Opp: Magic)") for highly readable X-axis plotting.

## 4. `predictor.py` 
The ML Inference engine. It loads the compiled `.pkl` Random Forest model, aggregates live team feature vectors via `mean()` pooling, and extracts class probabilities. It includes defensive programming to bypass `IndexError` crashes if the model is accidentally corrupted with single-class data, utilizing raw RoBERTa Confidence scores as a tie-breaking fallback.