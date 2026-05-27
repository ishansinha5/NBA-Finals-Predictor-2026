import os
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
import logging
import time
import random
import tempfile
import yt_dlp
from faster_whisper import WhisperModel
import socket

# Prevent the terminal from silently hanging if a VPN connection drops
socket.setdefaulttimeout(30)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class TranscriptIngestor:
    def __init__(self, data_dir="./data/historical/", min_words=150, whisper_model_size="base"):
        self.data_dir = data_dir
        self.min_words = min_words
        self.whisper_cache = {} # Cache for audio-transcribed text
        self.transcript_cache = {} # V5 UPGRADE: Global Cache for API-fetched transcripts
        
        if (not os.path.exists(self.data_dir)):
            os.makedirs(self.data_dir)
            
        logging.info(f"Initializing local faster-whisper model ({whisper_model_size})...")
        self.whisper_model = WhisperModel(whisper_model_size, device="cpu", compute_type="int8")

    def download_audio_temp(self, video_id):
        """Downloads just the audio track to a temporary file for Whisper to process."""
        temp_dir = tempfile.gettempdir()
        
        # We use %(ext)s so yt-dlp safely handles the raw format without clobbering it
        outtmpl = os.path.join(temp_dir, f"{video_id}.%(ext)s")
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'quiet': True,
            'no_warnings': True,
        }
        
        cookie_path = os.path.join(os.getcwd(), "cookies.txt")
        if (os.path.exists(cookie_path)):
            ydl_opts['cookiefile'] = cookie_path
            
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=True)
                
                ext = info.get('ext', 'webm')
                if ('requested_downloads' in info):
                    ext = info['requested_downloads'][0].get('ext', ext)
                    
                downloaded_file = os.path.join(temp_dir, f"{video_id}.{ext}")
                
                if (os.path.exists(downloaded_file)):
                    return downloaded_file
                else:
                    logging.error(f"  ! yt-dlp reported success, but file {downloaded_file} is missing.")
                    return None
                    
        except Exception as e:
            logging.error(f"  ! yt-dlp failed to download audio for {video_id}: {e}")
            return None

    def fetch_local_whisper(self, video_id, start_time=None, end_time=None):
        """Fallback method: Transcribes audio locally using faster-whisper."""
        logging.info(f"  ! Routing to Local Whisper...")
        
        # Check if we already transcribed this audio
        if (video_id in self.whisper_cache):
            logging.info(f"  ! Whisper Cache Hit! Instantly loading pre-transcribed audio for {video_id}...")
            segments = self.whisper_cache[video_id]
        else:
            audio_path = self.download_audio_temp(video_id)
            if (not audio_path):
                return False, ""
                
            try:
                logging.info(f"  ! Transcribing {video_id} on CPU... this takes a few minutes. Grab a coffee!")
                segments_generator, info = self.whisper_model.transcribe(audio_path, beam_size=5)
                
                # Cast the generator to a list so it can be safely stored and reused
                segments = list(segments_generator)
                self.whisper_cache[video_id] = segments
                
                # Clean up the temporary file
                os.remove(audio_path)
                
            except Exception as e:
                logging.error(f"  ! Local Whisper transcription failed: {e}")
                if (os.path.exists(audio_path)):
                    os.remove(audio_path)
                return False, ""
                
        full_text = ""
        for segment in segments:
            if ((start_time is not None) and (segment.start < start_time)):
                continue
            elif ((end_time is not None) and (segment.start > end_time)):
                continue
                
            full_text += segment.text + " "
            
        words = full_text.split()
        if (len(words) < self.min_words):
            logging.warning(f"  ! Local Whisper transcript too short ({len(words)} words).")
            return False, ""
            
        logging.info(f"  ! Local Whisper succeeded for {video_id}.")
        return True, full_text

    def evaluate_transcript(self, transcript_list, start_time=None, end_time=None):
        full_text = ""
        for segment in transcript_list:
            if (isinstance(segment, dict)):
                text = segment.get('text', '')
                start = segment.get('start', 0)
            else:
                text = getattr(segment, 'text', str(segment))
                start = getattr(segment, 'start', 0)
                
            if ((start_time is not None) and (start < start_time)):
                continue
            elif ((end_time is not None) and (start > end_time)):
                continue
                
            full_text += text + " "
            
        words = full_text.split()
        if (len(words) < self.min_words):
            return False, ""
        return True, full_text

    def fetch_transcripts(self, video_metadata, save_filename="raw_historical.csv"):
        filepath = os.path.join(self.data_dir, save_filename)
        
        completed_keys = []
        if (os.path.exists(filepath)):
            existing_df = pd.read_csv(filepath)
            if (('video_id' in existing_df.columns) and ('role' in existing_df.columns)):
                completed_keys = (existing_df['video_id'] + "_" + existing_df['role']).tolist()
                logging.info(f"Found a checkpoint! Skipping the {len(completed_keys)} roles we already have.")
            
        for video in video_metadata:
            vid_id = video['video_id']
            stage = video.get('stage', 'Unknown')
            role = video.get('role', 'aggregate')
            composite_key = f"{vid_id}_{role}"
            
            if (composite_key in completed_keys):
                continue
            
            # V5 UPGRADE: Check global transcript cache first
            if (vid_id in self.transcript_cache):
                logging.info(f"API Cache Hit! Reusing transcript for {vid_id}...")
                success, full_text = self.transcript_cache[vid_id]
            else:
                logging.info(f"Attempting to pull: {vid_id} ({video['team']} - {stage} - {role})")
                
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
                    
                    # Store in cache so next roles don't trigger an API call
                    self.transcript_cache[vid_id] = (success, full_text)
                    
                except Exception as e:
                    logging.warning(f"  ! Tier 1 YT API Error for {vid_id}: {str(e)[:100]}")
                    success, full_text = self.fetch_local_whisper(vid_id, start_bounds, end_bounds)
                    # Cache the result even if it was a Whisper fallback (prevents re-transcribing same video for different role)
                    self.transcript_cache[vid_id] = (success, full_text)
                
            if (success):
                video_data = {
                    'video_id': vid_id,
                    'team': video['team'],
                    'stage': stage,
                    'role': role,
                    'won_championship': video.get('bracket_result', 0),
                    'transcript': full_text.replace('\n', ' ')
                }
                
                single_video_df = pd.DataFrame([video_data])
                
                if (os.path.exists(filepath)):
                    single_video_df.to_csv(filepath, mode='a', header=False, index=False)
                else:
                    single_video_df.to_csv(filepath, mode='w', header=True, index=False)
                    
                logging.info(f"Saved {vid_id} ({role}) to the checkpoint.")
                time.sleep(random.uniform(5, 8))
            else:
                logging.error(f"Total failure for {vid_id} ({role}). Transcript too short or API blocked.")

        if (os.path.exists(filepath)):
            return pd.read_csv(filepath)
        return pd.DataFrame()