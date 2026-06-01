import pandas as pd
from transformers import pipeline
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SentimentEngine:
    def __init__(self, model_name="SamLowe/roberta-base-go_emotions"):
        logging.info("Loading up the AI model, this takes a lot of memory...")
        self.classifier = pipeline("text-classification", model=model_name, top_k=None)
        
    def score_text(self, text):
        words = text.split()
        max_words_per_chunk = 400 
        
        if (not words):
            return 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            
        chunks = [' '.join(words[i:i + max_words_per_chunk]) for i in range(0, len(words), max_words_per_chunk)]
        
        total_confidence = 0.0
        total_content = 0.0
        total_neutral = 0.0
        total_frustrated = 0.0
        total_upset = 0.0
        total_anxiety = 0.0
        total_surprise = 0.0
        
        num_chunks = len(chunks)
        
        for chunk in chunks:
            results = self.classifier(chunk, truncation=True, max_length=512)
            emotions = results[0]
            
            for emotion in emotions:
                label = emotion['label']
                score = emotion['score']
                
                if label in ['optimism', 'pride', 'approval']:
                    total_confidence += score
                elif label in ['joy', 'relief', 'gratitude']:
                    total_content += score
                elif label == 'neutral':
                    total_neutral += score
                elif label in ['annoyance', 'disapproval']:
                    total_frustrated += score
                elif label in ['anger', 'sadness', 'disappointment']:
                    total_upset += score
                elif label in ['nervousness', 'fear']:
                    total_anxiety += score
                elif label in ['surprise', 'confusion']:
                    total_surprise += score
                    
        return (
            total_confidence / num_chunks,
            total_content / num_chunks,
            total_neutral / num_chunks,
            total_frustrated / num_chunks,
            total_upset / num_chunks,
            total_anxiety / num_chunks,
            total_surprise / num_chunks
        )

    def process_dataframe(self, df):
        confidence_list, content_list, neutrality_list = [], [], []
        frustration_list, upset_list, anxiety_list, surprise_list = [], [], [], []
        
        for index in range(len(df)):
            row = df.iloc[index]
            text = str(row['transcript'])
            logging.info(f"Scoring text for row {index}...")
            
            conf, cont, neut, frust, ups, anx, surp = self.score_text(text)
            
            confidence_list.append(conf)
            content_list.append(cont)
            neutrality_list.append(neut)
            frustration_list.append(frust)
            upset_list.append(ups)
            anxiety_list.append(anx)
            surprise_list.append(surp)
            
        df['confidence'] = confidence_list
        df['content'] = content_list
        df['neutrality'] = neutrality_list
        df['frustration'] = frustration_list
        df['upset'] = upset_list
        df['anxiety'] = anxiety_list
        df['surprise'] = surprise_list
        return df