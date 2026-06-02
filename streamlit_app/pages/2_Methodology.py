import streamlit as st
import os

# Configure the page layout and strictly collapse the vertical sidebar navigation
st.set_page_config(
    page_title="Design Journey & Methodology", 
    page_icon="🏀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Injected CSS to match the vertical sidebar suppression from Home.py
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Horizontal Navigation Bar matching Home.py
nav_tabs = st.tabs([
    "🏠 Introduction & Overview", 
    "👔 Multi-Role Analytics", 
    "🧠 Interactive RAG Engine", 
    "🔮 2026 Finals Live Predictor",
    "季 Engineering Journey"
])

# Direct all content to Tab 4 (Engineering Journey) to replicate horizontal tab-switching behavior
with nav_tabs[4]:
    st.header("The Architectural Evolution: V1 vs. V2")
    st.subheader("Deep-Dive Engineering Overhaul Across Data Footprints, Feature Matrices, and Filtering Mechanics")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🛑 Legacy V1 Paradigm (The Baseline Proof-of-Concept)")
        st.markdown("""
        *   **Restricted Data Footprint:** Evaluated only 2 years of high-density data (2024 and 2025 Finals runs).
        *   **Linguistic Truncation:** Used basic hard-truncation at 2,500 characters. This frequently blind-sided the model on late press conference adjustments.
        *   **Tabular Blind Spot:** Lacked granular multi-role separation—averaging teams together in a broad, monolithic team bucket.
        *   **The Survival Bias Flaw:** By only training on teams that reached the Finals, the machine never learned what an early-round exit looked like. It could not accurately evaluate first-round panic.
        """)

    with col2:
        st.markdown("### 🚀 Upgraded V2 Framework (The Production Pipeline)")
        st.markdown("""
        *   **Preservation of the Score Filter:** We no longer take games that win any series into account out of preservation of the score. Post-series celebration scripts inject highly anomalous emotional spikes that do not reflect sustainable championship readiness. 
        *   **Tri-Tier Role Isolation:** The feature matrix has been completely refactored to isolate unique team dynamics across three distinct roles: **Coaches**, **Star Players**, and **Role Players**. This maps internal alignment and captures leadership stability vs. locker-room panic.
        *   **Multi-Season Historical Scaling:** The pipeline has been expanded to include other seasons (2019–2020 and 2021–2022) via an adaptive data-tiering approach, expanding historical baselines across completely different NBA eras.
        *   **Dual Hybrid Processing (Modern Seasons Only):** For the most recent high-density seasons, we introduced a generative **RAG Pipeline** to pull semantic source transcripts alongside a dedicated **Opponent Model** tracking matrix, evaluating both sides of a playoff series.
        *   **Sliding 400-Word Window Chunking:** Implements a chunking generator that steps across 100% of text files, protecting the 512-token ceiling of the local RoBERTa transformer without losing a single word.
        """)

    st.markdown("---")

    st.subheader("The Local Ingestion & Vector Pipeline Map")
    st.markdown("""
    1.  **Ingestion:** The system checks a global transcript cache to avoid hitting YouTube API rate limits. If automated captions are missing, `yt-dlp` captures raw audio streams and proxies them into a local `faster-whisper` CPU instance.
    2.  **Scoring Matrix:** The system loops through text slices using `SamLowe/roberta-base-go_emotions` to group 28 structural nuances into 7 composite sentiment dimensions: *Confidence, Contentment, Neutrality, Frustration, Upset, Anxiety, and Surprise*.
    3.  **Tabular Matrix Optimization:** Computes round-level and series-level weighted aggregates to train a Random Forest Classifier equipped with class-balancing hooks.
    """)

    example_img = "streamlit_app/assets/Knicks_sentiment_trajectory.png"
    if os.path.exists(example_img):
        st.image(example_img, caption="V2 Pipeline Output: Chronological Emotional Path Conversion.", use_container_width=True)

# Informational placeholders for other horizontal tabs to route users back to their respective files
for idx, tab_title in enumerate(["Introduction & Overview", "Multi-Role Analytics", "Interactive RAG Engine", "2026 Finals Live Predictor"]):
    # Match the mapping list to skip the 4th index cleanly
    target_idx = idx if idx < 4 else idx + 1
    with nav_tabs[idx if idx < 4 else idx]:
        if idx < 4:
            st.info(f"Navigate to the main menu page or the respective sub-file to view the full **{tab_title}** interface.")