import pandas as pd
import os
import logging
from scripts.visualization import EmotionVisualizer

if (__name__ == "__main__"):
    scored_path = "data/live_2026/scored_2025_2026.csv"
    
    if (os.path.exists(scored_path) == False):
        logging.error(f"⚠️ Target metrics file missing at verified tree layout: {scored_path}")
    else:
        df = pd.read_csv(scored_path)
        visualizer = EmotionVisualizer(primary_output_dir="./output", streamlit_asset_dir="./streamlit_app/assets")
        
        playoff_df = df[~df['stage'].str.startswith("Reg Season")]
        reg_season_df = df[df['stage'].str.startswith("Reg Season")]
        
        teams = ["Spurs", "Knicks", "Cavaliers", "Thunder"]
        
        # 1. Map all 4 Playoff Trajectories
        logging.info("--- Mapping 2026 Playoff Trajectories ---")
        for team in teams:
            visualizer.plot_concise_trajectories(
                playoff_df, 
                team_name=team, 
                season_label="2025-2026", 
                output_folder="live_2026"
            )
            
        # 2. Map all 4 Regular Season metrics paths with true historical imputation
        logging.info("--- Mapping 2026 Regular Season Trajectories ---")
        for team in teams:
            visualizer.plot_concise_trajectories(
                reg_season_df, 
                team_name=team, 
                season_label="2025-2026_RegSeason", 
                output_folder="live_2026",
                reference_df=df
            )
            
        # 3. Generate a Pre-Matchup comparison bar chart
        logging.info("--- Generating Spurs vs. Knicks Pre-Matchup Analysis ---")
        visualizer.plot_finals_comparison_bar(
            playoff_df, 
            champ_name="Spurs", 
            runner_name="Knicks", 
            season_label="2025-2026", 
            output_folder="live_2026",
            custom_title="2025-2026 NBA Finals Pre-Matchup Analysis",
            file_prefix="combined_pre_matchup"
        )
        
        # 4. Generate WCF bracket bar charts
        logging.info("--- Generating Western Conference Finals Bracket Map (Spurs vs. Thunder) ---")
        visualizer.plot_finals_comparison_bar(
            playoff_df, 
            champ_name="Spurs", 
            runner_name="Thunder", 
            season_label="2025-2026", 
            output_folder="live_2026",
            custom_title="2025-2026 Western Conference Finals",
            file_prefix="wcf_matchup"
        )
        
        # 5. Generate ECF bracket bar charts
        logging.info("--- Generating Eastern Conference Finals Bracket Map (Knicks vs. Cavaliers) ---")
        visualizer.plot_finals_comparison_bar(
            playoff_df, 
            champ_name="Knicks", 
            runner_name="Cavaliers", 
            season_label="2025-2026", 
            output_folder="live_2026",
            custom_title="2025-2026 Eastern Conference Finals",
            file_prefix="ecf_matchup"
        )
        
        print("\n🎉 Live 2026 multi-tier visualization loop run complete! Check output and asset pipelines.")