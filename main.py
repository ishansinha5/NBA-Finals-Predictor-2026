import json
import pandas as pd
import os
import logging

from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_historical_pipeline(json_path, output_raw_name, output_scored_name):
    with open(json_path, 'r') as f:
        video_metadata = json.load(f)

    logging.info(f"Loaded {len(video_metadata)} videos from {json_path}")

    # Tier 1 & Fallback Local Whisper Pipeline
    ingestor = TranscriptIngestor(data_dir="./data/historical/")
    raw_df = ingestor.fetch_transcripts(video_metadata, save_filename=output_raw_name)

    if (raw_df.empty):
        logging.error("No transcripts were fetched. Pipeline stopped.")
        return

    logging.info(f"Successfully ingested {len(raw_df)} transcripts. Moving to RoBERTa scoring...")

    # Score the Transcripts (400-Word Chunking Matrix)
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)

    output_dir = "./data/historical/"
    if (not os.path.exists(output_dir)):
        os.makedirs(output_dir)

    final_path = os.path.join(output_dir, output_scored_name)
    scored_df.to_csv(final_path, index=False)
    
    logging.info(f"Pipeline Complete! Scored data successfully saved to {final_path}")

if __name__ == "__main__":
    # Example execution sequence for your weekend run
    os.makedirs("./data/historical/", exist_ok=True)
    
    # Run the newly compiled manifests
    if (os.path.exists("./data/2021-2022_playoff_vids.json")):
        run_historical_pipeline(
            json_path="./data/2021-2022_playoff_vids.json",
            output_raw_name="raw_2021_2022.csv",
            output_scored_name="scored_2021_2022.csv"
        )