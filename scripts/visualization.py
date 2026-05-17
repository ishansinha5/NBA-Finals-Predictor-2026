import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Class to handle turning our raw sentiment numbers into pretty graphs for my portfolio
class EmotionVisualizer:
    def __init__(self, output_dir="../output/"):
        self.output_dir = output_dir
        
        if (not os.path.exists(self.output_dir)):
            os.makedirs(self.output_dir)
            
    # Function to create a line chart showing how emotions change over the series
    def plot_time_series(self, df, team_name):
        logging.info(f"Making the graph for the {team_name}...")
        
        # I want the graph to look clean, so I am using seaborn's darkgrid style
        sns.set_style("darkgrid")
        plt.figure(figsize=(12, 8))
        team_df = df[df['team'] == team_name]
        
        # Error handling for if we don't have data for the team
        if (team_df.empty == True):
            logging.warning(f"No data found for {team_name}, skipping this graph.")
            return False
        stages = team_df['stage']
        
        # Plotting each of our 7 emotions as a separate line
        plt.plot(stages, team_df['confidence'], label='Confidence', marker='o')
        plt.plot(stages, team_df['content'], label='Contentment', marker='o')
        plt.plot(stages, team_df['neutrality'], label='Neutral', marker='o')
        plt.plot(stages, team_df['frustration'], label='Frustration', marker='o')
        plt.plot(stages, team_df['upset'], label='Upset', marker='o')
        plt.plot(stages, team_df['anxiety'], label='Anxiety', marker='o')
        plt.plot(stages, team_df['surprise'], label='Surprise', marker='o')
        plt.title(f"Emotional Trajectory of the {team_name} (2026 Playoffs)")
        plt.xlabel("Playoff Stage")
        plt.ylabel("Emotion Score (from RoBERTa)")
        plt.legend(title="Emotions", bbox_to_anchor=(1.05, 1), loc='upper left')
        filename = f"{team_name}_sentiment_trajectory.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath)
        plt.close()
        
        logging.info(f"Saved the graph to {filepath}")
        return True

def run_tests():
    # Making some test data just to see if the graph draws correctly without needing the AI model
    test_data = []
    
    row1 = {}
    row1['team'] = 'Spurs'
    row1['stage'] = 'Round 1'
    row1['confidence'] = 0.8
    row1['content'] = 0.5
    row1['neutrality'] = 0.2
    row1['frustration'] = 0.1
    row1['upset'] = 0.0
    row1['anxiety'] = 0.3
    row1['surprise'] = 0.1
    test_data.append(row1)

    row2 = {}
    row2['team'] = 'Spurs'
    row2['stage'] = 'Round 2'
    row2['confidence'] = 0.9
    row2['content'] = 0.6
    row2['neutrality'] = 0.1
    row2['frustration'] = 0.0
    row2['upset'] = 0.0
    row2['anxiety'] = 0.1
    row2['surprise'] = 0.2
    test_data.append(row2)

    df = pd.DataFrame(test_data)
    
    # testing it locally
    viz = EmotionVisualizer(output_dir="./")
    viz.plot_time_series(df, 'Spurs')

if (__name__ == "__main__"):
    # run_tests()
    pass