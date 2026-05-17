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
    logging.info("PHASE 2: Generating Historical Training Data")
    
    manifest_path = "./data/videos.json"
    video_list = []
    
    try:
        json_file = open(manifest_path, 'r')
        video_list = json.load(json_file)
        json_file.close()
        logging.info("Successfully loaded the video manifest from the data folder!")
    except Exception as e:
        logging.error(f"Could not load the json file because of error: {e}")
        return
    
    # Implementing the new chunking strategy so we don't overwhelm the network
    target_team = "Celtics" 
    chunked_video_list = []
    
    # looping through the massive database and only pulling out the team we want right now
    for video in video_list:
        if (video['team'] == target_team):
            chunked_video_list.append(video)
            
    logging.info(f"Chunking strategy active: Only processing {len(chunked_video_list)} videos for the {target_team}.")
    
    logging.info("--- Phase 1: Data Ingestion (Historical) ---")
    
    ingestor = TranscriptIngestor(data_dir="./data/historical/")
    raw_df = ingestor.fetch_transcripts(chunked_video_list)
    
    if (raw_df.empty == True):
        logging.error("We didn't get any data! Stopping the pipeline.")
        return
    
    # The rest of the pipeline is commented out temporarily while we focus solely on getting the data downloaded
    # ingestor.save_to_csv(raw_df, "raw_historical.csv")
    # engine = SentimentEngine()
    # scored_df = engine.process_dataframe(raw_df)
    # ingestor.save_to_csv(scored_df, "scored_historical.csv")
    # scored_csv_path = os.path.join("./data/historical/", "scored_historical.csv")
    # predictor = PlayoffPredictor(model_dir="./models/")
    # predictor.train_model(scored_csv_path)
    # predictor.evaluate_model(scored_csv_path)
    # visualizer = EmotionVisualizer(output_dir="./output/")
    # scored_df = pd.read_csv(scored_csv_path)
    # visualizer.plot_time_series(scored_df, "Celtics")
    # visualizer.plot_time_series(scored_df, "Thunder")

if (__name__ == "__main__"):
    main()