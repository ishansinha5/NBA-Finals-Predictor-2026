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
            
        self._ensure_directories = _ensure_directories.__get__(self, EmotionVisualizer)

    def _get_opponent_meta(self, team, stage_str):
        round_prefix = stage_str[:2]
        
        # 2023-2024 Era
        celtics_opps = {
            "R1": {"coach": "E. Spoe.", "star": "B. Adeb.", "team": "MIA Heat"},
            "R2": {"coach": "J. Bice.", "star": "D. Mitc.", "team": "CLE Cavs"},
            "R3": {"coach": "R. Carl.", "star": "T. Hali.", "team": "IND Pacers"},
            "R4": {"coach": "J. Kidd.", "star": "L. Donc.", "team": "DAL Mavs"}
        }
        
        mavericks_opps = {
            "R1": {"coach": "T. Lue.",  "star": "P. Geor.", "team": "LA Clip."},
            "R2": {"coach": "M. Daig.", "star": "S. Gilg.", "team": "OKC Thun."},
            "R3": {"coach": "C. Finch", "star": "A. Edwa.", "team": "MIN Timb."},
            "R4": {"coach": "J. Mazz.", "star": "J. Tayt.", "team": "BOS Celt."}
        }
        
        # 2024-2025 Era (Thunder Paths & Pacers Paths)
        thunder_opps = {
            "R1": {"coach": "T. Jenk.", "star": "J. Mora.", "team": "MEM Griz."},
            "R2": {"coach": "M. Malo.", "star": "N. Joki.", "team": "DEN Nugg."},
            "R3": {"coach": "C. Finch", "star": "A. Edwa.", "team": "MIN Timb."},
            "R4": {"coach": "R. Carl.", "star": "T. Hali.", "team": "IND Pacers"}
        }
        
        pacers_opps = {
            "R1": {"coach": "D. Ham.",  "star": "G. Ante.", "team": "MIL Bucks"},
            "R2": {"coach": "J. Bice.", "star": "D. Mitc.", "team": "CLE Cavs"},
            "R3": {"coach": "T. Thib.", "star": "J. Brun.", "team": "NY Knicks"},
            "R4": {"coach": "M. Daig.", "star": "S. Gilg.", "team": "OKC Thun"}
        }
        
        # Historical Eras
        lakers_opps = {
            "R1": {"coach": "T. Stot.", "star": "D. Lill.", "team": "POR Trail."},
            "R2": {"coach": "M. DAnt.", "star": "J. Hard.", "team": "HOU Rock."},
            "R3": {"coach": "M. Malo.", "star": "N. Joki.", "team": "DEN Nugg."},
            "R4": {"coach": "E. Spoe.", "star": "J. Butl.", "team": "MIA Heat"}
        }
        
        bucks_opps = {
            "R1": {"coach": "E. Spoe.", "star": "J. Butl.", "team": "MIA Heat"},
            "R2": {"coach": "S. Nash",  "star": "K. Dura.", "team": "BKN Nets"},
            "R3": {"coach": "N. McMi.", "star": "T. Youn.", "team": "ATL Hawk."},
            "R4": {"coach": "M. Will.", "star": "D. Book.", "team": "PHX Suns"}
        }
        
        warriors_opps = {
            "R1": {"coach": "M. Malo.", "star": "N. Joki.", "team": "DEN Nugg."},
            "R2": {"coach": "T. Jenk.", "star": "J. Mora.", "team": "MEM Griz."},
            "R3": {"coach": "J. Kidd.", "star": "L. Donc.", "team": "DAL Mavs"},
            "R4": {"coach": "I. Udok.", "star": "J. Tayt.", "team": "BOS Celt."}
        }
        
        if (team == "Celtics"):
            return celtics_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Mavericks"):
            return mavericks_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Thunder"):
            return thunder_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Pacers"):
            return pacers_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Lakers"):
            return lakers_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Bucks"):
            return bucks_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Warriors"):
            return warriors_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
            
        return {"coach": "OPP", "star": "OPP", "team": "OPP"}

    def format_stage_label(self, stage_str, team, role):
        if (isinstance(stage_str, str) == False):
            return stage_str
            
        if ("R" not in stage_str):
            return stage_str
            
        meta = self._get_opponent_meta(team, stage_str)
        
        if (role == "coach"):
            return f"{stage_str} vs. {meta['coach']}"
            
        elif (role == "star"):
            return f"{stage_str} vs. {meta['star']}"
            
        else:
            return f"{stage_str} vs. {meta['team']}"

    def plot_concise_trajectories(self, df, team_name, season_label="2023-2024"):
        logging.info(f"Extracting specific visual segments for the {team_name}...")
        
        # This matches our target architecture paths safely
        out_dir, asset_dir = self._ensure_directories("historical")
        
        roles = ["aggregate", "coach", "star", "teammate"]
        emotions = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        colors = ['#2ca02c', '#1f77b4', '#7f7f7f', '#ff7f0e', '#d62728', '#9467bd', '#e377c2']
        
        sns.set_theme(style="darkgrid")
        team_data = df[df['team'] == team_name].copy()
        
        if (team_data.empty == True):
            logging.warning(f"No available dataframe indexes for {team_name}, skipping metrics track.")
            return

        sorted_timeline_df = team_data.sort_values(by=['stage'])
        master_stages = sorted_timeline_df['stage'].drop_duplicates().tolist()

        for role in roles:
            if (role == "aggregate"):
                working_df = team_data.copy()
            else:
                working_df = team_data[team_data['role'] == role].copy()
                
                if (working_df.empty == True):
                    continue
            
            working_df = working_df.sort_values(by=['stage'])
            
            raw_grouped = working_df.groupby('stage', sort=False)[emotions].mean()
            interp_df = raw_grouped.reindex(master_stages)
            interp_df = interp_df.interpolate(method='linear', limit_direction='both')
            
            final_labels = []
            for stage_idx in interp_df.index:
                formatted_label = self.format_stage_label(stage_idx, team_name, role)
                final_labels.append(formatted_label)
                
            interp_df.index = final_labels
            
            plt.figure(figsize=(12, 6))
            
            for emotion, color in zip(emotions, colors):
                if (emotion in interp_df.columns):
                    plt.plot(
                        interp_df.index, 
                        interp_df[emotion], 
                        label=emotion.capitalize(), 
                        marker='o', 
                        color=color, 
                        linewidth=2
                    )
            
            plt.title(f"{team_name} Trajectory ({role.capitalize()}) - {season_label}", fontsize=15, fontweight='bold')
            plt.ylabel("Sentiment Intensity (RoBERTa Vector)")
            plt.xticks(rotation=45, ha='right')
            plt.ylim(0, 1.0)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Emotions")
            plt.tight_layout()
            
            # Incorporating short year tag so 2023 and 2024 profiles never overwrite each other
            short_year = season_label[:4]
            filename = f"{team_name.lower()}_{short_year}_{role}_trajectory.png"
            
            # Explicitly routing out copies to both system pipelines
            plt.savefig(os.path.join(out_dir, filename), dpi=300, bbox_inches='tight')
            plt.savefig(os.path.join(asset_dir, filename), dpi=300, bbox_inches='tight')
            plt.close()

    def plot_finals_comparison_bar(self, df, champ_name, runner_name, season_label="2023-2024"):
        logging.info(f"Processing side-by-side historical baseline bar charts for {champ_name} vs {runner_name}...")
        
        out_dir, asset_dir = self._ensure_directories("historical")
        
        roles = ["aggregate", "coach", "star", "teammate"]
        emotions = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        sns.set_theme(style="darkgrid")
        x = np.arange(len(emotions))
        width = 0.35

        for role in roles:
            if (role == "aggregate"):
                c_slice = df[df['team'] == champ_name]
                r_slice = df[df['team'] == runner_name]
            else:
                c_slice = df[(df['team'] == champ_name) & (df['role'] == role)]
                r_slice = df[(df['team'] == runner_name) & (df['role'] == role)]
                
            if (c_slice.empty == True) or (r_slice.empty == True):
                continue
                
            c_means = c_slice[emotions].mean()
            r_means = r_slice[emotions].mean()
            
            plt.figure(figsize=(11, 6))
            
            plt.bar(x - width/2, c_means, width=width, label=f"{champ_name} (Champ)", color='forestgreen')
            plt.bar(x + width/2, r_means, width=width, label=f"{runner_name} (Runner-Up)", color='firebrick')
            
            plt.title(f"{season_label} Finals Matchup - {role.capitalize()} Average Profile", fontsize=14, fontweight='bold')
            plt.ylabel("Mean Emotional Response")
            
            capitalized_emotions = []
            for e in emotions:
                capital_e = e.capitalize()
                capitalized_emotions.append(capital_e)
                
            plt.xticks(x, capitalized_emotions)
            plt.ylim(0, 1.0)
            plt.legend()
            plt.tight_layout()
            
            filename = f"combined_{role}_comparison_bar.png"
            
            plt.savefig(os.path.join(out_dir, filename), dpi=300, bbox_inches='tight')
            plt.savefig(os.path.join(asset_dir, filename), dpi=300, bbox_inches='tight')
            plt.close()