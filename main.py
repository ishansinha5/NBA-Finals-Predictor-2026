import pandas as pd
import logging

# Importing my custom tools from the scripts folder
from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine
from scripts.visualization import EmotionVisualizer

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Starting the 2026 NBA Finals NLP Pipeline...")
    
    # Step 1: Define the videos we want to analyze
    # I am using placeholders here until I go to youtube and grab the real URLs for the matchups
    video_list = []
    
    vid1 = {}
    vid1['video_id'] = 'PLACEHOLDER_SPURS_R1'
    vid1['team'] = 'Spurs'
    vid1['stage'] = 'Round 1'
    video_list.append(vid1)
    
    vid2 = {}
    vid2['video_id'] = 'PLACEHOLDER_THUNDER_R1'
    vid2['team'] = 'Thunder'
    vid2['stage'] = 'Round 1'
    video_list.append(vid2)

    # Step 2: Ingest the data
    logging.info("--- Phase 1: Data Ingestion ---")
    
    # Passing the exact path because main.py runs from the root folder
    ingestor = TranscriptIngestor(data_dir="./data/raw/")
    raw_df = ingestor.fetch_transcripts(video_list)
    
    if (raw_df.empty == True):
        logging.error("We didn't get any data! Stopping the pipeline.")
        return
    
    ingestor.save_to_csv(raw_df, "raw_playoff_data.csv")
    
    # Step 3: Run the Sentiment Engine
    logging.info("--- Phase 2: Sentiment Analysis ---")
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)
    
    # Saving the scored data so I don't have to re-run the heavy model every time
    ingestor.save_to_csv(scored_df, "scored_playoff_data.csv")
    
    # Step 4: Visualize the results
    logging.info("--- Phase 3: Visualization ---")
    visualizer = EmotionVisualizer(output_dir="./output/")
    
    # I need to graph each team separately, tracking the main contenders
    teams_to_graph = []
    teams_to_graph.append('Spurs')
    teams_to_graph.append('Thunder')
    teams_to_graph.append('Knicks')
    teams_to_graph.append('Cavs')
    teams_to_graph.append('Pistons')
    
    for team in teams_to_graph:
        visualizer.plot_time_series(scored_df, team)
        
    logging.info("Pipeline finished successfully! Check the output folder for the graphs.")

if (__name__ == "__main__"):
    main()