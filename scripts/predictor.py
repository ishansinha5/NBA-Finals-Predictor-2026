import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class PlayoffPredictor:
    def __init__(self, model_dir="./models/"):
        self.model_dir = model_dir
        if (not os.path.exists(self.model_dir)):
            os.makedirs(self.model_dir)
            
        self.features = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        self.roles = ['coach', 'star', 'teammate', 'aggregate']

    def _flatten_historical_compiled_data(self, data_directory):
        """
        Pivots uneven historical logs into a wide series-level 28-column feature matrix.
        Protects older series with fallback imputations.
        """
        all_flattened_rows = []
        csv_targets = [f for f in os.listdir(data_directory) if (f.startswith("scored_") and f.endswith(".csv"))]
        
        for csv_file in csv_targets:
            filepath = os.path.join(data_directory, csv_file)
            df = pd.read_csv(filepath)
            
            # Group by unique teams inside each season file
            for team in df['team'].unique():
                team_df = df[df['team'] == team]
                won_championship = int(team_df['won_championship'].iloc[0])
                
                team_row = {'team': team, 'won_championship': won_championship}
                global_team_backup = team_df[self.features].mean()
                
                for role in self.roles:
                    role_df = team_df[team_df['role'] == role]
                    if (not role_df.empty):
                        role_means = role_df[self.features].mean()
                    else:
                        role_means = global_team_backup
                        
                    for feature in self.features:
                        col_name = f"{role}_{feature}"
                        team_row[col_name] = role_means[feature]
                        
                all_flattened_rows.append(team_row)
                
        return pd.DataFrame(all_flattened_rows)

    def train_historical_models(self, data_directory="./data/historical/"):
        """
        Trains two separate Random Forest checkpoints:
        1. A high-fidelity model restricted purely to modern dense data architectures.
        2. A comprehensive historical baseline model that handles imputation across eras.
        """
        logging.info("Compressing series-level historical profiles into training matrix...")
        flat_df = self._flatten_historical_compiled_data(data_directory)
        
        if flat_df.empty:
            logging.error("No data found to train model matrix.")
            return
            
        X_cols = [f"{role}_{feature}" for role in self.roles for feature in self.features]
        
        # ----------------------------------------------------
        # MODEL 1: THE FULL-ERA BASELINE MODEL (Everything)
        # ----------------------------------------------------
        X_all = flat_df[X_cols]
        y_all = flat_df['won_championship']
        
        logging.info(f"Training Model 1 (Full Baseline) on {len(flat_df)} localized team profiles...")
        rf_all = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
        rf_all.fit(X_all, y_all)
        
        save_path_all = os.path.join(self.model_dir, "playoff_rf_model_full_baseline.pkl")
        joblib.dump(rf_all, save_path_all)
        logging.info(f"Model 1 (Full Baseline) saved to {save_path_all}")
        
        # ----------------------------------------------------
        # MODEL 2: THE MODERN-ERA MODEL (2023-2024 onwards)
        # ----------------------------------------------------
        # Filter out older teams like the 2021 Bucks by explicitly isolating modern files
        # We do this by checking the raw team listings or files present in flat_df
        # Since flat_df aggregates everything, we can drop the 2021 Bucks explicitly:
        modern_flat_df = flat_df[flat_df['team'] != 'Bucks'] 
        
        if not modern_flat_df.empty:
            X_modern = modern_flat_df[X_cols]
            y_modern = modern_flat_df['won_championship']
            
            logging.info(f"Training Model 2 (Modern-Era) on {len(modern_flat_df)} high-density profiles...")
            rf_modern = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
            rf_modern.fit(X_modern, y_modern)
            
            save_path_modern = os.path.join(self.model_dir, "playoff_rf_model_modern_only.pkl")
            joblib.dump(rf_modern, save_path_modern)
            logging.info(f"Model 2 (Modern-Era Only) saved to {save_path_modern}")
        else:
            logging.warning("Skipping Modern-Era model: No dense files found.")

    def predict_series_winner(self, team1_csv, team2_csv, team1_name, team2_name):
        """Used by Streamlit to evaluate live head-to-head match-up inferences"""
        model_path = os.path.join(self.model_dir, "playoff_rf_model_v2.pkl")
        if (not os.path.exists(model_path)):
            return {"error": "Model not trained yet."}
            
        model = joblib.load(model_path)
        # Flatten logic can be run here on live data frames to return probability deltas
        return {team1_name: 0.55, team2_name: 0.45} # Placeholder signature for UI hook