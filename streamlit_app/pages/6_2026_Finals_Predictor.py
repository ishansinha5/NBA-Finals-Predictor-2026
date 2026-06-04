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
    page_title="2026 Live Predictor",
    page_icon="🏀",
    layout="wide"
)

# Apply global background configurations and render our 7-column horizontal link row
apply_global_styles()
render_navigation()

# --- CUSTOM WIDGET CSS INJECTION ---
# I am copying the exact custom CSS form to keep the dropdowns and buttons locked to our opaque blue aesthetic
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
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Locate assets dynamically relative to our project structure root
ASSETS_DIR = os.path.join(PROJECT_ROOT_DIR, "streamlit_app", "assets")
LIVE_DIR = os.path.join(ASSETS_DIR, "live_2026")

# --- MAIN PAGE HEADER ---
st.title("2026 Live Conference Finals Tracker")

st.write(
    "This module maps the real-time emotional features extracted across the current active 2026 postseason. "
    "Unlike historical data sheets, gathering these transcripts required navigating unique broadcasting setups. "
    "While standard media files were easy to capture, the Spurs data forced us to route audio feeds into a local Whisper "
    "transcription loop due to restricted podium access, and the Knicks files required scraping high-density audio streams "
    "directly from local SNY channel broadcasts to separate teammate sound bites cleanly."
)
st.markdown("---")

# Main dropdown controller block
col_empty1, col_dropdown, col_empty2 = st.columns([1, 2, 1])
with col_dropdown:
    selected_track = st.selectbox(
        "Select Active Analysis Window",
        ["Western Conference Champion", "Eastern Conference Champion", "Championship Matchup Preview"],
        index=0
    )

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# WESTERN CONFERENCE TRACK
# ══════════════════════════════════════════════════════════════════════════════
if (selected_track == "Western Conference Champion"):
    
    st.markdown("## San Antonio Spurs — Championship Footprint")
    st.write(
        "Tracing the Spurs from the initial regular season blocks into the deep playoff rounds paints a picture "
        "of massive structural stability. Their regular season profiles showed a group testing tactical adjustments "
        "with considerable neutrality. Once the Western Conference Finals opened, their confidence lines flatlined "
        "at an exceptionally high tier, indicating a complete resistance to elimination volatility heading into the Finals."
    )
    
    st.markdown("### Regular Season Baseline Profiles")
    col_s_reg1, col_s_reg2 = st.columns(2)
    with col_s_reg1:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_aggregate_trajectory.png"), caption="Spurs Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_coach_trajectory.png"), caption="Spurs Regular Season Coach")
    with col_s_reg2:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_star_trajectory.png"), caption="Spurs Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_teammate_trajectory.png"), caption="Spurs Regular Season Teammates")
        
    st.markdown("### Postseason Trajectory Tracks")
    col_s_play1, col_s_play2 = st.columns(2)
    with col_s_play1:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_aggregate_trajectory.png"), caption="Spurs Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_coach_trajectory.png"), caption="Spurs Playoff Coach")
    with col_s_play2:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_star_trajectory.png"), caption="Spurs Playoff Star")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_teammate_trajectory.png"), caption="Spurs Playoff Teammates")

    st.markdown("---")
    
    # Nested dropdown to isolate the defeated opponent layer
    st.markdown("## Opponent Layer Isolation")
    st.write("Select the defeated western bracket opponent to compare baseline trajectory deltas:")
    
    opponent_select_w = st.selectbox("Select Defeated Opponent:", ["Oklahoma City Thunder"])
    
    st.markdown("### Oklahoma City Thunder — Defeated Opponent Tracking")
    st.write(
        "The Thunder entered the series with elite multi-role metrics, but our trajectory data picks up the "
        "exact moments their coverage layers began to fray. Frustration spikes appeared in the teammate "
        "layer during high-stakes away frames, disrupting the collective composure they relied on in previous series."
    )
    
    col_t_reg1, col_t_reg2 = st.columns(2)
    with col_t_reg1:
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_aggregate_trajectory.png"), caption="Thunder Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_coach_trajectory.png"), caption="Thunder Regular Season Coach")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_aggregate_trajectory.png"), caption="Thunder Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_coach_trajectory.png"), caption="Thunder Playoff Coach")
    with col_t_reg2:
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_star_trajectory.png"), caption="Thunder Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_teammate_trajectory.png"), caption="Thunder Regular Season Teammates")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_star_trajectory.png"), caption="Thunder Playoff Star")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_teammate_trajectory.png"), caption="Thunder Playoff Teammates")

    st.markdown("---")
    
    st.markdown("## Western Conference Finals — Head-to-Head Comparison")
    st.write(
        "Analyzing the composite mean bar arrays over the full Western path reveals a razor-thin margin. "
        "While confidence metrics remained comparable across both star tracking rows, San Antonio's coach "
        "composure score showed slightly cleaner neutrality margins over the full series average."
    )
    
    col_wcf1, col_wcf2 = st.columns(2)
    with col_wcf1:
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_aggregate_comparison_bar.png"), caption="WCF Aggregate Profile")
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_coach_comparison_bar.png"), caption="WCF Coach Profile")
    with col_wcf2:
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_star_comparison_bar.png"), caption="WCF Star Profile")
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_teammate_comparison_bar.png"), caption="WCF Teammate Profile")

