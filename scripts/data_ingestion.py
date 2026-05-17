import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import time
import random

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class TranscriptIngestor:
    def __init__(self, data_dir="../data/raw/", min_words=150):
        self.data_dir = data_dir
        self.min_words = min_words
        
        if (not os.path.exists(self.data_dir)):
            os.makedirs(self.data_dir)

    def evaluate_transcript(self, transcript_list):
        full_text = ""
        for segment in transcript_list:
            text_part = segment.text
            full_text = full_text + text_part + " "
            
        words = full_text.split()
        word_count = len(words)
        
        if (word_count < self.min_words):
            return False, ""
        else:
            return True, full_text

    def fetch_transcripts(self, video_metadata, save_filename="raw_historical.csv"):
        filepath = os.path.join(self.data_dir, save_filename)
        completed_ids = []
        
        if (os.path.exists(filepath) == True):
            existing_df = pd.read_csv(filepath)
            for index in range(len(existing_df)):
                row = existing_df.iloc[index]
                vid = row['video_id']
                completed_ids.append(vid)
            logging.info("Found a checkpoint file! Skipping the videos we already have.")

        # going back to a purely anonymous api connection so we drop the burned cookie
        ytt_api = YouTubeTranscriptApi()

        for video in video_metadata:
            vid_id = video['video_id']
            
            if (vid_id in completed_ids):
                logging.info(f"Already downloaded {vid_id}, skipping it.")
                continue
                
            logging.info(f"Checking video: {vid_id}")
            
            try:
                raw_transcript_list = ytt_api.fetch(vid_id)
                
                start_time = 0.0
                end_time = 999999.0
                
                if ('start_time' in video):
                    start_time = video['start_time']
                    
                if ('end_time' in video):
                    end_time = video['end_time']
                
                filtered_transcript_list = []
                for segment in raw_transcript_list:
                    segment_start = segment.start
                    if (segment_start >= start_time):
                        if (segment_start <= end_time):
                            filtered_transcript_list.append(segment)
                
                is_good, full_text = self.evaluate_transcript(filtered_transcript_list)
                
                if (is_good == False):
                    logging.warning("Video too short or sliced too small, skipping it.")
                    continue
                
                video_data = {}
                video_data['video_id'] = vid_id
                
                if ('team' in video):
                    video_data['team'] = video['team']
                else:
                    video_data['team'] = 'Unknown'
                    
                if ('stage' in video):
                    video_data['stage'] = video['stage']
                else:
                    video_data['stage'] = 'Unknown'
                    
                if ('won_championship' in video):
                    video_data['won_championship'] = video['won_championship']
                else:
                    video_data['won_championship'] = 0
                    
                clean_text = full_text.replace('\n', ' ')
                video_data['transcript'] = clean_text
                
                video_data_list = []
                video_data_list.append(video_data)
                single_video_df = pd.DataFrame(video_data_list)
                
                if (os.path.exists(filepath) == True):
                    single_video_df.to_csv(filepath, mode='a', header=False, index=False)
                else:
                    single_video_df.to_csv(filepath, mode='w', header=True, index=False)
                    
                logging.info("Successfully got a good transcript and saved it to the checkpoint!")
                
                sleep_time = random.uniform(3, 7)
                logging.info(f"Sleeping for {sleep_time} seconds to avoid IP block...")
                time.sleep(sleep_time)

            except Exception as e:
                logging.error(f"Failed to get video {vid_id} because of error: {e}")

        if (os.path.exists(filepath) == True):
            final_df = pd.read_csv(filepath)
            return final_df
        else:
            return pd.DataFrame()

    def save_to_csv(self, df, filename="raw_transcripts.csv"):
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False)
        logging.info(f"Saved the dataframe to {filepath}")

if (__name__ == "__main__"):
    pass