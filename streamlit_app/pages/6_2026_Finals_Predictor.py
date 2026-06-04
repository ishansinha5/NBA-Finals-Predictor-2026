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
st.title("2026 Live Conference Finals Tracker")

st.write(
    "This page tracks the real-time emotional features we extracted across the current 2026 postseason run. "
    "To be honest, gathering these transcripts was a bit of a headache compared to the historical datasets. "
    "The Spurs data forced us to route audio feeds into a local Whisper loop because podium access was locked down, "
    "and for the Knicks, we had to scrape audio straight from the local SNY channel broadcasts to isolate the teammate quotes."
)
st.markdown("---")

# Main selector dropdown 
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
    
    st.markdown("## San Antonio Spurs")
    
    st.markdown("#### Regular Season Baseline")
    col_s_reg1, col_s_reg2 = st.columns(2)
    with col_s_reg1:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_aggregate_trajectory.png"), caption="Spurs Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_coach_trajectory.png"), caption="Spurs Regular Season Coach")
    with col_s_reg2:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_star_trajectory.png"), caption="Spurs Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_reg_teammate_trajectory.png"), caption="Spurs Regular Season Teammates")
        
    st.write(
        "Looking at the aggregate, the regular season was basically a playground for testing lines, keeping a super chill, high-neutrality vibe. "
        "Popovich was entirely in teaching mode, keeping his frustration levels flatlined even when bench rotations got messy. "
        "Wembanyama's star profile showed massive composure numbers while he was still figuring out his structural spacing footprint."
    )
        
    st.markdown("#### Playoff Run")
    col_s_play1, col_s_play2 = st.columns(2)
    with col_s_play1:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_aggregate_trajectory.png"), caption="Spurs Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_coach_trajectory.png"), caption="Spurs Playoff Coach")
    with col_s_play2:
        st.image(os.path.join(LIVE_DIR, "spurs_2025_star_trajectory.png"), caption="Spurs Playoff Star")
        st.image(os.path.join(LIVE_DIR, "spurs_2025_teammate_trajectory.png"), caption="Spurs Playoff Teammates")

    st.write(
        "The team aggregate completely stabilized the second the playoffs started, pinning their confidence near the absolute ceiling. "
        "Wemby completely dominated the media room too, channeling high contentment and zero anxiety as the lights got brighter. "
        "The supporting teammates completely mirrored that confidence curve, showing they weren't rattled by hostile road crowds. "
        "Popovich anchored everything with masterful poise, matching the exact flatline composure of our historical baseline champions."
    )

    st.markdown("---")
    
    st.markdown("## Oklahoma City Thunder")
    
    st.markdown("#### Regular Season Baseline")
    col_t_reg1, col_t_reg2 = st.columns(2)
    with col_t_reg1:
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_aggregate_trajectory.png"), caption="Thunder Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_coach_trajectory.png"), caption="Thunder Regular Season Coach")
    with col_t_reg2:
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_star_trajectory.png"), caption="Thunder Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_reg_teammate_trajectory.png"), caption="Thunder Regular Season Teammates")

    st.write(
        "On an aggregate level, OKC's regular season numbers look incredibly elite, showing a super unified, high-confidence blueprint. "
        "Mark Daigneault was completely dialed into the data, keeping a remarkably stable podium profile across all matchups. "
        "Shai's individual star profile was the anchor, showcasing immense poise and high neutrality week after week."
    )

    st.markdown("#### Playoff Run")
    col_t_play1, col_t_play2 = st.columns(2)
    with col_t_play1:
        st.image(os.path.join(LIVE_DIR, "thunder_2025_aggregate_trajectory.png"), caption="Thunder Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_coach_trajectory.png"), caption="Thunder Playoff Coach")
    with col_t_play2:
        st.image(os.path.join(LIVE_DIR, "thunder_2025_star_trajectory.png"), caption="Thunder Playoff Star")
        st.image(os.path.join(LIVE_DIR, "thunder_2025_teammate_trajectory.png"), caption="Thunder Playoff Teammates")

    st.write(
        "The playoff aggregate shows their baseline confidence was soaring high but started carrying a bit more volatile emotion. "
        "SGA kept his composure entirely flat, trusting his film study and shrugging off the aggressive defensive blitzes. "
        "However, the supporting teammate layer started showing some cracks, with anxiety metrics creeping up during tough road games. "
        "Daigneault stayed as solid as ever at the podium, but you could tell the structural spacing strain was testing the system."
    )

    st.markdown("---")
    
    st.markdown("## Western Conference Finals Matchup Analysis")
    col_wcf1, col_wcf2 = st.columns(2)
    with col_wcf1:
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_aggregate_comparison_bar.png"), caption="WCF Aggregate Profile")
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_coach_comparison_bar.png"), caption="WCF Coach Profile")
    with col_wcf2:
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_star_comparison_bar.png"), caption="WCF Star Profile")
        st.image(os.path.join(LIVE_DIR, "wcf_matchup_2025_teammate_comparison_bar.png"), caption="WCF Teammate Profile")

    st.write(
        "For the coaches, Popovich edged out Daigneault by keeping a slightly more composed, low-frustration profile under pressure. "
        "Looking at the stars, SGA and Wemby were almost neck-and-neck emotionally, both showcasing elite championship-level poise. "
        "The real gap showed up in the teammate bar charts, where San Antonio's supporting cast held much lower anxiety averages. "
        "On an aggregate level, the Spurs simply sustained a flatter, more stable emotional floor throughout the grueling series. "
        "San Antonio took the series because their role players completely absorbed the defensive physical strain without breaking their mental alignment."
    )