# ══════════════════════════════════════════════════════════════════════════════
# EASTERN CONFERENCE TRACK
# ══════════════════════════════════════════════════════════════════════════════
elif (selected_track == "Eastern Conference Champion"):
    
    st.markdown("## New York Knicks — Championship Footprint")
    st.write(
        "The Knicks processed their postseason path with an intense, grinding accountability profile. "
        "Their regular season data reflected high, volatile frustration metrics during rotational adjustments, "
        "but their playoff trajectory reveals a group that unified its communication channels completely. "
        "Brunson's star track and the teammate layer are highly aligned, showing steady confidence entering the Finals."
    )
    
    st.markdown("### Regular Season Baseline Profiles")
    col_k_reg1, col_k_reg2 = st.columns(2)
    with col_k_reg1:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_aggregate_trajectory.png"), caption="Knicks Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_coach_trajectory.png"), caption="Knicks Regular Season Coach")
    with col_k_reg2:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_star_trajectory.png"), caption="Knicks Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_teammate_trajectory.png"), caption="Knicks Regular Season Teammates")
        
    st.markdown("### Postseason Trajectory Tracks")
    col_k_play1, col_k_play2 = st.columns(2)
    with col_k_play1:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_aggregate_trajectory.png"), caption="Knicks Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_coach_trajectory.png"), caption="Knicks Playoff Coach")
    with col_k_play2:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_star_trajectory.png"), caption="Knicks Playoff Star")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_teammate_trajectory.png"), caption="Knicks Playoff Teammates")

    st.markdown("---")
    
    st.markdown("## Opponent Layer Isolation")
    st.write("Select the defeated eastern bracket opponent to compare baseline trajectory deltas:")
    
    opponent_select_e = st.selectbox("Select Defeated Opponent:", ["Cleveland Cavaliers"])
    
    st.markdown("### Cleveland Cavaliers — Defeated Opponent Tracking")
    st.write(
        "Cleveland maintained strong baseline metrics throughout the year, but their trajectory profile "
        "cracked under the intensity of New York's point-of-attack spacing pressure. Anxiety tracking rose "
        "sharply across their supporting teammate arrays as elimination frames loomed."
    )
    
    col_c_reg1, col_c_reg2 = st.columns(2)
    with col_c_reg1:
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_aggregate_trajectory.png"), caption="Cavs Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_coach_trajectory.png"), caption="Cavs Regular Season Coach")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_aggregate_trajectory.png"), caption="Cavs Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_coach_trajectory.png"), caption="Cavs Playoff Coach")
    with col_c_reg2:
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_star_trajectory.png"), caption="Cavs Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_teammate_trajectory.png"), caption="Cavs Regular Season Teammates")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_star_trajectory.png"), caption="Cavs Playoff Star")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_teammate_trajectory.png"), caption="Cavs Playoff Teammates")

    st.markdown("---")
    
    st.markdown("## Eastern Conference Finals — Head-to-Head Comparison")
    st.write(
        "The composite Eastern averages emphasize the defensive grit of the series. New York's teammate "
        "layer held lower average upset values, illustrating their ability to process physical containment "
        "without sacrificing core alignment metrics."
    )
    
    col_ecf1, col_ecf2 = st.columns(2)
    with col_ecf1:
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_aggregate_comparison_bar.png"), caption="ECF Aggregate Profile")
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_coach_comparison_bar.png"), caption="WCF Coach Profile")
    with col_ecf2:
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_star_comparison_bar.png"), caption="WCF Star Profile")
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_teammate_comparison_bar.png"), caption="WCF Teammate Profile")

# ══════════════════════════════════════════════════════════════════════════════
# COMBINED FINALS PREVIEW TRACK
# ══════════════════════════════════════════════════════════════════════════════
elif (selected_track == "Championship Matchup Preview"):
    
    st.markdown("## 2026 NBA Finals — Head-to-Head Pre-Matchup Matrix")
    st.write(
        "Here, we align the final combined emotional profiles of our two conference champions directly against "
        "each other. We map their baseline traits across all key semantic dimensions — evaluating coach composure, "
        "star stability, and teammate chemistry averages over the entirety of the postseason. "
        "We do not establish a mathematical conclusion or declare a definitive winner on this screen; the full "
        "predictive classification breakdown and final winner prediction are housed explicitly on the Matchup page."
    )
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_aggregate_comparison_bar.png"), caption="Championship Aggregate Matrix")
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_coach_comparison_bar.png"), caption="Championship Coaching Matrix")
    with col_p2:
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_star_comparison_bar.png"), caption="Championship Star Matrix")
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_teammate_comparison_bar.png"), caption="Championship Teammate Matrix")