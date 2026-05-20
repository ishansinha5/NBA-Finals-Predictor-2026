# Data Layer

Contains the input JSON manifests and the output CSVs representing the state of the data pipeline. 
* The `TranscriptIngestor` chunks requests and saves to `raw_live_2026.csv` to avoid API blocks.
* The `SentimentEngine` reads the raw file and generates `scored_live_2026.csv` using RoBERTa feature mapping.