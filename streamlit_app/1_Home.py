import streamlit as st
import sys
import os

# Get the absolute path to the root directory (one level up from streamlit_app)
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# Now Python can safely find utils
from utils.navigation import apply_global_styles, render_navigation

# Configure the page layout
st.set_page_config(
    page_title="2026 NBA Finals NLP Predictor", 
    page_icon="🏀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Inject background, CSS, and Top Menu
apply_global_styles()
render_navigation()

# Main Header Banner
st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Hero Visual Section
st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop", width="stretch")

st.markdown("## Project Motivation")
st.markdown("""
Standard basketball analytics usually focus on box score statistics like field goal rates, defensive metrics, and true shooting efficiency. While those numbers do a great job of showing *what* happened on the court, they cannot quite capture the mental mindset and emotional state of a locker room dealing with playoff intensity. 

I wanted to see if we could find a new angle by looking at text data from post-game podium press conferences. This project converts those transcripts into clear emotional scores. My goal was to discover whether steady linguistic composure can actually act as a helpful indicator for tracking championship runs.
""")

st.markdown("---")

st.markdown("## Core Project Steps")
st.markdown("""
The overall architecture processes language data across two straightforward layers to build our sports intelligence backend:

### Phase 1: Tabular Sentiment and Predictive Analysis
* **Transcript Ingestion:** The pipeline maps game indexes to video tags, pulling available text tracks or sending media audio streams directly into a local speech-to-text model when requests face network limits.
* **Linguistic Feature Extraction:** The system breaks down post-game statements across a specialized language model to measure precise readings for specific emotions, including *confidence, contentment, neutrality, frustration, upset, anxiety, and surprise*.
* **The Scoring Filter Boundary:** To protect the models from data corruption, we explicitly stop collecting transcript data exactly one game before any series is decided. This prevents the highly celebratory, anomalous emotional spikes of a clinching game from poisoning our regular series indicators.
* **Roster Layer Classification:** The data is flattened independently across coaches, franchise stars, and supporting teammates to see how closely aligned a group stays during a series.

### Phase 2: Search Index and Retrieval Augmentation (RAG)
* **Text Partitioning:** The engine divides long interview documents into small paragraphs to make sure text strings do not get clipped by processing thresholds.
* **Semantic Local Storage:** Passages are saved into a localized search database, allowing us to query exact quotes by team filters or specific game scenarios.
* **Query Interface:** A simple terminal lets users query real context directly from historical playoff files, making it easy to see exactly what players said without reading through hours of text manually.
""")

st.markdown("---")

st.markdown("## Computing Priorities and Resource Mindfulness")
st.markdown("""
A major personal goal while designing this tool was keeping things computationally lightweight and runnable on standard hardware. Instead of relying on heavy cloud servers or paid online interfaces that require massive computing steps, this tracking pipeline handles everything locally to keep a small processing footprint.

* **Compact Models:** All text parsing is done using localized transformer architectures. This lets us compute complex language shapes on consumer-grade hardware with zero network dependencies.
* **Smart Memory Boundaries:** The ingestion system processes data using a custom context generator to stay safely inside system memory layout limits.
* **Fast Binary Indexing:** Storing data coordinates in local database tables keeps lookup speeds under a millisecond while entirely skipping heavy software overhead.
""")