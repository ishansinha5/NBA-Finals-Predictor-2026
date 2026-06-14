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
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_global_styles()
render_navigation()

# Main Header Banner
st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Image Rendering
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

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("## A Successful Prediction")
st.write(
    "Prior to the conclusion of the 2026 NBA Finals, this model's Targeted Modern Pipeline projected that the **New York Knicks would defeat the San Antonio Spurs in 5 games.** "
    "This prediction was logged in this repository's version control on June 3, 2026. On June 13, 2026, the Knicks successfully closed out the series. "
    "You can view the full verification details and reflection on the Validation page of this dashboard."
)
st.markdown("---")

st.markdown("## The Question: Can we mathematically quantify a 'Championship Mindset'?")
st.write(
    "Standard basketball analytics usually focus on box score statistics like field goal rates, defensive metrics, and true shooting efficiency. "
    "While those numbers do a great job of showing what happened on the court, they cannot quite capture the mental mindset and emotional state of a locker room dealing with playoff intensity. "
)
st.write(
    "I built this Natural Language Processing (NLP) pipeline to branch out from traditional tabular data science. I wanted to see if the emotional language used in post-game press conferences could reveal a team's psychological readiness to win a ring. "
    "My goal was to discover whether steady linguistic composure can actually act as a helpful leading indicator for tracking championship runs."
)

st.markdown("---")

st.markdown("## Core Project Steps")
st.write("The overall architecture processes language data across two straightforward layers to build our sports intelligence backend:")

st.markdown("### Phase 1: Tabular Sentiment and Predictive Analysis")
st.markdown("""
* **Transcript Ingestion:** The pipeline maps game indexes to video tags, pulling available text tracks or sending media audio streams directly into a local Whisper speech-to-text model when auto-captions are disabled.
* **Linguistic Feature Extraction:** The system breaks down post-game statements across a specialized language model to measure precise readings for specific emotions, including confidence, contentment, neutrality, frustration, upset, anxiety, and surprise.
* **The Scoring Filter Boundary:** To protect the models from data corruption, we explicitly stop collecting transcript data exactly one game before any series is decided. This prevents the highly celebratory, anomalous emotional spikes of a clinching game from poisoning our regular series indicators.
* **Roster Layer Classification:** The data is flattened independently across coaches, franchise stars, and supporting teammates to see how closely aligned a group stays during a series.
""")

st.markdown("### Phase 2: Search Index and Retrieval Augmentation (RAG)")
st.markdown("""
* **Semantic Local Storage:** Passages are saved into a localized search database, allowing us to query exact quotes by team filters or specific game scenarios.
* **Deterministic Verification Terminal:** Instead of relying on expensive live LLM endpoints, this interface presents pre-compiled, high-yield semantic scenarios. It showcases the exact functionality of our offline ChromaDB pipeline.
""")

st.markdown("---")

st.markdown("## Computing Priorities and Resource Mindfulness")
st.write(
    "A major personal goal while designing this tool was keeping things computationally lightweight and sustainable. "
    "Instead of relying on heavy cloud servers or paid online interfaces that require massive computing steps, this tracking pipeline handles everything locally."
)

st.markdown("""
* **Compact Models:** All text parsing is done using localized transformer architectures (`roberta-base-go_emotions`). This lets us compute complex language shapes on consumer-grade hardware.
* **Fast Binary Indexing:** Storing data coordinates in local database tables keeps lookup speeds under a millisecond while entirely skipping heavy software overhead.
* **Continuous Uptime via CI/CD:** To navigate automatic container idling, I implemented a GitHub Actions cron-job workflow to act as a daily keep-alive ping. This ensures the dashboard remains highly available for portfolio display without incurring cloud compute costs.
""")