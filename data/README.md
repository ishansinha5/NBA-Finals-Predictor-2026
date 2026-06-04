# Data Architecture & Ingestion Pipeline

This directory acts as the central nervous system for the NLP Engine, housing the raw transcript manifests, the streaming datasets, and the cached vector store.

## Why This Structure Works
The pipeline is designed to keep data-processing decoupled from the application logic. 
* **The Manifest Layer:** The JSON files function as our "source of truth." These files track YouTube UUIDs and critical metadata like `bracket_tier` (progress level) and `won_championship` status. Tracking championship winners allows the model to map emotional baselines back to proven championship psychology, while the `bracket_tier` (e.g., Round 1 vs. Conference Finals) enables us to normalize expectations—it helps the model understand that a team surviving to the Conference Finals is under significantly different pressure than an early-round entrant. We also have metadata to clarify whether it was a star or a teammate or a coach speaking. For videos where multiple people would be interviewed in sequence, we would loop to timestamps. 
* **The Processing Layer:** Scripts ingest these manifests, run the transcript scraping, apply linear imputation to fill gaps in sparse historical datasets, and output the processed `raw_*.csv` and `scored_*.csv` files.
* **Separation of Concerns:** By isolating the raw data, the scored sentiment data, and the cached vector store, we ensure that the front-end never has to handle raw I/O, keeping the application performance snappy and predictable.

## Engineering Challenges
Data scraping was the most time-consuming part of this project. It wasn't just "hit API and wait." We ran into consistent roadblocks:
1. **The Transcription Bottleneck:** Many teams have restricted access to post-game podium transcripts, or they simply disable standard YouTube auto-captioning. To maintain data integrity, I had to build a custom audio extraction loop that piped raw MP4 audio feeds into a local instance of OpenAI’s Whisper to generate clean text files for teams that didn't provide standard captions. 
2. **Broadcast-Grade Audio Noise:** For teams where raw press room feeds were unavailable, I often had to pivot to scraping audio from high-density broadcast channel streams. This meant dealing with broadcast noise, crowd ambience, and music, which necessitated significant noise filtering and pre-processing work during the tokenization phase to isolate clean teammate sound bites.

## Data Practice & Housekeeping
You will notice that several folders (like `vector_store/`) and large CSV files are not visible in the repository. This is intentional. Large databases (like our ChromaDB store) and raw datasets are excluded from Git to keep the repository lightweight and to prevent leaking sensitive or unnecessary large-binary files into the version history. This is industry-standard practice to maintain clean, fast deployments. If you clone this repository, you generate these files locally by running the ingestion and scoring scripts in `scripts/`.