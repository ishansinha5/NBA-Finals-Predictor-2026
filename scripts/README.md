# Pipeline Execution Scripts

This directory contains the object-oriented Python classes and batch-processing scripts that drive the machine learning pipeline. It is architected into three distinct layers: the **Core Sentiment Engine**, the **Intelligence Retrieval Layer**, and the **Batch Orchestration Runners**.

## 1. Core Sentiment & Predictive Engine

* **`data_ingestion.py` (`TranscriptIngestor`):** Interfaces with the YouTube API. It implements a resilient checkpointing system (`.ingestion_checkpoint`) to handle rate-limiting. It includes a critical fallback loop: if YouTube's closed captions are missing (common for restricted media feeds), it triggers a local `faster-whisper` transcription instance to process raw audio streams directly, ensuring data continuity for teams like the Spurs.
* **`sentiment_engine.py` (`SentimentEngine`):** Wraps the `roberta-base-go_emotions` pipeline. It processes transcripts by chunking documents into 400-word segments to stay within the transformer's maximum sequence length. It aggregates 7-dimensional emotional vectors (confidence, content, neutrality, frustration, upset, anxiety, surprise) to calculate mean sentiment density across entire interviews.
* **`predictor.py` (`PlayoffPredictor`):** Contains the Random Forest ML logic. It handles the "flattening" of series-level data into a 28-column feature matrix (4 roles × 7 emotion vectors). It includes logic to train on both a "Full Baseline" (2020-2025) and a "Modern Era" optimized set, utilizing `joblib` for model persistence and defensive fallback weighting to handle class imbalance.

## 2. Intelligence & Retrieval (RAG)

* **`rag_pipeline.py` (`SportsIntelligenceRAG`):** Handles the Retrieval-Augmented Generation track. It uses `RecursiveCharacterTextSplitter` to partition texts into semantic chunks and encodes them via `all-MiniLM-L6-v2` embeddings. It interfaces with a local `ChromaDB` instance to perform vector-space cosine similarity lookups based on tactical queries. I did this solely so that I could see if I COULD make a RAG Pipeline, though I chose not to out of maintaining my environmental goals.  The next script helps me continue this:
* **`offline_rag_tester.py`:** A diagnostic utility for pipeline validation. It runs a standalone query against the local `ChromaDB` instance to verify that semantic node retrieval is functioning correctly, allowing for rapid debugging of the vector store outside of the Streamlit UI.

## 3. Orchestration & Visualization Runners

These scripts automate the generation of assets. Running these executes the heavy compute tasks required to populate the `output/` and `streamlit_app/assets/` folders.

* **`visualization.py` (`EmotionVisualizer`):** The primary plotting engine. It utilizes `matplotlib` and `seaborn` to translate score vectors into trajectory line graphs and comparative bar charts. It includes custom sanitization logic to convert raw stage tags (e.g., "R1G1") into human-readable X-axis labels and handles opponent-to-champ mapping dynamically.
* **`graph_historical.py`:** Executes the historical batch for 2019–2022 champions. It maps the aggregate emotional trends for each title winner and generates comparison bars against their respective Finals runners-up.
* **`graph_modern.py`:** Executes the modern batch (2023–2025). It follows the same trajectory plotting logic as the historical script but maps against the high-density datasets required for modern precision.
* **`graph_live_2026.py`:** The active runtime script. It processes the live 2026 postseason bracket, generating the trajectory and match-up bar charts specifically for the Spurs, Knicks, Thunder, and Cavaliers.
* **`predict_finals.py`:** The inference driver. It loads the `playoff_rf_model_modern_only.pkl`, performs final feature aggregation, and executes the synthesis logic that generates the `2026_Finals_Report.md`.

***

### Engineering Notes
* **Data Imputation:** Historical datasets (pre-2023) contained significant transcript sparseness. The ingestion pipeline employs linear imputation on the `scored_*.csv` files to bridge these gaps, ensuring visual trajectory continuity while maintaining statistical integrity.
* **Environmental Integrity:** Ensure all `requirements.txt` dependencies, including `chromadb` and `faster-whisper`, are installed in your active virtual environment before executing these scripts, as several runners rely on locally cached transformer weights.