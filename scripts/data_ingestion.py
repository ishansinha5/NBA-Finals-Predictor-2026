import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import time
import random
import tempfile
import yt_dlp
from faster_whisper import WhisperModel

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class TranscriptIngestor:
    def __init__(self, data_dir="./data/historical/", min_words=150, whisper_model_size="base"):
        self.data_dir = data_dir
        self.min_words = min_words
        
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            
        # V3 UPGRADE: Initialize the local Whisper model in memory
        logging.info(f"Initializing local faster-whisper model ({whisper_model_size})...")
        self.whisper_model = WhisperModel(whisper_model_size, device="cpu", compute_type="int8")

    def download_audio_temp(self, video_id):
        """Downloads just the audio track to a temporary file for Whisper to process."""
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"{video_id}.mp3")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_file_path,
            'quiet': True,
            'no_warnings': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        # Still use cookies if available to bypass IP bans on the audio download
        cookie_path = os.path.join(os.getcwd(), "cookies.txt")
        if os.path.exists(cookie_path):
            ydl_opts['cookiefile'] = cookie_path
            
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            return temp_file_path
        except Exception as e:
            logging.error(f"  ✗ yt-dlp failed to download audio for {video_id}: {e}")
            return None

    def fetch_local_whisper(self, video_id, start_time=None, end_time=None):
        """Fallback method: Transcribes audio locally using faster-whisper."""
        logging.info(f"  ↳ Routing to Local Whisper...")
        
        audio_path = self.download_audio_temp(video_id)
        if not audio_path:
            return False, ""
            
        try:
            # Run the transcription
            segments, info = self.whisper_model.transcribe(audio_path, beam_size=5)
            
            full_text = ""
            for segment in segments:
                # Apply the JSON timestamp filters if they exist
                if start_time is not None and segment.start < start_time:
                    continue
                if end_time is not None and segment.start > end_time:
                    continue
                    
                full_text += segment.text + " "
                
            # Clean up the temporary audio file!
            os.remove(audio_path)
            
            words = full_text.split()
            if len(words) < self.min_words:
                logging.warning(f"  ! Local Whisper transcript too short ({len(words)} words).")
                return False, ""
                
            logging.info(f"  ✓ Local Whisper succeeded for {video_id}.")
            return True, full_text
            
        except Exception as e:
            logging.error(f"  ✗ Local Whisper transcription failed: {e}")
            if os.path.exists(audio_path):
                os.remove(audio_path)
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
            start_bounds = video.get('start_time')
            end_bounds = video.get('end_time')
            
            try:
                # Tier 1: YouTube API
                api = YouTubeTranscriptApi()
                fetched_snippets = api.fetch(vid_id, languages=['en', 'en-US'])
                raw_transcript = [
                    {
                        'text': getattr(snip, 'text', str(snip)), 
                        'start': getattr(snip, 'start', 0)
                    } 
                    for snip in fetched_snippets
                ]
                success, full_text = self.evaluate_transcript(raw_transcript, start_bounds, end_bounds)
                
            except Exception as e:
                logging.warning(f"  ! Tier 1 YT API Error for {vid_id}: {str(e)[:150]}")
                # V3 UPGRADE: Route to local Whisper, passing timestamps
                success, full_text = self.fetch_local_whisper(vid_id, start_bounds, end_bounds)
                
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
                time.sleep(random.uniform(5, 8))
            else:
                logging.error(f"Total failure for {vid_id}. Transcript too short or API blocked.")

        if os.path.exists(filepath):
            return pd.read_csv(filepath)
        return pd.DataFrame()