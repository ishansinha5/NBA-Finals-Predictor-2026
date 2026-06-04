import pandas as pd
import os
import logging
from scripts.visualization import EmotionVisualizer

# Mapping out the historical eras so we can run the champions vs their respective runner-ups
FILES = [
    {
        "filepath": "data/historical/scored_2019_2020.csv",
        "season_label": "2019-2020",
        "champ": "Lakers",
        "runner_up": "Heat"
    },
    {
        "filepath": "data/historical/scored_2020_2021.csv",
        "season_label": "2020-2021",
        "champ": "Bucks",
        "runner_up": "Suns"
    },
    {
        "filepath": "data/historical/scored_2021_2022.csv",
        "season_label": "2021-2022",
        "champ": "Warriors",
        "runner_up": "Celtics"
    }
]

if (__name__ == "__main__"):
    visualizer = EmotionVisualizer(primary_output_dir="./output", streamlit_asset_dir="./streamlit_app/assets")
    
    for era in FILES:
        if (os.path.exists(era["filepath"]) == True):
            df = pd.read_csv(era["filepath"])
            
            # We are only plotting the trajectory lines for the Champions since we only hardcoded their specific opponent paths
            visualizer.plot_concise_trajectories(df, team_name=era["champ"], season_label=era["season_label"])
            
            # The bar charts just need raw math across the whole timeline, so we can pit the Champ against the Runner-Up flawlessly!
            visualizer.plot_finals_comparison_bar(df, champ_name=era["champ"], runner_name=era["runner_up"], season_label=era["season_label"])
            
        else:
            logging.error(f"⚠️ Missing scored vector artifact file: {era['filepath']}")
            
    print("\n🎉 Historical Era graphing pipeline complete! Check the assets folder.")