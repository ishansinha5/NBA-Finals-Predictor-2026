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
    # Scoring function that expands 28 go_emotions into our 7 portfolio categories
    # V2 UPGRADE: Implements 400-word chunking to process 100% of the transcript
    def score_text(self, text):
        words = text.split()
        max_words_per_chunk = 400 
        
        # Defensive check: if the transcript is empty, return zeros
        if not words:
            return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            
        # Generator to split the text into 400-word chunks
        chunks = [' '.join(words[i:i + max_words_per_chunk]) for i in range(0, len(words), max_words_per_chunk)]
        
        # Accumulators for the whole video
        total_confidence = 0.0
        total_content = 0.0
        total_neutral = 0.0
        total_frustrated = 0.0
        total_upset = 0.0
        total_anxiety = 0.0
        total_surprise = 0.0
        
        num_chunks = len(chunks)
        
        for chunk in chunks:
            # Pass the chunk to RoBERTa. We truncate at 2500 chars just as a hard safety net 
            # against massive unspaced strings, but the 400-word limit protects the 512 token ceiling.
            results = self.classifier(chunk, truncation=True, max_length=512)
            emotions = results[0]
            
            # Looping through all 28 scores from the AI for THIS specific chunk
            for emotion in emotions:
                label = emotion['label']
                score = emotion['score']
                
                # Confidence
                if label in ['optimism', 'pride', 'approval']:
                    total_confidence += score
                # Contentment
                elif label in ['joy', 'relief', 'gratitude']:
                    total_content += score
                # Neutral
                elif label == 'neutral':
                    total_neutral += score
                # Frustration
                elif label in ['annoyance', 'disapproval']:
                    total_frustrated += score
                # Upset
                elif label in ['anger', 'sadness', 'disappointment']:
                    total_upset += score
                # Anxiety
                elif label in ['nervousness', 'fear']:
                    total_anxiety += score
                # Surprise
                elif label in ['surprise', 'confusion']:
                    total_surprise += score
                    
        # Return the mathematical average across all chunks in the video
        return (
            total_confidence / num_chunks,
            total_content / num_chunks,
            total_neutral / num_chunks,
            total_frustrated / num_chunks,
            total_upset / num_chunks,
            total_anxiety / num_chunks,
            total_surprise / num_chunks
        )
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
    #run_tests()
    pass