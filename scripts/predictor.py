import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class PlayoffPredictor:
    def __init__(self, model_dir="./models/"):
        self.model_dir = model_dir
        if not os.path.exists(self.model_dir):
            os.makedirs(self.model_dir)
            
        self.features = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        self.roles = ['coach', 'star', 'role_player', 'aggregate']

    def _flatten_team_data(self, df):
        """
        The core V2 architecture. 
        Takes a raw dataframe, groups by Team and Role, and flattens it into a 28-column matrix.
        Implements defensive imputation: if a role is missing, it falls back to the team aggregate.
        """
        flat_data = []
        
        for team in df['team'].unique():
            team_df = df[df['team'] == team]
            team_row = {'team': team, 'won_championship': team_df['won_championship'].iloc[0]}
            
            # Calculate the aggregate baseline for imputation
            agg_means = team_df[self.features].mean()
            
            for role in self.roles:
                role_df = team_df[team_df['role'] == role]
                
                if not role_df.empty:
                    role_means = role_df[self.features].mean()
                else:
                    # Defensive Engineering: Impute missing roles with the team average
                    logging.warning(f"{team} is missing '{role}' data. Imputing with aggregate mean.")
                    role_means = agg_means
                    
                for feature in self.features:
                    # Creates columns like: 'coach_confidence', 'star_frustration', etc.
                    col_name = f"{role}_{feature}"
                    team_row[col_name] = role_means[feature]
                    
            flat_data.append(team_row)
            
        return pd.DataFrame(flat_data)

    def train_model(self, csv_path):
        logging.info("V2 Engine: Loading and flattening historical data...")
        raw_df = pd.read_csv(csv_path)
        
        # Transform from 7 features to 28 features
        flat_df = self._flatten_team_data(raw_df)
        
        # Build the exact column list we expect
        X_cols = [f"{role}_{feature}" for role in self.roles for feature in self.features]
        
        X = flat_df[X_cols]
        y = flat_df['won_championship']
        
        logging.info("Training the V2 Random Forest (28 Features)...")
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X, y)
        
        save_path = os.path.join(self.model_dir, "playoff_rf_model_v2.pkl")
        joblib.dump(rf_model, save_path)
        
        logging.info(f"Successfully saved the V2 trained model to {save_path}!")
        
        # Output Feature Importances for the README
        importances = pd.Series(rf_model.feature_importances_, index=X_cols).sort_values(ascending=False)
        logging.info("\n=== Top 5 Championship Drivers (V2) ===")
        for col, val in importances.head(5).items():
            logging.info(f"{col}: {val:.4f}")

    def evaluate_model(self, csv_path):
        # We will build this out in the next phase
        pass

    def predict_matchup(self, team1, team2, live_csv_path, output_dir="./output/predictions/"):
        # We will build this out in the next phase
        pass

def run_tests():
    logging.info("Running V2 tests for the predictor...")
    
    test_data = []
    
    # We must provide the 'role' and 'team' tags now for the V2 test to pass
    row1 = {'team': 'TestTeamA', 'role': 'star', 'confidence': 0.9, 'content': 0.8, 'neutrality': 0.1, 'frustration': 0.0, 'upset': 0.0, 'anxiety': 0.1, 'surprise': 0.0, 'won_championship': 1}
    row2 = {'team': 'TestTeamA', 'role': 'coach', 'confidence': 0.8, 'content': 0.7, 'neutrality': 0.2, 'frustration': 0.0, 'upset': 0.0, 'anxiety': 0.1, 'surprise': 0.0, 'won_championship': 1}
    row3 = {'team': 'TestTeamB', 'role': 'aggregate', 'confidence': 0.2, 'content': 0.1, 'neutrality': 0.1, 'frustration': 0.8, 'upset': 0.9, 'anxiety': 0.7, 'surprise': 0.1, 'won_championship': 0}
    
    test_data.extend([row1, row2, row3])
    df = pd.DataFrame(test_data)
    
    if not os.path.exists("./models/"):
        os.makedirs("./models/")
        
    df.to_csv("./models/test_scored_data_v2.csv", index=False)
    
    predictor = PlayoffPredictor(model_dir="./models/")
    predictor.train_model("./models/test_scored_data_v2.csv")
    logging.info("V2 Model test passed and weights saved!")

if __name__ == "__main__":
    #run_tests()
    pass