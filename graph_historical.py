import pandas as pd
import os
from scripts.visualization import EmotionVisualizer  # Adjust import path if visualization.py is not in scripts/

# Hardcoded playoff paths for the historical baselines
OPPONENT_MAPPINGS = {
    "Lakers": {"Round 1": "POR", "Round 2": "HOU", "Conference Finals": "DEN", "Finals": "MIA"},
    "Bucks": {"Round 1": "MIA", "Round 2": "BKN", "Conference Finals": "ATL", "Finals": "PHX"},
    "Warriors": {"Round 1": "DEN", "Round 2": "MEM", "Conference Finals": "DAL", "Finals": "BOS"}
}

FILES = {
    "Lakers": ("data/historical/scored_2019_2020.csv", "2019-2020 Playoff Archive"),
    "Bucks": ("data/historical/scored_2020_2021.csv", "2020-2021 Playoff Archive"),
    "Warriors": ("data/historical/scored_2021_2022.csv", "2021-2022 Playoff Archive")
}

if __name__ == "__main__":
    visualizer = EmotionVisualizer(primary_output_dir="./output", streamlit_asset_dir="./streamlit_app/assets")
    
    for team, (filepath, season_label) in FILES.items():
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            mapping = OPPONENT_MAPPINGS.get(team, {})
            visualizer.plot_era_trajectories(df, team_name=team, season_label=season_label, opponent_mapping=mapping)
        else:
            print(f"⚠️ Missing data file for {team}: {filepath}")
            
    print("\n🎉 Graphing complete! Check your output/historical and streamlit_app/assets/historical folders.")