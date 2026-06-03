import pandas as pd
import os
import logging
from scripts.visualization import EmotionVisualizer

MODERN_FILES = [
    {
        "filepath": "data/historical/scored_2023_2024.csv",
        "season_label": "2023-2024",
        "champ": "Celtics",
        "runner_up": "Mavericks"
    },
    {
        "filepath": "data/historical/scored_2024_2025.csv",
        "season_label": "2024-2025",
        "champ": "Thunder",
        "runner_up": "Pacers"
    }
]

# Custom file prefixes for named Finals comparison charts
FINALS_PREFIXES = {
    "2023-2024": "CeltMavs",
    "2024-2025": "ThunPac"
}

if (__name__ == "__main__"):
    visualizer = EmotionVisualizer(primary_output_dir="./output", streamlit_asset_dir="./streamlit_app/assets")
    
    for era in MODERN_FILES:
        if (os.path.exists(era["filepath"]) == True):
            df = pd.read_csv(era["filepath"])
            
            # Plotting unbroken timeline graphs utilizing master interpolation logic
            visualizer.plot_concise_trajectories(df, team_name=era["champ"], season_label=era["season_label"])
            visualizer.plot_concise_trajectories(df, team_name=era["runner_up"], season_label=era["season_label"])
            
            # Generating comparative side-by-side post-season average arrays with named prefix
            prefix = FINALS_PREFIXES.get(era["season_label"], "combined")
            visualizer.plot_finals_comparison_bar(
                df,
                champ_name=era["champ"],
                runner_name=era["runner_up"],
                season_label=era["season_label"],
                file_prefix=prefix
            )
            
        else:
            logging.error(f"⚠️ Missing scored modern era asset vector target: {era['filepath']}")
            
    print("\n🎉 Modern Era multi-year baseline visual assets updated cleanly! All 24 graphics mapped out.")