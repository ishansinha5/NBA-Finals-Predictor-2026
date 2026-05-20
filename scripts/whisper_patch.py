"""
whisper_patch.py — Hardened Spurs transcription patch
Strategy: HF Gradio Space (primary) → local yt-dlp + faster-whisper (fallback)

Install fallback deps once if needed:
    pip install yt-dlp faster-whisper

Usage:
    python whisper_patch.py
"""

import json
import time
import csv
import os
import logging
import tempfile
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────

MANIFEST_PATH    = "data/2025-2026_playoff_vids.json"
RAW_CSV_PATH     = "data/live_2026/raw_live_2026.csv"
OUTPUT_PATCH_TXT = "spurs_manual_patch.txt"
TARGET_TEAM      = "Spurs"
HF_SPACE         = "rajesh1729/youtube-video-transcription-with-whisper"
API_ENDPOINT     = "/get_text"
SLEEP_BETWEEN    = 30          # seconds, to respect HF rate limits
WHISPER_MODEL    = "base"      # tiny | base | small — balance speed vs quality
MAX_CHARS        = 2500        # RoBERTa head truncation, consistent with original
REQUEST_TIMEOUT  = 120         # seconds before we consider the HF Space hung


# ── Helpers ───────────────────────────────────────────────────────────────────

def load_completed_ids(csv_path: str, team: str) -> set:
    """Return video_ids already present in the CSV for the given team."""
    completed = set()
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("team") == team:
                    completed.add(row["video_id"])
        log.info(f"Found {len(completed)} already-processed {team} videos.")
    except FileNotFoundError:
        log.warning(f"{csv_path} not found — assuming 0 completed videos.")
    return completed


def load_target_videos(manifest_path: str, team: str, completed: set) -> list:
    """Return manifest entries for team that haven't been processed yet."""
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    targets = [
        v for v in manifest
        if v["team"] == team and v["video_id"] not in completed
    ]
    log.info(f"Found {len(targets)} unprocessed {team} videos to transcribe.")
    return targets


def normalize_url(video_id: str) -> str:
    """Use the long-form URL — more compatible with yt-dlp internals on HF."""
    return f"https://www.youtube.com/watch?v={video_id}"


def sanitize(text: str, max_chars: int = MAX_CHARS) -> str:
    """Strip newlines and commas (CSV safety), collapse whitespace, truncate."""
    text = text.replace("\n", " ").replace(",", " ")
    text = " ".join(text.split())
    return text[:max_chars]


# ── Transcription back-ends ───────────────────────────────────────────────────

def transcribe_via_hf_space(url: str) -> str | None:
    """
    Primary path: call the Gradio Space.
    Returns clean text on success, None on any failure.

    Common failure modes handled:
    - Space sleeping / cold-start timeout  → caught by generic Exception
    - Upstream app exception (no verbose)  → caught, returns None
    - Hung request                         → gradio_client has no native timeout;
      we rely on the OS-level socket timeout set below.
    """
    try:
        from gradio_client import Client
        # httpx (used internally by gradio_client) respects HTTPX_TIMEOUT
        os.environ.setdefault("HTTPX_TIMEOUT", str(REQUEST_TIMEOUT))

        client = Client(HF_SPACE)
        result = client.predict(url=url, api_name=API_ENDPOINT)

        if not result or not isinstance(result, str):
            log.warning("HF Space returned empty or unexpected response type.")
            return None

        return sanitize(result)

    except Exception as e:
        err = str(e)
        # Distinguish known-bad Space errors from transient network issues
        if "upstream Gradio app has raised an exception" in err:
            log.warning(f"HF Space internal error (likely yt-dlp or Whisper OOM): {e}")
        elif "Connection" in err or "timeout" in err.lower():
            log.warning(f"HF Space network/timeout error: {e}")
        else:
            log.warning(f"HF Space unexpected error: {e}")
        return None


