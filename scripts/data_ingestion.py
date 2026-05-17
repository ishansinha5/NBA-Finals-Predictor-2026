import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import logging

# Setting up logging so I can see what the code is doing in the terminal, I read that it was more professional than using print
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Class to handle grabbing Youtube captions and doing some basic cleaning
class TranscriptIngestor:
    def __init__(self, data_dir="../data/raw/", min_words=150):
        self.data_dir = data_dir
        self.min_words = min_words
        
        # Checking if the directory exists so the script doesn't crash when saving
        if (not os.path.exists(self.data_dir)):
            os.makedirs(self.data_dir)

    # Trying to figure out if this is actually a real press clip or an inaccurate short video, I don't want to waste time running the sentiment engine on bad data
    def evaluate_transcript(self, transcript_list):
        full_text = ""
        for segment in transcript_list:
            text_part = segment['text']
            full_text = full_text + text_part + " "
            
        words = full_text.split()
        word_count = len(words)
        
        if (word_count < self.min_words):
            return False, ""
        else:
            return True, full_text

    # The main engine that goes through the dictionary of videos
    def fetch_transcripts(self, video_metadata):
        all_transcripts = []

        for video in video_metadata:
            vid_id = video['video_id']
            logging.info(f"Checking video: {vid_id}")
            
            try:
                # Asking youtube for the captions
                transcript_list = YouTubeTranscriptApi.get_transcript(vid_id)
                
                is_good, full_text = self.evaluate_transcript(transcript_list)
                
                if (is_good == False):
                    logging.warning("Video too short, skipping it.")
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
                    
                clean_text = full_text.replace('\n', ' ')
                video_data['transcript'] = clean_text
                
                all_transcripts.append(video_data)
                logging.info("Successfully got a good transcript!")

            except Exception as e:
                logging.error(f"Failed to get video {vid_id} because of error: {e}")

        df = pd.DataFrame(all_transcripts)
        return df

    # Saving everything into a raw csv file
    def save_to_csv(self, df, filename="raw_transcripts.csv"):
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False)
        logging.info(f"Saved the dataframe to {filepath}")

# Testing function 
def run_tests():
    test_videos = []
    
    vid1 = {}
    vid1['video_id'] = '6UMounb2UQA' 
    vid1['team'] = 'Spurs'
    vid1['stage'] = 'Round 2'
    test_videos.append(vid1)

    vid2 = {}
    vid2['video_id'] = 'FAKE_ID_123'
    vid2['team'] = 'Thunder'
    vid2['stage'] = 'Round 2'
    test_videos.append(vid2)

    ingestor = TranscriptIngestor(data_dir="./")
    df_raw = ingestor.fetch_transcripts(test_videos)
    
    if (not df_raw.empty):
        print(df_raw.head())

if (__name__ == "__main__"):
    # run_tests()
    pass