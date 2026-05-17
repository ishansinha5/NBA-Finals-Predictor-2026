import pandas as pd
import logging
import os

# importing my custom tools from the scripts folder
from scripts.sentiment_engine import SentimentEngine
from scripts.visualization import EmotionVisualizer
from scripts.predictor import PlayoffPredictor

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Starting the 2026 NBA Finals NLP Pipeline...")
    logging.info("PHASE 2: Generating Historical Training Data")
    
    # We already have the raw data safely downloaded, so we can just load the CSV directly
    raw_csv_path = "./data/historical/raw_historical.csv"
    
    if not os.path.exists(raw_csv_path):
        logging.error("Could not find raw_historical.csv! Make sure it's in the right folder.")
        return
        
    raw_df = pd.read_csv(raw_csv_path)
    logging.info(f"Successfully loaded {len(raw_df)} historical press conferences!")
    
    # Step 2: Run the Sentiment Engine
    logging.info("--- Phase 2: Sentiment Analysis (Historical) ---")
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)
    
    # Saving the scored data
    scored_csv_path = os.path.join("./data/historical/", "scored_historical.csv")
    scored_df.to_csv(scored_csv_path, index=False)
    logging.info(f"Saved the scored dataframe to {scored_csv_path}")
    
    # Step 3: Train the AI
    logging.info("--- Phase 3: Model Training & Evaluation ---")
    
    predictor = PlayoffPredictor(model_dir="./models/")
    predictor.train_model(scored_csv_path)
    
    # Running the evaluation function to see how it did on the past 2 years
    predictor.evaluate_model(scored_csv_path)
    
    # Step 4: Visualize the Data
    logging.info("--- Phase 4: Generating Graphs ---")
    visualizer = EmotionVisualizer(output_dir="./output/")
    
    # reading the scored data so I can pass it to the visualizer
    scored_df = pd.read_csv(scored_csv_path)
    
    # generating individual trajectory graphs for all 4 teams
    visualizer.plot_time_series(scored_df, "Celtics")
    visualizer.plot_time_series(scored_df, "Thunder")
    visualizer.plot_time_series(scored_df, "Mavericks")
    visualizer.plot_time_series(scored_df, "Pacers")
    
    # generating the comparison bar charts for the Finals matchups
    visualizer.plot_finals_comparison_bar(scored_df, "Celtics", "Mavericks", "2024 NBA Finals")
    visualizer.plot_finals_comparison_bar(scored_df, "Thunder", "Pacers", "2025 NBA Finals")
    
    logging.info("Historical data pipeline finished successfully! We are ready for live 2026 predictions.")

if __name__ == "__main__":
    main()