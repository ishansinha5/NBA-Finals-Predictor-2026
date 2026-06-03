import json
import pandas as pd
import os
import logging

from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def run_live_2026_pipeline(json_path, output_raw_name, output_scored_name):
    """Processes live 2026 data arrays and routes outputs into live storage profiles."""
    with open(json_path, 'r') as f:
        video_metadata = json.load(f)

    # Expanded logic for filtering metadata
    filtered_metadata = []
    for video in video_metadata:
        if (video['team'] == 'Knicks'):
            filtered_metadata.append(video)
            
    video_metadata = filtered_metadata

    logging.info(f"Loaded {len(video_metadata)} active tracking profiles for the Knicks from {json_path}")

    if (len(video_metadata) == 0):
        logging.warning("No Knicks matching entries found in the target manifest file.")
        return

    # Initialize data director using live tracking paths
    ingestor = TranscriptIngestor(data_dir="./data/live_2026/")
    raw_df = ingestor.fetch_transcripts(video_metadata, save_filename=output_raw_name)

    if (raw_df.empty):
        logging.error("No live transcript streams were fetched. Execution loop halted.")
        return

    logging.info(f"Successfully compiled {len(raw_df)} scripts. Executing RoBERTa emotional extraction matrices...")

    # Vectorize text slices using local transformer architecture
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)

    output_dir = "./data/live_2026/"
    os.makedirs(output_dir, exist_ok=True)

    final_path = os.path.join(output_dir, output_scored_name)
    scored_df.to_csv(final_path, index=False)
    
    logging.info(f"Live processing track completed. Output pushed cleanly to: {final_path}")

if (__name__ == "__main__"):
    os.makedirs("./data/live_2026/", exist_ok=True)
    
    # Target the newly compiled 2025-2026 manifest file
    manifest_source = "./data/2025-2026_playoff_vids.json"
    
    if (os.path.exists(manifest_source)):
        logging.info("Initiating isolated 2026 pipeline execution targeting: Knicks.")
        run_live_2026_pipeline(
            json_path=manifest_source,
            output_raw_name="raw_2025_2026.csv",
            output_scored_name="scored_2025_2026.csv"
        )
    else:
        logging.error(f"Target manifest not found at {manifest_source}. Ensure file layout matches storage tracks.")