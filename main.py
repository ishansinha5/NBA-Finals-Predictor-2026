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
    
    # Pointing to the new JSON file
    manifest_path = "./data/2025-2026_playoff_vids.json"
    video_list = []
    
    try:
        with open(manifest_path, 'r') as json_file:
            video_list = json.load(json_file)
        logging.info("Successfully loaded the LIVE video manifest from the data folder!")
    except Exception as e:
        logging.error(f"Could not load the json file because of error: {e}")
        return
    
    logging.info("--- Phase 1: Data Ingestion (Live) ---")
    
    # Global Run: Pass the entire video_list. Checkpointing will ignore the 211 we already have
    ingestor = TranscriptIngestor(data_dir="./data/live_2026/")
    raw_df = ingestor.fetch_transcripts(video_list, save_filename="raw_live_2026.csv")
    
    if raw_df.empty:
        logging.error("We didn't get any data! Stopping the pipeline.")
        return
        
    logging.info("Data loaded. Proceeding to Phase 2 (Sentiment Analysis).")
    
    # --- Phase 2: Sentiment Analysis ---
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)
    
    scored_csv_path = "./data/live_2026/scored_live_2026.csv"
    scored_df.to_csv(scored_csv_path, index=False)
    logging.info("Phase 2 Complete! Scored data saved.")

    # --- Phase 3: Visualization Outputs ---
    logging.info("--- Phase 3: Generating Live Visualizations ---")
    live_scored_df = pd.read_csv(scored_csv_path)
    
    # Initialize your existing visualizer
    visualizer = EmotionVisualizer(output_dir="./output/live_2026/")
    
    # Generate individual team trajectories
    teams = ["Spurs", "Thunder", "Knicks", "Cavaliers"]
    for team in teams:
        # Pass the full df; plot_time_series filters it internally
        visualizer.plot_time_series(live_scored_df, team_name=team)
        
    # Generate head-to-head comparisons
    visualizer.plot_finals_comparison_bar(live_scored_df, "Spurs", "Thunder", "Spurs vs Thunder WCF")
    visualizer.plot_finals_comparison_bar(live_scored_df, "Knicks", "Cavaliers", "Knicks vs Cavaliers ECF")
    
    logging.info("Phase 3 Complete! Visualizations saved to /output/live_2026/")
    # --- Phase 4: Matchup Inference ---
    logging.info("--- Phase 4: Matchup Inference ---")
    predictor = PlayoffPredictor(model_dir="./models/")
    
    # Predict Conference Finals
    wcf_winner = predictor.predict_matchup("Spurs", "Thunder", scored_csv_path)
    ecf_winner = predictor.predict_matchup("Knicks", "Cavaliers", scored_csv_path)
    
    # Predict NBA Finals
    champion = predictor.predict_matchup(wcf_winner, ecf_winner, scored_csv_path)
    logging.info(f"The 2026 Predicted NBA Champion is: {champion}!")

if __name__ == "__main__":
    main()