import json
import pandas as pd
import os
import logging

# Importing our custom V2 classes
from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_historical_pipeline(json_path, output_raw_name, output_scored_name):
    # 1. Load the JSON manifest
    with open(json_path, 'r') as f:
        video_metadata = json.load(f)

    logging.info(f"Loaded {len(video_metadata)} videos from {json_path}")

    # 2. Ingest Transcripts (Tier 1: YT API, Tier 2: Whisper Fallback)
    ingestor = TranscriptIngestor(data_dir="./data/historical/")
    raw_df = ingestor.fetch_transcripts(video_metadata, save_filename=output_raw_name)

    if (raw_df.empty):
        logging.error("No transcripts were fetched. Pipeline stopped.")
        return

    logging.info(f"Successfully ingested {len(raw_df)} transcripts. Moving to RoBERTa scoring...")

    # 3. Score the Transcripts (V2 400-Word Chunking Engine)
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)

    # 4. Save the final scored dataset
    output_dir = "./data/historical/"
    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)

    final_path = os.path.join(output_dir, output_scored_name)
    scored_df.to_csv(final_path, index=False)
    
    logging.info(f"Pipeline Complete! Scored data successfully saved to {final_path}")

if __name__ == "__main__":
    # Updated to the new 2024-2025 manifest
    manifest_path = "./data/2024-2025_playoff_vids.json"
    
    run_historical_pipeline(
        json_path=manifest_path,
        output_raw_name="raw_2023_2024.csv",
        output_scored_name="scored_2023_2024.csv"
    )