import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import time
import random
import requests
from http.cookiejar import MozillaCookieJar

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# class to handle grabbing Youtube captions and doing some basic cleaning
class TranscriptIngestor:
    def __init__(self, data_dir="../data/raw/", min_words=150):
        self.data_dir = data_dir
        self.min_words = min_words
        
        # checking if the directory exists so the script doesn't crash when saving
        if (not os.path.exists(self.data_dir)):
            os.makedirs(self.data_dir)

    # trying to figure out if this is actually a real press clip or an inaccurate short video, I don't want to waste time running the sentiment engine on bad data
    def evaluate_transcript(self, transcript_list):
        full_text = ""
        for segment in transcript_list:
            # grabbing the text using dot notation since the library gives us objects now
            text_part = segment.text
            full_text = full_text + text_part + " "
            
        words = full_text.split()
        word_count = len(words)
        
        if (word_count < self.min_words):
            return False, ""
        else:
            return True, full_text

    # the main engine that goes through the dictionary of videos
    def fetch_transcripts(self, video_metadata, save_filename="raw_historical.csv"):
        # figuring out exactly where we are going to save the data
        filepath = os.path.join(self.data_dir, save_filename)
        
        # setting up a list to hold the ones we already downloaded so we don't repeat work
        completed_ids = []
        
        # checking if a save file already exists from a previous crash
        if (os.path.exists(filepath) == True):
            existing_df = pd.read_csv(filepath)
            
            # looping through the old data to get the video ids we already have
            for index in range(len(existing_df)):
                row = existing_df.iloc[index]
                vid = row['video_id']
                completed_ids.append(vid)
                
            logging.info("Found a checkpoint file! Skipping the videos we already have.")

        # trying to figure out how to manually load the cookies since the library updated and broke the old way
        # I found that I can use a requests session and a cookie jar to force it to use my authentication
        session = requests.Session()
        try:
            cookie_jar = MozillaCookieJar('./www.youtube.com_cookies.txt')
            cookie_jar.load(ignore_discard=True, ignore_expires=True)
            session.cookies = cookie_jar
            logging.info("Successfully loaded YouTube cookies into the request session!")
        except Exception as e:
            logging.error(f"Failed to load cookies because of error: {e}")
            return pd.DataFrame()
            
        # creating an instance of the api and giving it my authenticated session so it doesn't get blocked
        ytt_api = YouTubeTranscriptApi(http_client=session)

        for video in video_metadata:
            vid_id = video['video_id']
            
            # skipping the video if it is already inside my completed list
            if (vid_id in completed_ids):
                logging.info(f"Already downloaded {vid_id}, skipping it.")
                continue
                
            logging.info(f"Checking video: {vid_id}")
            
            try:
                # asking youtube for the captions using my authenticated api
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
                
                # putting the data into a list so I can turn it into a dataframe
                video_data_list = []
                video_data_list.append(video_data)
                single_video_df = pd.DataFrame(video_data_list)
                
                # saving this single video immediately so we don't lose it if it crashes
                if (os.path.exists(filepath) == True):
                    # opening the file in append mode without adding the headers again
                    single_video_df.to_csv(filepath, mode='a', header=False, index=False)
                else:
                    # creating the file for the first time with headers so it looks right
                    single_video_df.to_csv(filepath, mode='w', header=True, index=False)
                    
                logging.info("Successfully got a good transcript and saved it to the checkpoint!")
                
                # pausing for 3 to 7 seconds so YouTube doesn't think I am a bot
                sleep_time = random.uniform(3, 7)
                logging.info(f"Sleeping for {sleep_time} seconds to avoid IP block...")
                time.sleep(sleep_time)

            except Exception as e:
                logging.error(f"Failed to get video {vid_id} because of error: {e}")

        # reading everything from the hard drive at the end so we have the full dataset to return
        if (os.path.exists(filepath) == True):
            final_df = pd.read_csv(filepath)
            return final_df
        else:
            return pd.DataFrame()

    def save_to_csv(self, df, filename="raw_transcripts.csv"):
        # keeping this function here so I don't break main.py, but it will just overwrite the file with the same exact data
        filepath = os.path.join(self.data_dir, filename)
        df.to_csv(filepath, index=False)
        logging.info(f"Saved the dataframe to {filepath}")

def run_tests():
    pass

if (__name__ == "__main__"):
    #run_tests()
    pass