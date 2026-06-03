import pandas as pd
import os
import logging
from scripts.visualization import EmotionVisualizer

if (__name__ == "__main__"):
    scored_path = "data/historical/scored_2023_2024.csv"
    
    if (os.path.exists(scored_path) == False):
        logging.error(f"Target vector artifact not found at {scored_path}. Run main.py pipelines first.")
    else:
        df = pd.read_csv(scored_path)
        
        visualizer = EmotionVisualizer(primary_output_dir="./output", streamlit_asset_dir="./streamlit_app/assets")
        
        # Plotting isolated trajectory lines game-by-game for both configurations
        visualizer.plot_concise_trajectories(df, team_name="Celtics", season_label="2023-2024")
        visualizer.plot_concise_trajectories(df, team_name="Mavericks", season_label="2023-2024")
        
        # Computing aggregate statistical averages to output the final comparison bar charts
        visualizer.plot_finals_comparison_bar(df, champ_name="Celtics", runner_name="Mavericks", season_label="2023-2024")
        
        print("\n🎉 Modern Era Execution loop complete! All 12 isolated graphics generated cleanly.")