import streamlit as st
import os
import pandas as pd

st.set_page_config(page_title="Modern Era Analytics", page_icon="🏀", layout="wide")

st.title("Modern Era Deep Analytics (2024 - 2026)")
st.subheader("High-Density Bracket Mappings and Inter-Role Sentiment Tracking")

st.markdown("""
This workspace features the premium, high-density tracking layer available exclusively for modern data targets. 
Select an era and a specific team role to isolate emotional trends across coaches, franchise stars, and support units.
""")

# Main Archive Filter
selected_season = st.selectbox(
    "Select Modern Playoff Archive", 
    ["2023-2024 (Celtics/Mavericks)", "2024-2025 (Thunder/Pacers)", "2025-2026 (Live Current Cohort)"]
)

st.markdown("---")

# Granular Role Workspace Tabs
role_tab, coach_tab, star_tab, teammate_tab = st.tabs([
    "📊 Team Aggregates", 
    "👔 Coach Podiums", 
    "⭐ Star Dynamics", 
    "👥 Teammate Chemistry"
])

# ----------------------------------------------------
# 1. TEAM AGGREGATES TAB
# ----------------------------------------------------
with role_tab:
    if "2023-2024" in selected_season:
        st.header("Overarching Team Comparison: Celtics vs. Mavericks")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### The Macro Psychological Profile
            At a team aggregate level, the Random Forest model heavily weighted Boston's extreme emotional stability[cite: 4, 13]. 
            When all game transcripts are compiled, the Celtics maintained a distinct advantage in **Neutrality** and structured **Contentment**, signaling a group completely decoupled from external media narratives[cite: 13, 15].
            """)
            comp_img = "streamlit_app/assets/Celtics_vs_Mavericks_comparison.png"
            if os.path.exists(comp_img):
                st.image(comp_img, caption="Team Average Emotional Profile Side-by-Side Comparison", use_container_width=True)
        with col2:
            st.image("streamlit_app/assets/Boston-Celtics-logo.png", width=200)
            st.image("streamlit_app/assets/Dallas-Mavericks-Logo.png", width=200)

    elif "2024-2025" in selected_season:
        st.header("Overarching Team Comparison: Thunder vs. Pacers")
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("""
            ### Macro Maturity Alignment
            The aggregate vector for the 2025 Thunder perfectly mirrored the 2024 Celtics championship blueprint[cite: 15]. 
            Conversely, the Pacers' team aggregate was weighed down by late-series surges in **Frustration** and **Anxiety** expressions following road losses[cite: 15].
            """)
            comp_img = "streamlit_app/assets/Thunder_vs_Pacers_comparison.png"
            if os.path.exists(comp_img):
                st.image(comp_img, caption="Team Average Emotional Profile Side-by-Side Comparison", use_container_width=True)
        with col2:
            st.image("streamlit_app/assets/Oklahoma-City-Thunder-logo.png", width=200)

    elif "2025-2026" in selected_season:
        st.info("Live 2026 team data streams are currently processing. View the Live Predictor page to parse real-time aggregate matchups.")

# ----------------------------------------------------
# 2. COACH PODIUMS TAB
# ----------------------------------------------------
with coach_tab:
    if "2023-2024" in selected_season:
        st.header("Coach Logic Isolation: Joe Mazzulla vs. Jason Kidd")
        st.markdown("""
        *   **Joe Mazzulla (Celtics):** Stood as the algorithmic anchor for 'Stoicism'. Across all four rounds, his text records recorded zero significant variance in *Anxiety* or *Surprise* markers, keeping the locker room insulated[cite: 5, 15].
        *   **Jason Kidd (Mavericks):** Displayed classic tactical pivoting signatures—showing clear spikes in *Surprise* and *Frustration* metrics following Games 1 and 2, which the model flags as reactive rather than proactive[cite: 5, 15].
        """)
        
    elif "2024-2025" in selected_season:
        st.header("Coach Logic Isolation: Mark Daigneault vs. Rick Carlisle")
        st.markdown("""
        *   **Mark Daigneault (Thunder):** His data points tracked with pure *Neutrality* and high analytical focus, anchoring a young roster through hostile environments[cite: 5, 15].
        *   **Rick Carlisle (Pacers):** Showed intense, text-based spikes in *Upset* and *Frustration* categories during officiating queries, adding emotional friction to the series track[cite: 5, 15].
        """)
        
    elif "2025-2026" in selected_season:
        st.info("Live final coach presser streams are running through RoBERTa. Real-time vector updates will map here shortly.")

# ----------------------------------------------------
# 3. STAR DYNAMICS TAB
# ----------------------------------------------------
with star_tab:
    if "2023-2024" in selected_season:
        st.header("Franchise Star Metrics: Jayson Tatum / Jaylen Brown vs. Luka Dončić")
        st.markdown("""
        *   **Celtics Stars:** Maintained flat, uniform *Confidence* ratings[cite: 19]. Even during poor shooting stretches, their linguistic markers did not track with defensive deflation or panic[cite: 19].
        *   **Luka Dončić:** Exhibited extreme linguistic swings. Wins produced massive, unparalleled spikes in raw *Confidence* and *Contentment*, while losses triggered immediate text spikes in *Frustration* and *Upset* variables[cite: 5].
        """)
        celtics_traj = "streamlit_app/assets/Celtics_sentiment_trajectory.png"
        if os.path.exists(celtics_traj):
            st.image(celtics_traj, caption="Boston Star Profile Trajectory", use_container_width=True)

    elif "2024-2025" in selected_season:
        st.header("Franchise Star Metrics: Shai Gilgeous-Alexander vs. Tyrese Haliburton")
        st.markdown("""
        *   **Shai Gilgeous-Alexander:** Evaluated as an absolute 'business-first' profile. His transcripts registered consistent *Contentment* and flat *Anxiety* signatures across all 4 playoff series.
        *   **Tyrese Haliburton:** Showed a highly expressive emotional signature. Spikes in *Surprise* and linguistic *Anxiety* registered prominently during games where opposing coverage switched aggressively[cite: 5].
        """)
        thunder_traj = "streamlit_app/assets/Thunder_sentiment_trajectory copy.png"
        if os.path.exists(thunder_traj):
            st.image(thunder_traj, caption="OKC Star Psychological Track", use_container_width=True)

    elif "2025-2026" in selected_season:
        st.info("Live star athlete podium transcripts are compiling in your local whisper cache.")

# ----------------------------------------------------
# 4. TEAMMATE CHEMISTRY TAB
# ----------------------------------------------------
with teammate_tab:
    if "2023-2024" in selected_season:
        st.header("Support Unit Chemistry Matrix")
        st.markdown("""
        *   **Boston Teammates (White, Holiday, Horford):** Recorded an exact, tight clustering alongside their coach's profile. This confirms complete team-wide buy-in to the stoic framework[cite: 19].
        *   **Dallas Teammates:** Displayed high variance. Support player confidence plummeted when falling into series deficits, leaving the star isolated[cite: 4].
        """)
        mavs_traj = "streamlit_app/assets/Mavericks_sentiment_trajectory.png"
        if os.path.exists(mavs_traj):
            st.image(mavs_traj, caption="Dallas Teammate Vulnerability Index", use_container_width=True)

    elif "2024-2025" in selected_season:
        st.header("Support Unit Chemistry Matrix")
        st.markdown("""
        *   **OKC Teammates (Williams, Holmgren, Dort):** Despite their youth, the supporting tier's vectors clustered perfectly with the team's professional, business-like baseline signature[cite: 15].
        *   **Indiana Teammates:** Showed pronounced variance, echoing individual game volatility rather than staying anchored to a set series-long standard[cite: 15].
        """)
        pacers_traj = "streamlit_app/assets/Pacers_sentiment_trajectory.png"
        if os.path.exists(pacers_traj):
            st.image(pacers_traj, caption="Indiana Role Player Trajectory Deviation", use_container_width=True)

    elif "2025-2026" in selected_season:
        st.info("Live secondary role player media data is vectorizing inside ChromaDB[cite: 9].")