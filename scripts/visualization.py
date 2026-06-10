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
            out_path = os.path.abspath(os.path.join(self.primary_output_dir, sub_folder))
            asset_path = os.path.abspath(os.path.join(self.streamlit_asset_dir, sub_folder))
            
            os.makedirs(out_path, exist_ok=True)
            os.makedirs(asset_path, exist_ok=True)
            
            return out_path, asset_path
            
        self._ensure_directories = _ensure_directories.__get__(self, EmotionVisualizer)

    def _get_opponent_meta(self, team, stage_str, season_label=""):
        round_prefix = stage_str[:2]
        
        if ("2025-2026" in season_label):
            spurs_opps = {"R1": "POR", "R2": "MIN", "R3": "OKC"}
            knicks_opps = {"R1": "ATL", "R2": "PHI", "R3": "CLE"}
            thunder_opps = {"R1": "PHX", "R2": "LAL", "R3": "SAS"}
            cavs_opps = {"R1": "TOR", "R2": "DET", "R3": "NYK"}
            
            if (team == "Spurs"):
                return {"coach": "M. Daig.", "star": "S. Gilg.", "team": spurs_opps.get(round_prefix, "OPP")}
            elif (team == "Knicks"):
                return {"coach": "J. Bice.", "star": "D. Mitc.", "team": knicks_opps.get(round_prefix, "OPP")}
            elif (team == "Thunder"):
                return {"coach": "M. John.", "star": "V. Wemb.", "team": thunder_opps.get(round_prefix, "OPP")}
            elif (team == "Cavaliers"):
                return {"coach": "T. Thib.", "star": "J. Brun.", "team": cavs_opps.get(round_prefix, "OPP")}

        lakers_opps = {"R1": {"coach": "T. Stot.", "star": "D. Lill.", "team": "POR Trail."}, "R2": {"coach": "M. DAnt.", "star": "J. Hard.", "team": "HOU Rock."}, "R3": {"coach": "M. Malo.", "star": "N. Joki.", "team": "DEN Nugg."}, "R4": {"coach": "E. Spoe.", "star": "J. Butl.", "team": "MIA Heat"}}
        bucks_opps = {"R1": {"coach": "E. Spoe.", "star": "J. Butl.", "team": "MIA Heat"}, "R2": {"coach": "S. Nash", "star": "K. Dura.", "team": "BKN Nets"}, "R3": {"coach": "N. McMi.", "star": "T. Youn.", "team": "ATL Hawk."}, "R4": {"coach": "M. Will.", "star": "D. Book.", "team": "PHX Suns"}}
        warriors_opps = {"R1": {"coach": "M. Malo.", "star": "N. Joki.", "team": "DEN Nugg."}, "R2": {"coach": "T. Jenk.", "star": "J. Mora.", "team": "MEM Griz."}, "R3": {"coach": "J. Kidd.", "star": "L. Donc.", "team": "DAL Mavs"}, "R4": {"coach": "I. Udok.", "star": "J. Tayt.", "team": "BOS Celt."}}
        celtics_opps = {"R1": {"coach": "E. Spoe.", "star": "B. Adeb.", "team": "MIA Heat"}, "R2": {"coach": "J. Bice.", "star": "D. Mitc.", "team": "CLE Cavs"}, "R3": {"coach": "R. Carl.", "star": "T. Hali.", "team": "IND Pacers"}, "R4": {"coach": "J. Kidd.", "star": "L. Donc.", "team": "DAL Mavs"}}
        mavericks_opps = {"R1": {"coach": "T. Lue.", "star": "P. Geor.", "team": "LA Clip."}, "R2": {"coach": "M. Daig.", "star": "S. Gilg.", "team": "OKC Thun."}, "R3": {"coach": "C. Finch", "star": "A. Edwa.", "team": "MIN Timb."}, "R4": {"coach": "J. Mazz.", "star": "J. Tayt.", "team": "BOS Celt."}}
        
        if (team == "Celtics"): return celtics_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Mavericks"): return mavericks_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Lakers"): return lakers_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Bucks"): return bucks_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        elif (team == "Warriors"): return warriors_opps.get(round_prefix, {"coach": "OPP", "star": "OPP", "team": "OPP"})
        return {"coach": "OPP", "star": "OPP", "team": "OPP"}

    def format_stage_label(self, stage_str, team, role, season_label=""):
        if (isinstance(stage_str, str) == False):
            return stage_str
            
        if (stage_str.startswith("Reg Season") == True):
            opp = stage_str.split("-")[1].strip()
            return f"Reg Season vs. {opp}"
            
        if ("R" not in stage_str):
            return stage_str
            
        meta = self._get_opponent_meta(team, stage_str, season_label)
        
        if (role == "coach"):
            return f"{stage_str} vs. {meta['coach']}"
        elif (role == "star"):
            return f"{stage_str} vs. {meta['star']}"
        else:
            return f"{stage_str} vs. {meta['team']}"

    def plot_concise_trajectories(self, df, team_name, season_label="2023-2024", output_folder="historical"):
        logging.info(f"Extracting visual indexes for {team_name} mapping down to {output_folder}...")
        out_dir, asset_dir = self._ensure_directories(output_folder)
        
        roles = ["aggregate", "coach", "star", "teammate"]
        emotions = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        colors = ['#2ca02c', '#1f77b4', '#7f7f7f', '#ff7f0e', '#d62728', '#9467bd', '#e377c2']
        
        sns.set_theme(style="darkgrid")
        team_data = df[df['team'] == team_name].copy()
        
        if (team_data.empty == True):
            logging.warning(f"Empty indices for {team_name}, skipping execution.")
            return

        sorted_timeline_df = team_data.sort_values(by=['stage'])
        master_stages = sorted_timeline_df['stage'].drop_duplicates().tolist()

        # DYNAMIC RE-ENGINEERING: Bulletproof aggregate synthesis for mixed datasets
        non_agg_df = team_data[team_data['role'] != 'aggregate']
        explicit_agg_df = team_data[team_data['role'] == 'aggregate']
        
        computed_agg = non_agg_df.groupby('stage', sort=False)[emotions].mean() if not non_agg_df.empty else pd.DataFrame()
        explicit_agg = explicit_agg_df.groupby('stage', sort=False)[emotions].mean() if not explicit_agg_df.empty else pd.DataFrame()
        
        # Combine computed means and explicit legacy data seamlessly
        if not computed_agg.empty and not explicit_agg.empty:
            agg_grouped = computed_agg.combine_first(explicit_agg).reindex(master_stages)
        elif not computed_agg.empty:
            agg_grouped = computed_agg.reindex(master_stages)
        elif not explicit_agg.empty:
            agg_grouped = explicit_agg.reindex(master_stages)
        else:
            agg_grouped = pd.DataFrame(columns=emotions, index=master_stages)

        for role in roles:
            if role == "aggregate":
                interp_df = agg_grouped.copy()
            else:
                working_df = team_data[team_data['role'] == role].copy().sort_values(by=['stage'])
                raw_grouped = working_df.groupby('stage', sort=False)[emotions].mean()
                interp_df = raw_grouped.reindex(master_stages)
                
                # Fallback imputation to protect against sparse data slots
                for stage in master_stages:
                    if pd.isna(interp_df.loc[stage]).all() and stage in agg_grouped.index:
                        interp_df.loc[stage] = agg_grouped.loc[stage]
            
            interp_df = interp_df.interpolate(method='linear', limit_direction='both')
            
            final_labels = []
            for stage_idx in interp_df.index:
                formatted_label = self.format_stage_label(stage_idx, team_name, role, season_label)
                final_labels.append(formatted_label)
            interp_df.index = final_labels
            
            plt.figure(figsize=(12, 6))
            for emotion, color in zip(emotions, colors):
                if (emotion in interp_df.columns):
                    plt.plot(interp_df.index, interp_df[emotion], label=emotion.capitalize(), marker='o', color=color, linewidth=2)
            
            title_modifier = " (Reg Season)" if "RegSeason" in season_label else ""
            clean_season = season_label.replace("_RegSeason", "")
            
            role_display = role.capitalize()
            if (role == "teammate"):
                role_display = "Teammates"
            elif (role == "coach"):
                if (team_name == "Spurs"): role_display = "Coach (Mitch Johnson)"
                elif (team_name == "Knicks"): role_display = "Coach (Tom Thibodeau)"
                elif (team_name == "Thunder"): role_display = "Coach (Mark Daigneault)"
                elif (team_name == "Cavaliers"): role_display = "Coach (Kenny Atkinson)"
                elif (team_name == "Celtics"): role_display = "Coach (Joe Mazzulla)"
                elif (team_name == "Mavericks"): role_display = "Coach (Jason Kidd)"
                elif (team_name == "Lakers"): role_display = "Coach (Frank Vogel)"
                elif (team_name == "Heat"): role_display = "Coach (Erik Spoelstra)"
                elif (team_name == "Bucks"): role_display = "Coach (Mike Budenholzer)"
                elif (team_name == "Suns"): role_display = "Coach (Monty Williams)"
                elif (team_name == "Warriors"): role_display = "Coach (Steve Kerr)"
            elif (role == "star"):
                if (team_name == "Spurs"): role_display = "Star (Victor Wembanyama)"
                elif (team_name == "Knicks"): role_display = "Star (Jalen Brunson)"
                elif (team_name == "Thunder"): role_display = "Star (Shai Gilgeous-Alexander)"
                elif (team_name == "Cavaliers"): role_display = "Star (Donovan Mitchell)"
                elif (team_name == "Celtics"): role_display = "Star (Jayson Tatum)"
                elif (team_name == "Mavericks"): role_display = "Star (Luka Doncic)"
                elif (team_name == "Lakers"): role_display = "Star (LeBron James)"
                elif (team_name == "Heat"): role_display = "Star (Jimmy Butler)"
                elif (team_name == "Bucks"): role_display = "Star (Giannis Antetokounmpo)"
                elif (team_name == "Suns"): role_display = "Star (Devin Booker)"
                elif (team_name == "Warriors"): role_display = "Star (Stephen Curry)"
            
            plt.title(f"{team_name} Trajectory ({role_display}){title_modifier} - {clean_season}", fontsize=15, fontweight='bold')
            plt.ylabel("Sentiment Intensity")
            plt.xticks(rotation=45, ha='right')
            plt.ylim(0, 1.0)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Emotions")
            plt.tight_layout()
            
            short_year = clean_season[:4]
            reg_tag = "_reg" if "RegSeason" in season_label else ""
            filename = f"{team_name.lower()}_{short_year}{reg_tag}_{role}_trajectory.png"
            
            plt.savefig(os.path.join(out_dir, filename), dpi=300, bbox_inches='tight')
            plt.savefig(os.path.join(asset_dir, filename), dpi=300, bbox_inches='tight')
            plt.close()

    def plot_finals_comparison_bar(self, df, champ_name, runner_name, season_label="2023-2024", output_folder="historical", custom_title=None, file_prefix="combined"):
        logging.info(f"Processing bar charts for {champ_name} vs {runner_name}...")
        out_dir, asset_dir = self._ensure_directories(output_folder)
        
        roles = ["aggregate", "coach", "star", "teammate"]
        emotions = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        sns.set_theme(style="darkgrid")
        x = np.arange(len(emotions))
        width = 0.35

        for role in roles:
            if (role == 'aggregate'):
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
            plt.bar(x - width/2, c_means, width=width, label=f"{champ_name}", color='forestgreen')
            plt.bar(x + width/2, r_means, width=width, label=f"{runner_name}", color='firebrick')
            
            role_display = "Teammates" if role == "teammate" else role.capitalize()
            if (custom_title != None):
                plt.title(f"{custom_title} - {role_display} Average Profile", fontsize=14, fontweight='bold')
            else:
                plt.title(f"{season_label} Finals Matchup - {role_display} Average Profile", fontsize=14, fontweight='bold')
                
            plt.ylabel("Mean Emotional Response")
            plt.xticks(x, [e.capitalize() for e in emotions])
            plt.ylim(0, 1.0)
            plt.legend()
            plt.tight_layout()
            
            short_year = season_label[:4]
            filename = f"{file_prefix}_{short_year}_{role}_comparison_bar.png"
            
            plt.savefig(os.path.join(out_dir, filename), dpi=300, bbox_inches='tight')
            plt.savefig(os.path.join(asset_dir, filename), dpi=300, bbox_inches='tight')
            plt.close()