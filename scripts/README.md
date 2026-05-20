# Execution Scripts

This module contains the object-oriented Python classes and patch scripts that drive the pipeline.

## 1. Core Engine
* **`data_ingestion.py` (`TranscriptIngestor`):** Interfaces with YouTube to extract closed captions. Implements a resilient checkpointing system (`.ingestion_checkpoint`) to prevent duplicate API calls and handle YouTube's rate-limiting.
* **`sentiment_engine.py` (`SentimentEngine`):** Initializes the Hugging Face `roberta-base-go_emotions` pipeline. **Crucial Optimization:** Transcripts are hardcapped at 2500 characters. This prevents context window overflow and ensures the model isolates the player's primary emotional state without getting noisy signals from long media questions.
* **`visualization.py` (`EmotionVisualizer`):** Maps emotional trajectories. Includes a string parsing loop to clean messy categorical data (e.g., converting "Reg Season - Magic" to "Regular Season (Opp: Magic)") for readable X-axis plotting.
* **`predictor.py` (`PlayoffPredictor`):** The ML Inference engine. Loads the `.pkl` Random Forest model, aggregates feature vectors via `mean()` pooling, and extracts probabilities. Includes defensive fallback logic to use raw Confidence scores if the model encounters single-class data errors.

## 2. Hardened Edge-Case Patches
Data pipelines are rarely perfect. These scripts were engineered to handle specific architectural failures and edge cases without bloating the core engine.

* **`whisper_patch.py` (The Spurs Dilemma):** While most NBA teams provide auto-captions, the San Antonio Spurs aggressively disable them. Because a core constraint of this project was sustainable, lean computing, I built a two-tier extraction patch. It first attempts to proxy the video through a lightweight Hugging Face Gradio Space API. If that times out, it cascades gracefully to a local `yt-dlp` audio extraction and processes the waveform through `faster-whisper`. It sanitizes the output and generates a CSV-safe patch file.
* **`homogenize_csv.py` (Schema Alignment):** A utility script built to repair corrupted data ingestions. During a specific scrape, PyArrow typing failed due to a schema shift (thousands of characters of transcript data shifted into the integer `won_championship` column, rendering `transcript` as NaN). This script generates boolean masks to isolate the affected Spurs rows, shifts the textual data back to the correct column, and resets the target variable to `"0"`, saving the pipeline from catastrophic downstream type-errors.