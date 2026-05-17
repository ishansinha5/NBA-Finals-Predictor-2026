import pandas as pd
import logging
import json
import os

# importing my custom tools from the scripts folder
from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine
from scripts.visualization import EmotionVisualizer
from scripts.predictor import PlayoffPredictor

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Starting the 2026 NBA Finals NLP Pipeline...")
    logging.info("PHASE 2: Generating Historical Training Data")
    
    # setting up the path to the database file so I can load it 
    # making sure this matches the actual file name we saved in the data folder
    manifest_path = "./data/videos.json"
    video_list = []
    
    try:
        # opening the json file to read the video data so it isn't hardcoded anymore
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
    
    # checking if the dataframe is empty so we don't break the sentiment engine
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
    logging.info("--- Phase 3: Model Training & Evaluation ---")
    
    # getting the exact path where I just saved the scored csv
    scored_csv_path = os.path.join("./data/historical/", "scored_historical.csv")
    
    predictor = PlayoffPredictor(model_dir="./models/")
    predictor.train_model(scored_csv_path)
    
    # running the new evaluation function to see how it did on the past 2 years
    predictor.evaluate_model(scored_csv_path)
    
    # Step 4: Visualize the Data
    logging.info("--- Phase 4: Generating Graphs ---")
    visualizer = EmotionVisualizer(output_dir="./output/")
    
    # reading the scored data so I can pass it to the visualizer
    scored_df = pd.read_csv(scored_csv_path)
    
    # generating a graph for the Celtics and Thunder to see their championship runs
    visualizer.plot_time_series(scored_df, "Celtics")
    visualizer.plot_time_series(scored_df, "Thunder")
        
    logging.info("Historical data pipeline finished successfully! We are ready for live 2026 predictions.")

if (__name__ == "__main__"):
    main()