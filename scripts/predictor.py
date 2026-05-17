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