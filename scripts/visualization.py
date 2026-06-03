import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class EmotionVisualizer:
    def __init__(self, primary_output_dir="./output", streamlit_asset_dir="./streamlit_app/assets"):
        self.primary_output_dir = primary_output_dir
        self.streamlit_asset_dir = streamlit_asset_dir
            
    def _ensure_directories(self, sub_folder):
        out_path = os.path.join(self.primary_output_dir, sub_folder)
        asset_path = os.path.join(self.streamlit_asset_dir, sub_folder)
        os.makedirs(out_path, exist_ok=True)
        os.makedirs(asset_path, exist_ok=True)
        return out_path, asset_path

    def format_stage_label(self, stage_str, opp_mapping):
        """Converts 'Round 1 Game 1' to 'R1G1 - vs. OPP'"""
        if not isinstance(stage_str, str):
            return stage_str
            
        series_key = None
        for key in opp_mapping.keys():
            if key in stage_str:
                series_key = key
                break
                
        opponent = opp_mapping.get(series_key, "OPP") if series_key else "OPP"
        
        formatted = stage_str.replace("Round ", "R").replace(" Game ", "G")
        formatted = formatted.replace("Conference Finals", "CF").replace("Finals", "FIN")
        
        return f"{formatted} - vs. {opponent}"

    def plot_era_trajectories(self, df, team_name, season_label="Historical Era", opponent_mapping=None):
        logging.info(f"Generating isolated role visualizations for {team_name}...")
        
        if opponent_mapping is None:
            opponent_mapping = {}

        sub_folder = "historical"
        if ("2025-2026" in season_label):
            sub_folder = "live_2026"
            
        out_dir, asset_dir = self._ensure_directories(sub_folder)
        roles = ["aggregate", "coach", "star", "teammate"]
        emotions = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        colors = ['#2ca02c', '#1f77b4', '#7f7f7f', '#ff7f0e', '#d62728', '#9467bd', '#e377c2']

        sns.set_theme(style="darkgrid")

        # 1. Apply formatting and extract the master chronological timeline
        df['tick_label'] = df['stage'].apply(lambda x: self.format_stage_label(x, opponent_mapping))
        master_timeline = df['tick_label'].drop_duplicates().tolist()

        for role in roles:
            # 2. Compute the True Aggregate mathematically, or filter by role
            if (role == "aggregate"):
                grouped_df = df.groupby('tick_label', sort=False)[emotions].mean()
            else:
                role_df = df[df['role'] == role].copy()
                if role_df.empty:
                    continue
                grouped_df = role_df.groupby('tick_label', sort=False)[emotions].mean()
            
            # 3. Reindex to master timeline and interpolate missing gaps
            grouped_df = grouped_df.reindex(master_timeline)
            grouped_df = grouped_df.interpolate(method='linear', limit_direction='both')
            
            # Initialize Plot
            plt.figure(figsize=(12, 6))
            
            for emotion, color in zip(emotions, colors):
                if emotion in grouped_df.columns:
                    plt.plot(grouped_df.index, grouped_df[emotion], label=emotion.capitalize(), marker='o', color=color, linewidth=2)
            
            plt.title(f"{team_name} Profile Trajectory ({role.capitalize()}) - {season_label}", fontsize=16, fontweight='bold')
            plt.ylabel("Sentiment Intensity (0.0 to 1.0)", fontsize=12)
            plt.xticks(rotation=45, ha='right')
            plt.ylim(0, 1.0)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            
            filename = f"{team_name.lower()}_{role}_trajectory.png"
            
            plt.savefig(os.path.join(out_dir, filename), dpi=300, bbox_inches='tight')
            plt.savefig(os.path.join(asset_dir, filename), dpi=300, bbox_inches='tight')
            plt.close()
            
        logging.info(f"✅ Generated {len(roles)} continuous PNG graphs for {team_name}.")