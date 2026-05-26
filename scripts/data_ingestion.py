import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import time
import random
import requests

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class TranscriptIngestor:
    def __init__(self, data_dir="./output/historical/", min_words=150):
        self.data_dir = data_dir
        self.min_words = min_words
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # The Hugging Face Gradio endpoint for headless transcription
        self.hf_endpoint = "https://rajesh1729-youtube-video-transcription-with-whisper.hf.space/run/predict"

    def fetch_hf_whisper(self, video_id):
        """Fallback method: Hits the remote Whisper model if YT captions are disabled."""
        logging.info(f"  ↳ Routing to Hugging Face Whisper...")
        url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            response = requests.post(
                self.hf_endpoint,
                json={"data": [url]},
                timeout=120
            )
            if response.status_code == 200:
                result = response.json()
                if "data" in result and len(result["data"]) > 0:
                    logging.info(f"  ✓ HF Whisper succeeded for {video_id}.")
                    return True, result["data"][0]
            else:
                logging.error(f"  ✗ HF Whisper HTTP Error: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            logging.error(f"  ✗ HF Whisper Request failed: {e}")
        return False, ""

    def evaluate_transcript(self, transcript_list, start_time=None, end_time=None):
        full_text = ""
        for segment in transcript_list:
            if isinstance(segment, dict):
                text = segment.get('text', '')
                start = segment.get('start', 0)
            else:
                text = getattr(segment, 'text', str(segment))
                start = getattr(segment, 'start', 0)
                
            # Skip the text chunk if it falls outside our defined timestamps
            if start_time is not None and start < start_time:
                continue
            if end_time is not None and start > end_time:
                continue
                
            full_text += text + " "
            
        words = full_text.split()
        if len(words) < self.min_words:
            return False, ""
        return True, full_text

    def fetch_transcripts(self, video_metadata, save_filename="raw_historical.csv"):
        filepath = os.path.join(self.data_dir, save_filename)
        completed_ids = []
        
        if os.path.exists(filepath):
            existing_df = pd.read_csv(filepath)
            if 'video_id' in existing_df.columns:
                completed_ids = existing_df['video_id'].tolist()
                logging.info(f"Found a checkpoint! Skipping the {len(completed_ids)} videos we already have.")
            
        for video in video_metadata:
            vid_id = video['video_id']
            
            if vid_id in completed_ids:
                continue
                
            logging.info(f"Attempting to pull: {vid_id} ({video['team']} - {video.get('role', 'aggregate')})")
            
            success = False
            full_text = ""
            
            try:
                # Tier 1: The Working Object-Instantiation Syntax
                api = YouTubeTranscriptApi()
                fetched_snippets = api.fetch(vid_id, languages=['en', 'en-US'])
                
                # UPDATE: We now extract the timestamp ('start') from the YouTube snippet
                raw_transcript = [
                    {
                        'text': getattr(snip, 'text', str(snip)), 
                        'start': getattr(snip, 'start', 0)
                    } 
                    for snip in fetched_snippets
                ]
                
                # Pass the JSON time boundaries into the evaluator
                start_bounds = video.get('start_time')
                end_bounds = video.get('end_time')
                success, full_text = self.evaluate_transcript(raw_transcript, start_bounds, end_bounds)
                
            except Exception as e:
                logging.warning(f"  ! Tier 1 YT API Error for {vid_id}: {str(e)[:150]}")
                success, full_text = self.fetch_hf_whisper(vid_id)
            if success:
                video_data = {
                    'video_id': vid_id,
                    'team': video['team'],
                    'stage': video['stage'],
                    'role': video.get('role', 'aggregate'), # V2 schema enforcement
                    'won_championship': video.get('bracket_result', 0),
                    'transcript': full_text.replace('\n', ' ')
                }
                
                single_video_df = pd.DataFrame([video_data])
                
                if os.path.exists(filepath):
                    single_video_df.to_csv(filepath, mode='a', header=False, index=False)
                else:
                    single_video_df.to_csv(filepath, mode='w', header=True, index=False)
                    
                logging.info(f"Saved {vid_id} to the checkpoint.")
                time.sleep(random.uniform(2, 5))
            else:
                logging.error(f"Total failure for {vid_id}. Transcript too short or API blocked.")

        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        return pd.DataFrame()