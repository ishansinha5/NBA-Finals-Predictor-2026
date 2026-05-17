import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Class to handle grabbing Youtube captions and doing some basic cleaning
class TranscriptIngestor:
    def __init__(self, data_dir="../data/raw/", min_words=150):
        self.data_dir = data_dir
        self.min_words = min_words
        
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
                raw_transcript_list = YouTubeTranscriptApi.get_transcript(vid_id)
                
                # Setting up the timestamps if we have mashed together interviews
                start_time = 0.0
                end_time = 999999.0
                
                if ('start_time' in video):
                    start_time = video['start_time']
                    
                if ('end_time' in video):
                    end_time = video['end_time']
                
                # Slicing the transcript so we only get the parts we want
                filtered_transcript_list = []
                for segment in raw_transcript_list:
                    segment_start = segment['start']
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
                
                all_transcripts.append(video_data)
                logging.info("Successfully got a good transcript!")

            except Exception as e:
                logging.error(f"Failed to get video {vid_id} because of error: {e}")

        df = pd.DataFrame(all_transcripts)
        return df

    def save_to_csv(self, df, filename="raw_transcripts.csv"):
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False)
        logging.info(f"Saved the dataframe to {filepath}")