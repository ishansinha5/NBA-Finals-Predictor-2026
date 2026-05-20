import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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
        team_df = team_df[~team_df['stage'].str.contains("Reg Season", na=False)]
        
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
        plt.ylabel("Emotion Score (from RoBERTa)")
        
        # Tilting the x-axis labels so they don't overlap now that we have 20+ games!
        plt.xticks(rotation=45, ha='right')
        
        plt.legend(title="Emotions", bbox_to_anchor=(1.05, 1), loc='upper left')
        filename = f"{team_name}_sentiment_trajectory.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        
        logging.info(f"Saved the graph to {filepath}")
        return True

    # New function to compare the average emotions of two teams side-by-side
    def plot_finals_comparison_bar(self, df, team_winner, team_loser, matchup_name):
        logging.info(f"Making the comparison graph for {matchup_name}...")
        
        sns.set_style("darkgrid")
        plt.figure(figsize=(10, 6))

        t1_df = df[df['team'] == team_winner]
        t2_df = df[df['team'] == team_loser]
        
        if (t1_df.empty == True) or (t2_df.empty == True):
            logging.warning(f"Missing data for {team_winner} or {team_loser}, skipping comparison graph.")
            return False
            
        emotions = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        # Getting the average score for each emotion over the whole playoff run
        t1_means = t1_df[emotions].mean()
        t2_means = t2_df[emotions].mean()
        
        x = np.arange(len(emotions))
        width = 0.35
        
        # Plotting the winner in green and the loser in red to easily tell them apart
        plt.bar(x - width/2, t1_means, width=width, label=f"{team_winner}", color='forestgreen')
        plt.bar(x + width/2, t2_means, width=width, label=f"{team_loser}", color='firebrick')
        
        plt.title(f"{matchup_name} - Average Emotional Profile")
        plt.xlabel("Emotions")
        plt.ylabel("Average Emotion Score")
        plt.xticks(x, [e.capitalize() for e in emotions])
        plt.legend()
        
        filename = f"{team_winner}_vs_{team_loser}_comparison.png"
        filepath = os.path.join(self.output_dir, filename)
        plt.savefig(filepath, bbox_inches='tight')
        plt.close()
        
        logging.info(f"Saved the comparison graph to {filepath}")
        return True

def run_tests():
    pass

if (__name__ == "__main__"):
    #run_tests()
    pass