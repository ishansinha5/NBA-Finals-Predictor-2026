import pandas as pd
import logging
import json
import os

# Importing my custom tools from the scripts folder
from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine
from scripts.visualization import EmotionVisualizer
from scripts.predictor import PlayoffPredictor

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Starting the 2026 NBA Finals NLP Pipeline...")
    logging.info("PHASE 2: Generating Historical Training Data")
    
    # Setting up the path to the database file so I can load it
    manifest_path = "./data/video_manifest.json"
    video_list = []
    
    try:
        # Opening the json file to read the video data so it isn't hardcoded anymore
        json_file = open(manifest_path, 'r')
        video_list = json.load(json_file)
        json_file.close()
        logging.info("Successfully loaded the video manifest from the data folder!")
    except Exception as e:
        logging.error(f"Could not load the json file because of error: {e}")
        return
    
    # Step 1: Ingest the data
    logging.info("--- Phase 1: Data Ingestion (Historical) ---")
    
    ingestor = TranscriptIngestor(data_dir="./data/historical/")
    raw_df = ingestor.fetch_transcripts(video_list)
    
    # Checking if the dataframe is empty so we don't break the sentiment engine
    if (raw_df.empty == True):
        logging.error("We didn't get any data! Stopping the pipeline.")
        return
    
    ingestor.save_to_csv(raw_df, "raw_historical.csv")
    
    # Step 2: Run the Sentiment Engine
    logging.info("--- Phase 2: Sentiment Analysis (Historical) ---")
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)
    
    ingestor.save_to_csv(scored_df, "scored_historical.csv")
    
    # Step 3: Train the AI
    logging.info("--- Phase 3: Model Training ---")
    
    # Getting the exact path where I just saved the scored csv
    scored_csv_path = os.path.join("./data/historical/", "scored_historical.csv")
    
    predictor = PlayoffPredictor(model_dir="./models/")
    predictor.train_model(scored_csv_path)
        
    logging.info("Historical data pipeline finished successfully! We are ready for live 2026 predictions.")

if (__name__ == "__main__"):
    main()