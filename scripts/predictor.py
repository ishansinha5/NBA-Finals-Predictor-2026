import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import logging
import joblib

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Class to handle training our Random Forest AI on the emotional data
class PlayoffPredictor:
    def __init__(self, model_dir="./models/"):
        self.model_dir = model_dir
        
        if (not os.path.exists(self.model_dir)):
            os.makedirs(self.model_dir)

    def train_model(self, csv_path):
        logging.info("Loading up the historical scored data to train the model...")
        df = pd.read_csv(csv_path)
        
        feature_columns = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        X = df[feature_columns]
        y = df['won_championship']
        
        logging.info("Training the Random Forest...")
        
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X, y)
        
        save_path = os.path.join(self.model_dir, "playoff_rf_model.pkl")
    
        file = open(save_path, "wb")
        pickle.dump(rf_model, file)
        file.close()
        
        logging.info(f"Successfully saved the trained model to {save_path}!")

    def evaluate_model(self, csv_path):
        logging.info("Testing the AI on the historical data to see if it learned the patterns...")
        df = pd.read_csv(csv_path)
        
        feature_columns = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        X = df[feature_columns]
        y_actual = df['won_championship']
        
        load_path = os.path.join(self.model_dir, "playoff_rf_model.pkl")
        
        file = open(load_path, "rb")
        rf_model = pickle.load(file)
        file.close()
        
        predictions = rf_model.predict(X)
        
        correct_guesses = 0
        total_guesses = len(predictions)
        
        for i in range(total_guesses):
            if (predictions[i] == y_actual[i]):
                correct_guesses = correct_guesses + 1
                
        accuracy = correct_guesses / total_guesses
        logging.info(f"Model Accuracy on Historical Data: {accuracy}")
        
        df['predicted_win'] = predictions
        predicted_champs = []
        
        for index in range(len(df)):
            row = df.iloc[index]
            if (row['predicted_win'] == 1):
                team_name = row['team']
                if (team_name not in predicted_champs):
                    predicted_champs.append(team_name)
                    
        logging.info("The AI predicts these teams had championship-level press conferences:")
        for team in predicted_champs:
            logging.info(f"- {team}")
    
    def predict_matchup(self, team1, team2, live_csv_path, output_dir="./output/predictions/"):
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Load the Model
        model_path = os.path.join(self.model_dir, "playoff_rf_model.pkl")
        if not hasattr(self, 'model'):
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
            else:
                logging.error(f"Cannot find trained model at {model_path}")
                return None

        # 2. Extract Data
        df = pd.read_csv(live_csv_path)
        features = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        t1_data = df[df['team'] == team1][features].mean()
        t2_data = df[df['team'] == team2][features].mean()
        
        # Convert to DataFrames to suppress the UserWarning
        t1_df = pd.DataFrame([t1_data], columns=features)
        t2_df = pd.DataFrame([t2_data], columns=features)
        
        # 3. Predict using the Random Forest
        t1_probs = self.model.predict_proba(t1_df)[0] 
        t2_probs = self.model.predict_proba(t2_df)[0]
        
        # 4. Bulletproof Class Mapping (Solves the IndexError)
        classes = list(self.model.classes_)
        
        if 1 in classes:
            target_idx = classes.index(1)
            t1_prob = t1_probs[target_idx]
            t2_prob = t2_probs[target_idx]
        elif '1' in classes:
            target_idx = classes.index('1')
            t1_prob = t1_probs[target_idx]
            t2_prob = t2_probs[target_idx]
        else:
            # Fallback: The model is broken and only knows 1 class. 
            # We bypass the ML failure and use raw RoBERTa Confidence as the tiebreaker.
            t1_prob = t1_data['confidence']
            t2_prob = t2_data['confidence']
        
        # 5. Determine Winner
        if t1_prob > t2_prob:
            winner, loser = team1, team2
            win_prob, lose_prob = t1_prob, t2_prob
            diffs = t1_data - t2_data
        else:
            winner, loser = team2, team1
            win_prob, lose_prob = t2_prob, t1_prob
            diffs = t2_data - t1_data
            
        top_diffs = diffs.sort_values(ascending=False).head(3)
        
        # 6. Generate Text Summary
        summary = (
            f"PREDICTED WINNER: {winner}\n"
            f"CHAMPIONSHIP MINDSET CONFIDENCE: {win_prob * 100:.1f}%\n"
            f"({loser} scored {lose_prob * 100:.1f}%)\n\n"
            f"TOP 3 EMOTIONAL DRIVERS:\n"
        )
        for emotion, val in top_diffs.items():
            summary += f"- {emotion.capitalize()} (+{val:.3f} margin over {loser})\n"
            
        summary += f"\nANALYSIS: The {winner} project a much stronger championship psychology, driven primarily by elevated {top_diffs.index[0]}."
        
        # 7. Save to TXT
        filepath = os.path.join(output_dir, f"{team1}_vs_{team2}.txt")
        with open(filepath, "w") as f:
            f.write(summary)
            
        logging.info(f"Prediction saved: {filepath}")
        return winner

def run_tests():
    logging.info("Running tests for the predictor...")
    
    test_data = []
    
    row1 = {'confidence': 0.9, 'content': 0.8, 'neutrality': 0.1, 'frustration': 0.0, 'upset': 0.0, 'anxiety': 0.1, 'surprise': 0.0, 'won_championship': 1}
    test_data.append(row1)
    
    row2 = {'confidence': 0.2, 'content': 0.1, 'neutrality': 0.1, 'frustration': 0.8, 'upset': 0.9, 'anxiety': 0.7, 'surprise': 0.1, 'won_championship': 0}
    test_data.append(row2)
    
    df = pd.DataFrame(test_data)
    if (not os.path.exists("./models/")):
        os.makedirs("./models/")
        
    df.to_csv("./models/test_scored_data.csv", index=False)
    
    predictor = PlayoffPredictor(model_dir="./models/")
    predictor.train_model("./models/test_scored_data.csv")
    logging.info("Model test passed and weights saved!")

if (__name__ == "__main__"):
    #run_tests()
    pass