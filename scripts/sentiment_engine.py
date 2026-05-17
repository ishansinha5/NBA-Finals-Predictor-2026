import pandas as pd
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Class to run the huggingface model on our dataframe
class SentimentEngine:
    def __init__(self, model_name="SamLowe/roberta-base-go_emotions"):
        logging.info("Loading up the AI model, this takes a lot of memory...")
        self.classifier = pipeline("text-classification", model=model_name, top_k=None)
        
    # Scoring function that expands 28 go_emotions into our 7 portfolio categories
    def score_text(self, text):
        short_text = text[:512] 
        results = self.classifier(short_text) 
        emotions = results[0]
        
        confidence_score = 0.0
        content_score = 0.0
        neutral_score = 0.0
        frustrated_score = 0.0
        upset_score = 0.0
        anxiety_score = 0.0
        surprise_score = 0.0
        
        # Looping through all 28 scores from the AI
        for emotion in emotions:
            label = emotion['label']
            score = emotion['score']
            
            # Confidence
            if (label == 'optimism'):
                confidence_score = confidence_score + score
            elif (label == 'pride'):
                confidence_score = confidence_score + score
            elif (label == 'approval'):
                confidence_score = confidence_score + score
                
            # Contentment
            elif (label == 'joy'):
                content_score = content_score + score
            elif (label == 'relief'):
                content_score = content_score + score
            elif (label == 'gratitude'):
                content_score = content_score + score
                
            # Neutral
            elif (label == 'neutral'):
                neutral_score = neutral_score + score
                
            # Frustration
            elif (label == 'annoyance'):
                frustrated_score = frustrated_score + score
            elif (label == 'disapproval'):
                frustrated_score = frustrated_score + score
                
            # Upset
            elif (label == 'anger'):
                upset_score = upset_score + score
            elif (label == 'sadness'):
                upset_score = upset_score + score
            elif (label == 'disappointment'):
                upset_score = upset_score + score
                
            # Anxiety
            elif (label == 'nervousness'):
                anxiety_score = anxiety_score + score
            elif (label == 'fear'):
                anxiety_score = anxiety_score + score
                
            # Surprise
            elif (label == 'surprise'):
                surprise_score = surprise_score + score
            elif (label == 'confusion'):
                surprise_score = surprise_score + score
                
        return confidence_score, content_score, neutral_score, frustrated_score, upset_score, anxiety_score, surprise_score

    # Iterating through the dataframe to score every single row
    def process_dataframe(self, df):
        confidence_list = []
        content_list = []
        neutral_list = []
        frustrated_list = []
        upset_list = []
        anxiety_list = []
        surprise_list = []
        for index in range(len(df)):
            row = df.iloc[index]
            text = row['transcript']
            logging.info(f"Scoring text for row {index}...")
            
            conf, cont, neut, frust, ups, anx, surp = self.score_text(text)
            
            confidence_list.append(conf)
            content_list.append(cont)
            neutral_list.append(neut)
            frustrated_list.append(frust)
            upset_list.append(ups)
            anxiety_list.append(anx)
            surprise_list.append(surp)
            
        df['confidence'] = confidence_list
        df['content'] = content_list
        df['neutrality'] = neutral_list
        df['frustration'] = frustrated_list
        df['upset'] = upset_list
        df['anxiety'] = anxiety_list
        df['surprise'] = surprise_list
        return df
    
#Testing function to run some basic tests on the sentiment engine
def run_tests():
    logging.info("Running tests for the sentiment engine...")
    test_data = []
    
    # Making a fake row of data to see if the huggingface model downloads and scores correctly
    row1 = {}
    row1['video_id'] = 'test1_thunder'
    row1['transcript'] = "We played great tonight. I am very proud of the team and we are ready for the next round."
    test_data.append(row1)

    df_test = pd.DataFrame(test_data)
    
    engine = SentimentEngine()
    df_scored = engine.process_dataframe(df_test)
    
    print(df_scored)

if (__name__ == "__main__"):
    # run_tests()
    pass