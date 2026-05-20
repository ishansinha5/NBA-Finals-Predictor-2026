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
    historical_csv_path = "./data/historical/scored_historical.csv" # Ensure this path points to your historical data!
    
    # ==========================================
    # PHASES 1, 2 & 3: INGESTION, SCORING, VISUALS (MUTED)
    # ==========================================
    # (Kept muted for speed as requested)

    # ==========================================
    # PHASE 4: MATCHUP INFERENCE (ACTIVE)
    # ==========================================
    logging.info("--- Phase 4: Matchup Inference ---")
    predictor = PlayoffPredictor(model_dir="./models/")
    
    # 1. RETRAIN THE MODEL ON THE CORRECT HISTORICAL DATA TO FIX THE .PKL
    logging.info("Repairing the model by retraining on historical data...")
    predictor.train_model(historical_csv_path) 
    
    teams = ["Spurs", "Thunder", "Knicks", "Cavaliers"]
    matchups = list(itertools.combinations(teams, 2))
    
    for t1, t2 in matchups:
        predictor.predict_matchup(t1, t2, scored_csv_path)
    
    logging.info("Phase 4 Complete! All prediction text files generated.")

if __name__ == "__main__":
    main()