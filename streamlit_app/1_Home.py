import streamlit as st
import base64
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if (ROOT_DIR not in sys.path):
    sys.path.append(ROOT_DIR)

from utils.navigation import apply_global_styles, render_navigation






# ── Page entry point ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="2026 NBA Finals NLP Predictor",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_global_styles()
render_navigation()

# Main Header Banner
st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Bulletproof Image Seeker targeting .png explicitly
possible_paths = [
    os.path.join(ROOT_DIR, "spursknicks.png"),
    os.path.join(ROOT_DIR, "streamlit_app", "spursknicks.png"),
    os.path.join(ROOT_DIR, "assets", "spursknicks.png"),
    os.path.join(ROOT_DIR, "streamlit_app", "assets", "spursknicks.png"),
    os.path.join(os.path.dirname(ROOT_DIR), "assets", "spursknicks.png")
]

img_path = None
for p in possible_paths:
    if (os.path.exists(p) == True):
        img_path = p
        break

if (img_path != None):
    st.image(img_path, use_container_width=True)
else:
    st.info("Matchup header graphic 'spursknicks.png' loading out of assets repository...")

st.markdown("<br>", unsafe_allow_html=True)
st.write(
    "Welcome to the NBA Post-Game NLP Engine. This project is built to extract, tokenize, and analyze text sentiment "
    "from press room transcripts, mapping out emotional stability patterns to spot exactly when teams crack under pressure. "
    "By stacking machine learning classification alongside a localized transcript evidence system, we track how coaches, "
    "marquee stars, and bench players maintain composure across full postseason runs."
)

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
* **Deterministic Verification Terminal:** Instead of relying on expensive, live cloud LLM endpoints that violate Green AI principles, this interface presents pre-compiled, high-yield semantic scenarios. It showcases the exact functionality of our offline ChromaDB pipeline with zero external computational overhead.
""")

st.markdown("---")

st.markdown("## Computing Priorities and Resource Mindfulness")
st.markdown("""
A major personal goal while designing this tool was keeping things computationally lightweight and runnable on standard hardware. Instead of relying on heavy cloud servers or paid online interfaces that require massive computing steps, this tracking pipeline handles everything locally to keep a small processing footprint.

* **Compact Models:** All text parsing is done using localized transformer architectures. This lets us compute complex language shapes on consumer-grade hardware with zero network dependencies.
* **Smart Memory Boundaries:** The ingestion system processes data using a custom context generator to stay safely inside system memory layout limits.
* **Fast Binary Indexing:** Storing data coordinates in local database tables keeps lookup speeds under a millisecond while entirely skipping heavy software overhead.
""")