# ══════════════════════════════════════════════════════════════════════════════
# EASTERN CONFERENCE TRACK
# ══════════════════════════════════════════════════════════════════════════════
elif (selected_track == "Eastern Conference Champion"):
    
    st.markdown("## New York Knicks")
    
    st.markdown("#### Regular Season Baseline")
    col_k_reg1, col_k_reg2 = st.columns(2)
    with col_k_reg1:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_aggregate_trajectory.png"), caption="Knicks Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_coach_trajectory.png"), caption="Knicks Regular Season Coach")
    with col_k_reg2:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_star_trajectory.png"), caption="Knicks Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_reg_teammate_trajectory.png"), caption="Knicks Regular Season Teammates")
        
    st.write(
        "In the regular season, the team aggregate was an absolute rollercoaster of high frustration and intense grinding energy. "
        "Coach Thibodeau was clearly pushing his guys hard, showing massive frustration spikes during rough rotational stretches. "
        "Brunson's star track was the saving grace, displaying massive accountability metrics and holding things together by sheer force of will."
    )
        
    st.markdown("#### Playoff Run")
    col_k_play1, col_k_play2 = st.columns(2)
    with col_k_play1:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_aggregate_trajectory.png"), caption="Knicks Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_coach_trajectory.png"), caption="Knicks Playoff Coach")
    with col_k_play2:
        st.image(os.path.join(LIVE_DIR, "knicks_2025_star_trajectory.png"), caption="Knicks Playoff Star")
        st.image(os.path.join(LIVE_DIR, "knicks_2025_teammate_trajectory.png"), caption="Knicks Playoff Teammates")

    st.write(
        "The moment the playoffs kicked off, the team aggregate completely locked in and stabilized around an intense, focused baseline. "
        "Jalen Brunson operated at an absolute superstar level of composure, filtering out the media noise and pacing the offense perfectly. "
        "The supporting teammates fed directly off that energy, showing an unbelievable level of defensive grit and alignment. "
        "Thibs still had his classic intense podium moments, but his baseline metrics shifted from pure frustration to controlled confidence."
    )

    st.markdown("---")
    
    st.markdown("## Cleveland Cavaliers")
    
    st.markdown("#### Regular Season Baseline")
    col_c_reg1, col_c_reg2 = st.columns(2)
    with col_c_reg1:
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_aggregate_trajectory.png"), caption="Cavs Regular Season Aggregate")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_coach_trajectory.png"), caption="Cavs Regular Season Coach")
    with col_c_reg2:
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_star_trajectory.png"), caption="Cavs Regular Season Star")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_reg_teammate_trajectory.png"), caption="Cavs Regular Season Teammates")

    st.write(
        "Across the regular season, the Cavs' aggregate metrics showed a really solid, quietly confident team floating through the bracket. "
        "The coaching staff kept a steady, business-like profile, maintaining clean composure readings across most home matchups. "
        "Their star layer showcased massive confidence peaks, proving they could control the game pace when their rhythm was unbothered."
    )

    st.markdown("#### Playoff Run")
    col_c_play1, col_c_play2 = st.columns(2)
    with col_c_play1:
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_aggregate_trajectory.png"), caption="Cavs Playoff Aggregate")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_coach_trajectory.png"), caption="Cavs Playoff Coach")
    with col_c_play2:
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_star_trajectory.png"), caption="Cavs Playoff Star")
        st.image(os.path.join(LIVE_DIR, "cavaliers_2025_teammate_trajectory.png"), caption="Cavs Playoff Teammates")

    st.write(
        "The playoff aggregate shows a team that started the postseason strong but began to visually waver under heavy physical pressure. "
        "Their star player kept fighting and held up his confidence readings well, but the external scoring load was clearly mounting. "
        "The teammate layer is where things got really shaky, showing steep spikes in anxiety as the defensive clamps tightened. "
        "The coaching staff's frustration readings began to climb with every game as their standard rotational answers stopped working."
    )

    st.markdown("---")
    
    st.markdown("## Eastern Conference Finals Matchup Analysis")
    col_ecf1, col_ecf2 = st.columns(2)
    with col_ecf1:
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_aggregate_comparison_bar.png"), caption="ECF Aggregate Profile")
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_coach_comparison_bar.png"), caption="ECF Coach Profile")
    with col_ecf2:
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_star_comparison_bar.png"), caption="ECF Star Profile")
        st.image(os.path.join(LIVE_DIR, "ecf_matchup_2025_teammate_comparison_bar.png"), caption="ECF Teammate Profile")

    st.write(
        "At the podium, the Knicks' coaching staff managed to channel their intensity into cleaner, more controlled confidence scores. "
        "For the franchise stars, Jalen Brunson displayed an elite edge in composure, keeping his emotional line completely flat. "
        "The teammate comparison chart shows the Cavs' supporting cast letting anxiety and upset readings bleed heavily into their profiles. "
        "Looking at the overall aggregate averages, New York simply maintained a much more unified, mentally resilient floor. "
        "The Knicks advanced because their entire roster completely embraced the physical grit required to execute under high-pressure parameters."
    )

# ══════════════════════════════════════════════════════════════════════════════
# COMBINED FINALS PREVIEW TRACK
# ══════════════════════════════════════════════════════════════════════════════
elif (selected_track == "Championship Matchup Preview"):
    
    st.markdown("## 2026 NBA Finals — Head-to-Head Pre-Matchup Matrix")
    st.write(
        "Here, we align the final combined emotional profiles of our two conference champions directly against "
        "each other. We map their baseline traits across all key semantic dimensions — evaluating coach composure, "
        "star stability, and teammate chemistry averages over the entirety of the postseason. "
        "Want to know who the model thinks wins? Go to the Matchup page."
    )
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_aggregate_comparison_bar.png"), caption="Championship Aggregate Matrix")
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_coach_comparison_bar.png"), caption="Championship Coaching Matrix")
    with col_p2:
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_star_comparison_bar.png"), caption="Championship Star Matrix")
        st.image(os.path.join(LIVE_DIR, "combined_pre_matchup_2025_teammate_comparison_bar.png"), caption="Championship Teammate Matrix")