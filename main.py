import pandas as pd
import logging
import json
import os

from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine
from scripts.visualization import EmotionVisualizer
from scripts.predictor import PlayoffPredictor

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Starting the 2026 NBA Finals NLP Pipeline...")
    logging.info("PHASE 1: Generating Live 2026 Testing Data")
    
    # Pointing to the new JSON file we just created
    manifest_path = "./data/2025-2026_playoff_vids.json"
    video_list = []
    
    try:
        json_file = open(manifest_path, 'r')
        video_list = json.load(json_file)
        json_file.close()
        logging.info("Successfully loaded the LIVE video manifest from the data folder!")
    except Exception as e:
        logging.error(f"Could not load the json file because of error: {e}")
        return
    
    # Chunking strategy active for the live teams
    target_team = "Cavaliers"  # Change this to the team you want to focus on for the live chunk
    chunked_video_list = []
    
    for video in video_list:
        if (video['team'] == target_team):
            chunked_video_list.append(video)
            
    logging.info(f"Chunking strategy active: Only processing {len(chunked_video_list)} videos for the {target_team}.")
    
    logging.info("--- Phase 1: Data Ingestion (Live) ---")
    
    # Saving to a brand new folder and file so we don't overwrite the historical data!
    ingestor = TranscriptIngestor(data_dir="./data/live_2026/")
    raw_df = ingestor.fetch_transcripts(chunked_video_list, save_filename="raw_live_2026.csv")
    
    if (raw_df.empty == True):
        logging.error("We didn't get any data! Stopping the pipeline.")
        return
        
    logging.info("Successfully ingested chunk. The rest of the ML pipeline is paused.")
    
    # Phase 2, 3, and 4 are COMMENTED OUT for now
    # engine = SentimentEngine()
    # scored_df = engine.process_dataframe(raw_df)
    # scored_csv_path = os.path.join("./data/live_2026/", "scored_live_2026.csv")
    # scored_df.to_csv(scored_csv_path, index=False)
    # predictor = PlayoffPredictor(model_dir="./models/")
    # predictor.train_model(scored_csv_path)
    # predictor.evaluate_model(scored_csv_path)

if __name__ == "__main__":
    main()