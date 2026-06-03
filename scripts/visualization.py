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

    def plot_era_trajectories(self, df, team_name, season_label="Historical Era", opponent_name=None):
        logging.info(f"Generating isolated role visualizations for {team_name}...")
        
        sub_folder = "historical"
        if ("2025-2026" in season_label):
            sub_folder = "live_2026"
            
        out_dir, asset_dir = self._ensure_directories(sub_folder)
        roles = ["aggregate", "coach", "star", "teammate"]
        emotions = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']

        for role in roles:
            sns.set_style("darkgrid")
            plt.figure(figsize=(12, 6))
            
            if (role == "aggregate"):
                role_df = df[(df['team'] == team_name)].copy()
            else:
                role_df = df[(df['team'] == team_name) & (df['role'] == role)].copy()
                
            if (role_df.empty):
                plt.close()
                continue
                
            # Formatting stage tick marks to look like: "R1G1 v War."
            clean_ticks = []
            for _, row in role_df.iterrows():
                stage_val = row['stage']
                opp = opponent_name if (opponent_name is not None) else "Opp"
                if ('opp_team' in role_df.columns and pd.notna(row['opp_team'])):
                    opp = row['opp_team']
                trunc_opp = str(opp)[:3].capitalize()
                clean_ticks.append(f"{stage_val} v {trunc_opp}.")
                
            role_df['tick_label'] = clean_ticks
            grouped_df = role_df.groupby('tick_label')[emotions].mean().reindex(clean_ticks).dropna()
            
            for emotion, color in zip(emotions, colors):
                if (emotion in grouped_df.columns):
                    plt.plot(grouped_df.index, grouped_df[emotion], label=emotion.capitalize(), marker='o', color=color, linewidth=2)
            
            plt.title(f"{team_name} Profile Trajectory - Role: {role.capitalize()} ({season_label})")
            plt.ylabel("Mean Vector Magnitude")
            plt.xticks(rotation=45, ha='right')
            plt.legend(title="Features", bbox_to_anchor=(1.05, 1), loc='upper left')
            
            filename = f"{team_name.lower().replace(' ', '_')}_{role}_trajectory.png"
            plt.savefig(os.path.join(out_dir, filename), bbox_inches='tight')
            plt.savefig(os.path.join(asset_dir, filename), bbox_inches='tight')
            plt.close()
            
        return True