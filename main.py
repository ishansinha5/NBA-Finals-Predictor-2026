import pandas as pd
import logging
import json
import os
import itertools

from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine
from scripts.visualization import EmotionVisualizer
from scripts.predictor import PlayoffPredictor

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Starting the 2026 NBA Finals NLP Pipeline...")
    
    scored_csv_path = "./data/live_2026/scored_live_2026.csv"
    historical_csv_path = "./data/historical/scored_historical.csv"
    manifest_path = "./data/2025-2026_playoff_vids.json"
    
    # ==========================================
    # PHASE 1: DATA INGESTION
    # ==========================================
    logging.info("--- Phase 1: Data Ingestion (Live) ---")
    with open(manifest_path, 'r') as json_file:
        video_list = json.load(json_file)
        
    ingestor = TranscriptIngestor(data_dir="./data/live_2026/")
    raw_df = ingestor.fetch_transcripts(video_list, save_filename="raw_live_2026.csv")
    
    if raw_df.empty:
        logging.error("We didn't get any data! Stopping the pipeline.")
        return
        
    # ==========================================
    # PHASE 2: SENTIMENT ANALYSIS
    # ==========================================
    logging.info("--- Phase 2: Sentiment Analysis ---")
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)
    scored_df.to_csv(scored_csv_path, index=False)
    logging.info("Phase 2 Complete! Scored data saved.")
    
    # ==========================================
    # PHASE 3: VISUALIZATIONS
    # ==========================================
    logging.info("--- Phase 3: Generating Live Visualizations ---")
    live_scored_df = pd.read_csv(scored_csv_path)
    visualizer = EmotionVisualizer(output_dir="./output/live_2026/")
    teams = ["Spurs", "Thunder", "Knicks", "Cavaliers"]
    
    for team in teams:
        visualizer.plot_time_series(live_scored_df, team_name=team)
        
    matchups = list(itertools.combinations(teams, 2))
    for t1, t2 in matchups:
        visualizer.plot_finals_comparison_bar(live_scored_df, t1, t2, f"{t1} vs {t2}")

    logging.info("Phase 3 Complete! All visualization combinations saved.")

    # ==========================================
    # PHASE 4: MATCHUP INFERENCE
    # ==========================================
    logging.info("--- Phase 4: Matchup Inference ---")
    predictor = PlayoffPredictor(model_dir="./models/")
    
    logging.info("Repairing the model by retraining on historical data...")
    predictor.train_model(historical_csv_path) 
    
    for t1, t2 in matchups:
        predictor.predict_matchup(t1, t2, scored_csv_path)
    
    logging.info("Phase 4 Complete! All prediction text files generated.")

if __name__ == "__main__":
    main()