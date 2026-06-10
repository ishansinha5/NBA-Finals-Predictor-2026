import streamlit as st
import sys
import os

# --- BULLETPROOF ROUTING CORRECTION ---
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if (ROOT_DIR not in sys.path):
    sys.path.append(ROOT_DIR)

from utils.navigation import apply_global_styles, render_navigation

st.set_page_config(
    page_title="Historical Baselines", 
    page_icon="🏀", 
    layout="wide"
)

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
    ul[data-baseweb="menu"] {
        background-color: rgba(11, 26, 48, 0.95) !important;
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

    /* Disable typing in the selectbox */
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        pointer-events: none !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# --- HARDCODED ASSET PATHS ---
ASSETS = os.path.join(ROOT_DIR, "assets")
HIST   = os.path.join(ASSETS, "historical")

# --- MAIN PAGE CONTENT ---
st.title("Historical Championship Baselines")

st.write(
    "To figure out what a championship team actually sounds like, I scraped the post-game press conferences "
    "of the 2020, 2021, and 2022 NBA Champions. The older transcripts were a bit sparse and full of gaps, "
    "so I used linear imputation to fill out the timeline and keep the visual trajectories continuous. "
    "It's not a perfect dataset, but it gives us a really solid psychological baseline of how a team "
    "communicates when they are on a deep title run."
)
st.markdown("---")

# --- DATA DICTIONARY ---
teams_data = {
    "2019-2020 Los Angeles Lakers": {
        "prefix": "lakers_2019",
        "logo": "Los_Angeles_Lakers_lo.go.png",
        "analysis": "The 2020 Lakers operated with a heavy, veteran, business-like demeanor inside the Orlando bubble. Their aggregate mindset remained remarkably flat and content, showing almost zero panic even after dropping early series games. Frank Vogel's coach trajectory reflects a steady, unwavering trust in his game plan without letting frustration spike. LeBron James, as the star, commanded the media room with intense neutrality and confidence, absorbing all the external pressure. The teammates followed suit, mirroring that flat emotional line and completely suppressing anxiety to close out the championship run."
    },
    "2020-2021 Milwaukee Bucks": {
        "prefix": "bucks_2020",
        "logo": "Milwaukee_Bucks_logo.png",
        "analysis": "The 2021 Bucks played with a resilient, down-to-earth joy that helped them bounce back from deep series deficits. Their aggregate momentum reveals a team that absorbed early frustration but channeled it directly into rising confidence. Mike Budenholzer kept his emotional profile completely steady, anchoring the team when the media doubted their half-court execution. Giannis Antetokounmpo was the absolute emotional battery, displaying massive spikes of contentment and zero anxiety as the stakes got higher. The supporting teammates matched this energy, steadily growing more confident as they learned how to win on the biggest stage."
    },
    "2021-2022 Golden State Warriors": {
        "prefix": "warriors_2021",
        "logo": "Golden-State-Warriors-logo.png",
        "analysis": "The 2022 Warriors brought a youthful, loose, and incredibly confident swagger to their redemption tour. Looking at their aggregate lines, they maintained an exceptionally high baseline of contentment and neutrality, completely brushing off the ghosts of past injuries. Steve Kerr's podium presence was masterful, showing minimal frustration and massive trust in his system. Stephen Curry's star trajectory is a clinic in emotional stability, showing pure confidence while letting the noise slide right off him. The teammates, a mix of the old core and new blood, bought in entirely, keeping anxiety flatlined and letting their championship pedigree take over."
    }
}

col_empty1, col_dropdown, col_empty2 = st.columns([1, 2, 1])
with col_dropdown:
    selected_team = st.selectbox("Select Championship Roster", list(teams_data.keys()), index=0)

st.markdown("<br>", unsafe_allow_html=True)

# --- LOGO & ANALYSIS LAYOUT ---
col_logo, col_text = st.columns([1, 5])
current_meta = teams_data[selected_team]

with col_logo:
    st.image(os.path.join(ASSETS, current_meta["logo"]), width=140)

with col_text:
    st.write(current_meta["analysis"])

st.markdown("---")
st.markdown("### Series Emotional Trajectories")

col1, col2 = st.columns(2)
pfx = current_meta["prefix"]

# BUGFIX CORRECTIONS: Dynamically align string pointers with structural short_year filename shifts
with col1:
    st.image(os.path.join(HIST, f"{pfx}_aggregate_trajectory.png"), caption="Team Aggregate Momentum")
    st.image(os.path.join(HIST, f"{pfx}_coach_trajectory.png"),     caption="Head Coach Momentum")
with col2:
    st.image(os.path.join(HIST, f"{pfx}_star_trajectory.png"),      caption="Franchise Star Momentum")
    st.image(os.path.join(HIST, f"{pfx}_teammate_trajectory.png"),  caption="Supporting Teammates Momentum")