import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os
import logging

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
        
        # Putting all of my 7 custom emotions into a list for the features
        feature_columns = []
        feature_columns.append('confidence')
        feature_columns.append('content')
        feature_columns.append('neutrality')
        feature_columns.append('frustration')
        feature_columns.append('upset')
        feature_columns.append('anxiety')
        feature_columns.append('surprise')
        
        X = df[feature_columns]
        y = df['won_championship']
        
        logging.info("Training the Random Forest...")
        
        # Building the AI with 100 trees and setting a random state so it is reproducible
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
        
        # putting all of my 7 custom emotions into a list for the features again
        feature_columns = []
        feature_columns.append('confidence')
        feature_columns.append('content')
        feature_columns.append('neutrality')
        feature_columns.append('frustration')
        feature_columns.append('upset')
        feature_columns.append('anxiety')
        feature_columns.append('surprise')
        
        X = df[feature_columns]
        y_actual = df['won_championship']
        
        load_path = os.path.join(self.model_dir, "playoff_rf_model.pkl")
        
        # opening the saved weights
        file = open(load_path, "rb")
        rf_model = pickle.load(file)
        file.close()
        
        predictions = rf_model.predict(X)
        
        # calculating how many it got right manually to see the math
        correct_guesses = 0
        total_guesses = len(predictions)
        
        for i in range(total_guesses):
            if (predictions[i] == y_actual[i]):
                correct_guesses = correct_guesses + 1
                
        accuracy = correct_guesses / total_guesses
        logging.info(f"Model Accuracy on Historical Data: {accuracy}")
        
        # finding out which teams the AI actually thought won
        df['predicted_win'] = predictions
        predicted_champs = []
        
        for index in range(len(df)):
            row = df.iloc[index]
            if (row['predicted_win'] == 1):
                team_name = row['team']
                # making sure I don't add the same team twice to my print list
                if (team_name not in predicted_champs):
                    predicted_champs.append(team_name)
                    
        logging.info("The AI predicts these teams had championship-level press conferences:")
        for team in predicted_champs:
            logging.info(f"- {team}")
    
    def predict_matchup(self, team1, team2, live_csv_path, output_dir="./output/predictions/"):
        import os
        import pandas as pd
        import joblib
        import logging
        
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. Foolproof Model Loading
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
        
        # 3. Predict using the Random Forest
        t1_prob = self.model.predict_proba([t1_data])[0][1] 
        t2_prob = self.model.predict_proba([t2_data])[0][1]
        
        # 4. Determine Winner
        if t1_prob > t2_prob:
            winner, loser = team1, team2
            win_prob, lose_prob = t1_prob, t2_prob
            diffs = t1_data - t2_data
        else:
            winner, loser = team2, team1
            win_prob, lose_prob = t2_prob, t1_prob
            diffs = t2_data - t1_data
            
        top_diffs = diffs.sort_values(ascending=False).head(3)
        
        # 5. Generate Text Summary
        summary = (
            f"PREDICTED WINNER: {winner}\n"
            f"CHAMPIONSHIP MINDSET CONFIDENCE: {win_prob * 100:.1f}%\n"
            f"({loser} scored {lose_prob * 100:.1f}%)\n\n"
            f"TOP 3 EMOTIONAL DRIVERS:\n"
        )
        for emotion, val in top_diffs.items():
            summary += f"- {emotion.capitalize()} (+{val:.3f} margin over {loser})\n"
            
        summary += f"\nANALYSIS: The {winner} project a much stronger championship psychology, driven primarily by elevated {top_diffs.index[0]}."
        
        # 6. Save to TXT
        filepath = os.path.join(output_dir, f"{team1}_vs_{team2}.txt")
        with open(filepath, "w") as f:
            f.write(summary)
            
        logging.info(f"Prediction saved: {filepath}")
        return winner

def run_tests():
    logging.info("Running tests for the predictor...")
    
    # Setting up dummy data to see if the model trains without crashing
    test_data = []
    
    row1 = {}
    row1['confidence'] = 0.9
    row1['content'] = 0.8
    row1['neutrality'] = 0.1
    row1['frustration'] = 0.0
    row1['upset'] = 0.0
    row1['anxiety'] = 0.1
    row1['surprise'] = 0.0
    row1['won_championship'] = 1
    test_data.append(row1)
    
    row2 = {}
    row2['confidence'] = 0.2
    row2['content'] = 0.1
    row2['neutrality'] = 0.1
    row2['frustration'] = 0.8
    row2['upset'] = 0.9
    row2['anxiety'] = 0.7
    row2['surprise'] = 0.1
    row2['won_championship'] = 0
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