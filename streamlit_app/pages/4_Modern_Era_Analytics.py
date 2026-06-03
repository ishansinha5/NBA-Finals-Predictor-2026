import streamlit as st
import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from utils.navigation import apply_global_styles, render_navigation

st.set_page_config(
    page_title="Modern Era Analytics",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        pointer-events: none !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

ASSETS = os.path.join(ROOT_DIR, "assets")
HIST   = os.path.join(ASSETS, "historical")

# --- MAIN PAGE CONTENT ---
st.title("Modern Era Deep Analytics")

st.write(
    "In this modern tracking era, we expanded our data footprint to capture both the champion and runner-up "
    "trajectories across full playoff runs. Every team in this archive maintained clean, complete transcript "
    "coverage throughout their postseason, allowing us to build dense emotional profiles across all four roster "
    "layers without any imputation. This lets us pinpoint the exact moments opponents began to crack under "
    "playoff pressure and compare them directly against the championship baseline."
)
st.markdown("---")

col_empty1, col_dropdown, col_empty2 = st.columns([1, 2, 1])
with col_dropdown:
    selected_season = st.selectbox(
        "Select Modern Data Archive",
        ["2023-2024 Boston Celtics", "2024-2025 Oklahoma City Thunder"],
        index=0
    )

st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# 2023-2024 CELTICS SEASON
# ══════════════════════════════════════════════════════════════════════════════
if selected_season == "2023-2024 Boston Celtics":

    # --- SECTION 1: CHAMPION ---
    col_logo, col_text = st.columns([1, 5])
    with col_logo:
        st.image(os.path.join(ASSETS, "Boston-Celtics-logo.png"), width=140)
    with col_text:
        st.markdown("### 2023-2024 Boston Celtics — Championship Run")
        st.write(
            "What stood out most to me about the 2024 Celtics was how boring their emotional data looked — "
            "and I mean that as a compliment. Their aggregate confidence stayed high and flat the whole way "
            "through, which is pretty rare across a full playoff run. Mazzulla kept a really steady podium "
            "presence; even in the tighter series moments the frustration readings barely budged. Tatum's "
            "star profile was similarly calm — not flashy, just consistent. The teammate layer is honestly "
            "what surprised me most; the supporting guys held their composure better than I expected, which "
            "I think is a big reason they were able to close it out."
        )

    st.markdown("#### Champion Emotional Trajectories")
    col1, col2 = st.columns(2)
    with col1:
        st.image(os.path.join(HIST, "celtics_2023_aggregate_trajectory.png"),  caption="Team Aggregate Momentum")
        st.image(os.path.join(HIST, "celtics_2023_coach_trajectory.png"),      caption="Head Coach Momentum")
    with col2:
        st.image(os.path.join(HIST, "celtics_2023_star_trajectory.png"),       caption="Franchise Star Momentum")
        st.image(os.path.join(HIST, "celtics_2023_teammate_trajectory.png"),   caption="Supporting Teammates Momentum")

    st.markdown("---")

    # --- SECTION 2: RUNNER-UP ---
    col_logo2, col_text2 = st.columns([1, 5])
    with col_logo2:
        st.image(os.path.join(ASSETS, "Dallas-Mavericks-Logo.png"), width=140)
    with col_text2:
        st.markdown("### 2023-2024 Dallas Mavericks — Runner-Up Arc")
        st.write(
            "The Mavericks data was genuinely interesting to dig through. Luka drove a real confidence spike "
            "through the early rounds and the conference finals run looked legitimately championship-caliber "
            "on paper. But once the Finals started, you can see anxiety creep into the teammate layer in a "
            "way that just wasn't there earlier. Kidd's coaching readings also got noticeably more frustrated "
            "as the series went on — the gap between his profile and Mazzulla's widened every game. I don't "
            "think Dallas was outmatched talent-wise, but the emotional data suggests the pressure of the "
            "moment got to the supporting pieces before it got to Boston."
        )

    st.markdown("#### Runner-Up Emotional Trajectories")
    col3, col4 = st.columns(2)
    with col3:
        st.image(os.path.join(HIST, "mavericks_2023_aggregate_trajectory.png"), caption="Team Aggregate Momentum")
        st.image(os.path.join(HIST, "mavericks_2023_coach_trajectory.png"),     caption="Head Coach Momentum")
    with col4:
        st.image(os.path.join(HIST, "mavericks_2023_star_trajectory.png"),      caption="Franchise Star Momentum")
        st.image(os.path.join(HIST, "mavericks_2023_teammate_trajectory.png"),  caption="Supporting Teammates Momentum")

    st.markdown("---")

    # --- SECTION 3: FINALS COMBINED ---
    st.markdown("### 2024 Finals — Head-to-Head Emotional Comparison")
    st.write(
        "Putting both teams side by side is where it gets clearest. Boston just held a more stable floor "
        "across almost every category — it wasn't a blowout difference, but it was consistent. The teammate "
        "comparison is probably the most telling chart here; Dallas's supporting cast had higher surprise and "
        "anxiety readings than Boston's, which tracks with how the series felt to watch. The coach bar chart "
        "is interesting too — both coaches showed similar confidence levels, but Kidd's frustration reading "
        "came out noticeably higher across the full series average."
    )
    col5, col6 = st.columns(2)
    with col5:
        agg_path = os.path.join(HIST, "CeltMavs_2023_aggregate_comparison_bar.png")
        coach_path = os.path.join(HIST, "CeltMavs_2023_coach_comparison_bar.png")
        if os.path.exists(agg_path):
            st.image(agg_path, caption="Aggregate Comparison")
        else:
            st.info("Aggregate comparison chart coming soon.")
        if os.path.exists(coach_path):
            st.image(coach_path, caption="Coach Comparison")
        else:
            st.info("Coach comparison chart coming soon.")
    with col6:
        star_path = os.path.join(HIST, "CeltMavs_2023_star_comparison_bar.png")
        teammate_path = os.path.join(HIST, "CeltMavs_2023_teammate_comparison_bar.png")
        if os.path.exists(star_path):
            st.image(star_path, caption="Star Comparison")
        else:
            st.info("Star comparison chart coming soon.")
        if os.path.exists(teammate_path):
            st.image(teammate_path, caption="Teammate Comparison")
        else:
            st.info("Teammate comparison chart coming soon.")

# ══════════════════════════════════════════════════════════════════════════════
# 2024-2025 THUNDER SEASON
# ══════════════════════════════════════════════════════════════════════════════
elif selected_season == "2024-2025 Oklahoma City Thunder":

    # --- SECTION 1: CHAMPION ---
    col_logo, col_text = st.columns([1, 5])
    with col_logo:
        st.image(os.path.join(ASSETS, "Oklahoma-City-Thunder-logo.png"), width=140)
    with col_text:
        st.markdown("### 2024-2025 Oklahoma City Thunder — Championship Run")
        st.write(
            "OKC's data is probably the cleanest championship profile in this whole dataset. Their confidence "
            "curve just kept climbing and almost nothing knocked it down — no anxiety spikes, barely any "
            "frustration showing up even in the tougher games. Daigneault's coaching readings were really "
            "consistent at the podium, which I think matters more than people realize for how a team carries "
            "itself through a long playoff run. SGA's star profile was the highlight for me personally — "
            "high confidence, low negative emotion, pretty much the whole way through. And the teammate "
            "layer matched it, which is what separates good teams from championship ones in this model."
        )

    st.markdown("#### Champion Emotional Trajectories")
    col1, col2 = st.columns(2)
    with col1:
        st.image(os.path.join(HIST, "thunder_2024_aggregate_trajectory.png"),  caption="Team Aggregate Momentum")
        st.image(os.path.join(HIST, "thunder_2024_coach_trajectory.png"),      caption="Head Coach Momentum")
    with col2:
        st.image(os.path.join(HIST, "thunder_2024_star_trajectory.png"),       caption="Franchise Star Momentum")
        st.image(os.path.join(HIST, "thunder_2024_teammate_trajectory.png"),   caption="Supporting Teammates Momentum")

    st.markdown("---")

    # --- SECTION 2: RUNNER-UP ---
    col_logo2, col_text2 = st.columns([1, 5])
    with col_logo2:
        st.image(os.path.join(ASSETS, "Indiana-Pacers-Logo-2017-Present.png"), width=140)
    with col_text2:
        st.markdown("### 2024-2025 Indiana Pacers — Runner-Up Arc")
        st.write(
            "Honestly the Pacers were the most fun team to analyze in this whole project. Their early-round "
            "data looked like a team that had no business being there but just didn't know it — confidence "
            "kept building as they knocked off better-seeded teams, and Carlisle's readings stayed composed "
            "in a way I didn't expect. Haliburton's star trajectory had some real peaks in there, but also "
            "showed some vulnerability in the high-pressure moments that OKC's defense kept targeting. "
            "The place where it fell apart in the data is the teammate layer in the Finals — there's a "
            "noticeable anxiety uptick that just isn't there in the Thunder's version of the same chart. "
            "That gap felt like the difference."
        )

    st.markdown("#### Runner-Up Emotional Trajectories")
    col3, col4 = st.columns(2)
    with col3:
        st.image(os.path.join(HIST, "pacers_2024_aggregate_trajectory.png"),  caption="Team Aggregate Momentum")
        st.image(os.path.join(HIST, "pacers_2024_coach_trajectory.png"),      caption="Head Coach Momentum")
    with col4:
        st.image(os.path.join(HIST, "pacers_2024_star_trajectory.png"),       caption="Franchise Star Momentum")
        st.image(os.path.join(HIST, "pacers_2024_teammate_trajectory.png"),   caption="Supporting Teammates Momentum")

    st.markdown("---")

    # --- SECTION 3: FINALS COMBINED ---
    st.markdown("### 2025 Finals — Head-to-Head Emotional Comparison")
    st.write(
        "This is the comparison I was most curious about when I built this. The aggregate chart shows OKC "
        "ahead but not by a massive margin — what's more interesting is where the gaps show up. The teammate "
        "comparison is the clearest story: Thunder's supporting cast held significantly higher confidence and "
        "lower anxiety than Indiana's across the full Finals average. The coach chart is close but Daigneault "
        "edges out Carlisle on the composure side. The star comparison is honestly the most competitive — "
        "SGA and Haliburton were pretty evenly matched emotionally, which tracks with how their individual "
        "performances went."
    )
    col5, col6 = st.columns(2)
    with col5:
        agg_path = os.path.join(HIST, "ThunPac_2024_aggregate_comparison_bar.png")
        coach_path = os.path.join(HIST, "ThunPac_2024_coach_comparison_bar.png")
        if os.path.exists(agg_path):
            st.image(agg_path, caption="Aggregate Comparison")
        else:
            st.info("Aggregate comparison chart coming soon.")
        if os.path.exists(coach_path):
            st.image(coach_path, caption="Coach Comparison")
        else:
            st.info("Coach comparison chart coming soon.")
    with col6:
        star_path = os.path.join(HIST, "ThunPac_2024_star_comparison_bar.png")
        teammate_path = os.path.join(HIST, "ThunPac_2024_teammate_comparison_bar.png")
        if os.path.exists(star_path):
            st.image(star_path, caption="Star Comparison")
        else:
            st.info("Star comparison chart coming soon.")
        if os.path.exists(teammate_path):
            st.image(teammate_path, caption="Teammate Comparison")
        else:
            st.info("Teammate comparison chart coming soon.")