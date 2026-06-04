import streamlit as st
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if (ROOT_DIR not in sys.path):
    sys.path.append(ROOT_DIR)

from utils.navigation import apply_global_styles, render_navigation

st.set_page_config(
    page_title="Design Journey", 
    page_icon="🏀", 
    layout="wide"
)

apply_global_styles()
render_navigation()

st.title("🏀 Engineering Journey: Decoding Championship Psychology")
st.markdown("### The Architectural Evolution: V1 vs. V2")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Legacy V1 Paradigm: Proof of Concept")
    st.write(
        "Our original prototype laid down the foundation for language-aware basketball analytics, "
        "but it operated under sharp structural limitations that masked true roster psychology."
    )
    
    st.markdown("""
    * **Restricted Data Matrix:** Evaluated only a narrow, two-year footprint of data.
    * **Linguistic Truncation:** Used hard token clipping, which dropped critical context mid-sentence.
    * **Tabular Blind Spot:** Lacked granular multi-role separation, averaging out all voices into one number.
    * **Survival Bias:** Only trained on deep Finals runs, completely missing early-exit locker room panic.
    """)

with col2:
    st.markdown("### Upgraded V2 Framework: Production Pipeline")
    st.write(
        "The current production version refines our feature extraction pipeline, expanding "
        "our computational footprints to model complete organizational stability."
    )
    
    st.markdown("""
    * **Preservation of the Score Filter Boundary:** I intentionally stop collecting transcript data exactly one game before a playoff series is decided. This prevents the anomalous emotional spikes inherent in series-clinching celebrations from skewing our training baselines.
    * **Tri-Tier Role Isolation:** The feature matrix cleanly isolates roster sub-dynamics across three separate perspectives: head coaches, franchise stars, and supporting teammates.
    * **Multi-Season Scaling:** The data pipeline steps backwards into historical playoff arcs to broaden our classification profiles.
    * **Deterministic Verification Layer:** Rejects heavy, paywalled commercial cloud endpoints in favor of an optimized local evidence block array, matching our commitment to Green AI principles while perfectly simulating our offline RAG pipeline.
    """)

st.markdown("---")

st.markdown("### Dual Classifier Modeling Optimization")
st.write(
    "To provide deeper comparative resolution, the system evaluates live series inputs through two distinct "
    "Random Forest classifier architectures trained on different historical contexts:"
)

col3, col4 = st.columns(2)
with col3:
    st.markdown("#### Model 1: Full Baseline Engine")
    st.write(
        "Trained on our complete multi-era repository spanning older playoff arcs back to 2020. "
        "This model evaluates macro trends over a broader historical footprint, establishing conservative "
        "weights that account for structural shifts across different eras of post-game media management."
    )

with col4:
    st.markdown("#### Model 2: Modern Era Optimized Engine")
    st.write(
        "Trained exclusively on high-density data sheets from the recent 2024 and 2025 seasons. By evaluating "
        "environments where every conference final team and corresponding opponent tracking arrays were entirely populated, "
        "this model picks up on modern player-media dynamics and sharp confidence deltas."
    )

st.markdown("---")
st.write(
    "Note: For an atomic, line-by-line breakdown of the underlying data-scraping parameters, "
    "tokenization algorithms, and random forest tuning weights, please refer to the primary repository documentation."
)