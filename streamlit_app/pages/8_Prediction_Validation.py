import streamlit as st
import sys
import os

# --- BULLETPROOF ROUTING CORRECTION ---
STREAMLIT_APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if (STREAMLIT_APP_DIR not in sys.path):
    sys.path.append(STREAMLIT_APP_DIR)

PROJECT_ROOT_DIR = os.path.dirname(STREAMLIT_APP_DIR)
if (PROJECT_ROOT_DIR not in sys.path):
    sys.path.append(PROJECT_ROOT_DIR)

from utils.navigation import apply_global_styles, render_navigation

# Configure the page layout
st.set_page_config(
    page_title="Prediction Validation",
    layout="wide"
)

# Apply global background configurations and render navigation
apply_global_styles()
render_navigation()

# --- MAIN PAGE HEADER ---
st.title("Model Validation and Reflection")

st.write(
    "When building this project, I knew that fitting a model to historical data was only "
    "the first step. Testing the pipeline against a live event was the real goal, and seeing "
    "it hold up in real-time was a great learning experience."
)
st.markdown("---")

# --- AUDIT TRAIL & REFLECTION SECTION ---
col_audit, col_text = st.columns([1, 1.2])

with col_audit:
    st.markdown("### Version Control Timestamp")
    st.info(
        "To ensure transparency, the model's output was committed to this public repository "
        "before the NBA Finals concluded."
    )
    
    col_m1, col_m2 = st.columns(2)
    col_m1.metric(label="Logged Prediction", value="Knicks in 5")
    col_m2.metric(label="Commit Date", value="June 3, 2026") 
    
    st.markdown("**Version Control Hash:**")
    st.code("Commit ID: 4038067", language="bash")
    
    commit_url = "https://github.com/ishansinha5/NBA-Finals-Predictor-2026/commit/4038067"
    st.link_button("Verify Original Commit on GitHub", commit_url, type="primary")

with col_text:
    st.markdown("### The Prediction")
    st.write(
        "Before the Finals ended, the Targeted Modern Model processed the transcripts from the Conference Finals. "
        "It indicated that the New York Knicks had a measurable composure advantage over the San Antonio Spurs, "
        "pointing to a Knicks victory in 5 games."
    )
    
    st.markdown("### The Reflection")
    st.write(
        "What makes this outcome particularly meaningful to me is that it was not driven by hard stats. "
        "Most traditional predictive models rely heavily on box scores, true shooting percentages, and efficiency ratings. "
        "This pipeline took a different approach by evaluating 'softer' data—the emotional language and psychological "
        "state of the locker room. Watching the Knicks close out the series showed me that these intangible, human elements "
        "can actually be quantified and used as genuine indicators for success. Seeing a non-traditional approach hold up "
        "in a live scenario was an incredible learning milestone."
    )

st.markdown("---")
st.markdown("<h3 style='text-align: center; color: #F58426;'>NEW YORK KNICKS: 2026 NBA CHAMPIONS</h3>", unsafe_allow_html=True)