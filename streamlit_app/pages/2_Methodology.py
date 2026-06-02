import streamlit as st
import os

st.set_page_config(page_title="Design Journey & Methodology", page_icon="🏀", layout="wide")

st.title("The Architectural Evolution: V1 vs. V2")
st.subheader("Engineering Around Survival Bias, Context Caps, and Sparse Data Tracks")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Legacy V1 Paradigm (The Baseline Proof-of-Concept)")
    st.markdown("""
    *   **Data Footprint:** Evaluated only 2 years of high-density data (2024 and 2025 Finals runs).
    *   **Linguistic Truncation:** Used basic hard-truncation at 2,500 characters. This frequently blind-sided the model on late press conference adjustments.
    *   **Tabular Blind Spot:** Lacked granular multi-role separation—averaging teams together in a broad bucket.
    *   **The Survival Bias Flaw:** By only training on teams that reached the Finals, the machine never learned what an early-round exit looked like. It could not accurately evaluate first-round panic.
    """)

with col2:
    st.markdown("### Upgraded V2 Framework (The Production Pipeline)")
    st.markdown("""
    *   **The Tiered Manifest System:** Introduces an adaptive data parsing strategy. Isolates **The Champion's Path** for scarce historical eras (2020, 2021) while deploying full-bracket traces for modern eras.
    *   **Sliding 400-Word Window Chunking:** Implements a chunking generator that steps across 100% of the text file. Protects the 512-token ceiling of the RoBERTa model without losing a single word.
    *   **28-Column Role-Isolated Matrix:** Flattens metrics independently across **Coach, Star, and Teammate**, utilizing automated team aggregate fallbacks for historical data holes.
    *   **Generative Context Augmentation:** Complements traditional predictive tabular metrics with a vector-indexed retrieval system to parse exact presser quotes.
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