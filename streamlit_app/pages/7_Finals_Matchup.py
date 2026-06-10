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

# Configure the page layout and strictly collapse the vertical sidebar navigation
st.set_page_config(
    page_title="Finals Matchup Preview",
    page_icon="🏀",
    layout="wide"
)

# Apply global background configurations and render our horizontal link row
apply_global_styles()
render_navigation()

# --- CUSTOM WIDGET CSS INJECTION ---
custom_css = """
<style>
    .stSelectbox label {
        display: flex !important;
        justify-content: center !important;
        font-size: 1.1rem !important;
        padding-bottom: 8px !important;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(11, 26, 48, 0.95) !important;
        border: 1px solid #1f3a5f !important;
        color: white !important;
        border-radius: 6px;
    }
    div[data-baseweb="select"] > div > div > div {
        text-align: center !important;
        justify-content: center !important;
    }
    div[data-baseweb="popover"] > div, ul[data-baseweb="menu"] {
        background-color: rgba(11, 26, 48, 0.98) !important;
        border: 1px solid #1f3a5f !important;
    }
    li[data-baseweb="menu-item"] {
        color: white !important;
        text-align: center !important;
        justify-content: center !important;
    }
    li[data-baseweb="menu-item"]:hover {
        background-color: #1f3a5f !important;
    }
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        pointer-events: none !important;
    }
    
    /* Expander icon fix to stop raw text string overrides */
    span.stIconMaterial, 
    span[data-testid="stIconMaterial"], 
    .material-symbols-rounded {
        font-family: 'Material Symbols Rounded' !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Locate assets dynamically relative to our project structure root
ASSETS_DIR = os.path.join(PROJECT_ROOT_DIR, "streamlit_app", "assets")
LIVE_DIR = os.path.join(ASSETS_DIR, "live_2026")

# --- MAIN PAGE HEADER ---
st.title("The Ultimate 2026 Finals Prediction: Spurs vs. Knicks")

st.write(
    "To build the most balanced prediction engine possible, I trained two separate Random Forest architectures on our post-game data tracking. "
    "The Full Baseline Model looks at all available eras in our dataset to maximize the training sample size and historical depth, "
    "whereas the Targeted Modern Baseline limits its scope entirely to the 2023–2025 seasons to map current play styles and roster structures. "
    "While the full historical track adds amazing volume, the modern era version is significantly more thorough and accurate because it prevents "
    "outdated coaching styles and standard 1990s media room patterns from skewing how the model scores emotional features today."
)
st.markdown("---")

# Main selector dropdown 
col_empty1, col_dropdown, col_empty2 = st.columns([1, 2, 1])
with col_dropdown:
    selected_model = st.selectbox(
        "Select Active Predictive Pipeline Model",
        ["Full Baseline Model (All Eras)", "Modern Era Model (2023-2025)"],
        index=1  # Default to our highly accurate Targeted Modern model
    )

st.markdown("<br>", unsafe_allow_html=True)

# --- DYNAMIC REPORT EXTRACTION LOGIC ---
games_count = "5"
blurb = "Loading analysis data..."

report_path = os.path.join(PROJECT_ROOT_DIR, "output", "predictions", "2026_Finals_Report.md")
if os.path.exists(report_path):
    with open(report_path, "r") as f:
        report_content = f.read()
        
    # Parse the markdown dynamically based on the selected model name
    sections = report_content.split("## ")
    for sec in sections:
        if sec.startswith(selected_model):
            for line in sec.split('\n'):
                # Extract the dynamic number of games
                if "**Predicted Champion:**" in line:
                    for word in line.split():
                        if word.isdigit():
                            games_count = word
                            break
                # Extract the dynamic model rationale
                if "**Analytical Blurb:**" in line:
                    blurb = line.replace("**Analytical Blurb:**", "").strip()
else:
    blurb = "Warning: 2026_Finals_Report.md missing. Run scripts/predict_finals.py locally to generate inferences."

# --- DISPLAY DYNAMIC CHAMPIONSHIP CONTAINER ---
st.markdown(f"<p style='text-align: center; font-size: 1.4rem; font-weight: bold;'>The {selected_model} model says the winner of the 2026 NBA Finals is...</p>", unsafe_allow_html=True)

# Display giant New York Knicks logo centrally
col_logo_l, col_logo_c, col_logo_r = st.columns([1, 1, 1])
with col_logo_c:
    knicks_logo_path = os.path.join(ASSETS_DIR, "New-York-Knicks-logo.png")
    if (os.path.exists(knicks_logo_path) == True):
        st.image(knicks_logo_path, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #F58426; font-size: 4rem;'>NEW YORK KNICKS</h1>", unsafe_allow_html=True)

st.markdown(f"<h1 style='text-align: center; font-size: 3.5rem;'>In {games_count} games!</h1>", unsafe_allow_html=True)

col_b_l, col_b_c, col_b_r = st.columns([1, 3, 1])
with col_b_c:
    st.write(blurb)

st.markdown("---")

# --- COMPARATIVE HEAD-TO-HEAD MATRIX VISUALS ---
st.markdown("### Head-to-Head Pre-Matchup Visual Matrix")

col_img1, col_img2 = st.columns(2)
with col_img1:
    st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_aggregate_comparison_bar.png"), caption="Championship Aggregate Matrix")
    st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_coach_comparison_bar.png"), caption="Championship Coaching Matrix")
with col_img2:
    st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_star_comparison_bar.png"), caption="Championship Star Matrix")
    st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_teammate_comparison_bar.png"), caption="Championship Teammate Matrix")