def transcribe_via_local_whisper(video_id: str, start_time: float | None, end_time: float | None) -> str | None:
    """
    Fallback path: download audio with yt-dlp, transcribe with faster-whisper.
    Handles start_time/end_time for shared video IDs (e.g., split press-conf recordings).
    Returns clean text on success, None on failure.
    """
    try:
        import yt_dlp
        from faster_whisper import WhisperModel
    except ImportError:
        log.error(
            "Fallback deps missing. Install with:\n"
            "  pip install yt-dlp faster-whisper"
        )
        return None

    url = normalize_url(video_id)

    with tempfile.TemporaryDirectory() as tmpdir:
        audio_path = os.path.join(tmpdir, "audio.%(ext)s")

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": audio_path,
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }],
        }

        # ── Segment extraction (handles start_time / end_time in manifest) ──
        # Only slice if at least one boundary is defined
        if start_time is not None or end_time is not None:
            download_sections = []
            start_str = str(int(start_time)) if start_time is not None else "0"
            end_str   = str(int(end_time))   if end_time is not None  else "inf"
            download_sections.append(f"*{start_str}-{end_str}")
            ydl_opts["download_ranges"] = yt_dlp.utils.download_range_func(None, download_sections)
            ydl_opts["force_keyframes_at_cuts"] = True
            log.info(f"Slicing audio: {start_str}s → {end_str}s")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as e:
            log.error(f"yt-dlp download failed for {video_id}: {e}")
            return None

        # Find the downloaded .wav file
        wav_files = list(Path(tmpdir).glob("*.wav"))
        if not wav_files:
            log.error(f"No audio file found after download for {video_id}.")
            return None

        wav_file = str(wav_files[0])

        # ── Whisper inference ──────────────────────────────────────────────
        log.info(f"Running faster-whisper ({WHISPER_MODEL}) on {os.path.basename(wav_file)}...")
        try:
            model = WhisperModel(WHISPER_MODEL, device="cpu", compute_type="int8")
            segments, _ = model.transcribe(wav_file, beam_size=1)
            full_text = " ".join(seg.text for seg in segments)
            return sanitize(full_text)
        except Exception as e:
            log.error(f"Whisper transcription failed for {video_id}: {e}")
            return None


# ── Main patch runner ─────────────────────────────────────────────────────────

def run_spurs_patch():
    log.info("=== Spurs Whisper Patch (hardened) ===")

    completed = load_completed_ids(RAW_CSV_PATH, TARGET_TEAM)
    targets   = load_target_videos(MANIFEST_PATH, TARGET_TEAM, completed)

    if not targets:
        log.info("Nothing to do — all Spurs videos already processed.")
        return

    stats = {"hf_success": 0, "local_success": 0, "failed": 0}

    with open(OUTPUT_PATCH_TXT, "w", encoding="utf-8") as out_f:
        for i, vid in enumerate(targets, 1):
            video_id   = vid["video_id"]
            stage      = vid.get("stage", "Unknown")
            start_time = vid.get("start_time")   # float or None
            end_time   = vid.get("end_time")     # float or None
            url        = normalize_url(video_id)

            log.info(f"\n[{i}/{len(targets)}] {video_id} | {stage}")

            # ── Tier 1: HF Space ──────────────────────────────────────────
            text = transcribe_via_hf_space(url)
            if text:
                log.info(f"  ✓ HF Space succeeded.")
                stats["hf_success"] += 1
            else:
                # ── Tier 2: local Whisper ─────────────────────────────────
                log.info(f"  ↳ HF Space failed. Falling back to local Whisper...")
                text = transcribe_via_local_whisper(video_id, start_time, end_time)
                if text:
                    log.info(f"  ✓ Local Whisper succeeded.")
                    stats["local_success"] += 1
                else:
                    log.error(f"  ✗ Both tiers failed for {video_id}.")
                    text = "FAILED"
                    stats["failed"] += 1

            # Write result — CSV-safe (commas already stripped in sanitize)
            out_f.write(f"{video_id},{TARGET_TEAM},{stage},{text}\n")
            out_f.flush()

            # Rate-limit only between HF Space calls; local Whisper is self-throttling
            if i < len(targets) and text != "FAILED":
                if stats["hf_success"] > 0:
                    log.info(f"  Sleeping {SLEEP_BETWEEN}s...")
                    time.sleep(SLEEP_BETWEEN)

    log.info(
        f"\n=== Done ===\n"
        f"  HF Space successes : {stats['hf_success']}\n"
        f"  Local Whisper wins : {stats['local_success']}\n"
        f"  Total failures     : {stats['failed']}\n"
        f"  Output             : {OUTPUT_PATCH_TXT}\n"
        f"\nAppend to {RAW_CSV_PATH}:\n"
        f"  cat {OUTPUT_PATCH_TXT} >> {RAW_CSV_PATH}"
    )


if __name__ == "__main__":
    run_spurs_patch()