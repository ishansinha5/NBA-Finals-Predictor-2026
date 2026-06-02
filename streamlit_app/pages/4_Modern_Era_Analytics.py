import streamlit as st
import pandas as pd
import os

# Configure the page layout and strictly collapse the vertical sidebar navigation
st.set_page_config(
    page_title="Multi-Role Analytics", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Injected CSS to match the vertical sidebar suppression
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Main Header
st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Horizontal Navigation Bar
nav_tabs = st.tabs([
    "Introduction & Overview", 
    "Multi-Role Analytics", 
    "Interactive RAG Engine", 
    "2026 Finals Live Predictor",
    "Engineering Journey"
])

# Route content to the 2nd tab (Multi-Role Analytics)
with nav_tabs[1]:
    st.header("Modern Era Deep Analytics")
    st.markdown("Select a modern playoff archive to dynamically explore the psychological profiles of champions and their opponents. This interface pulls directly from the RoBERTa scoring matrix, eliminating narrative bias.")

    # Dynamic File Mapping
    season_map = {
        "2023-2024 Playoff Archive": "scored_2023_2024.csv",
        "2024-2025 Playoff Archive": "scored_2024_2025.csv",
        "2025-2026 Current Cohort": "scored_2025_2026.csv"
    }

    selected_season = st.selectbox("Select Data Archive", list(season_map.keys()))
    data_path = os.path.join(".", "data", "historical", season_map[selected_season])

    if not os.path.exists(data_path):
        st.warning(f"Data file not found at {data_path}. Please ensure the data ingestion pipeline has finished running for this season.")
    else:
        # Load the real dataset
        df = pd.read_csv(data_path)
        available_teams = df['team'].unique().tolist()
        sentiment_cols = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']

        st.markdown("### Head-to-Head Opponent Comparison")
        st.markdown("Select two teams from the archive to compare their raw emotional feature sets side-by-side.")
        
        col1, col2 = st.columns(2)
        with col1:
            team_a = st.selectbox("Select Primary Team", available_teams, index=0)
        with col2:
            team_b = st.selectbox("Select Opponent Team", available_teams, index=1 if len(available_teams) > 1 else 0)

        st.markdown("---")

        # Granular Role Workspace Tabs
        role_tab, coach_tab, star_tab, teammate_tab = st.tabs([
            "Team Aggregates", 
            "Coach Podiums", 
            "Star Dynamics", 
            "Teammate Chemistry"
        ])

        def display_team_comparison(role_filter):
            """Helper function to filter the dataframe by role and display sentiment averages."""
            if role_filter == "aggregate":
                df_a = df[df['team'] == team_a]
                df_b = df[df['team'] == team_b]
            else:
                df_a = df[(df['team'] == team_a) & (df['role'] == role_filter)]
                df_b = df[(df['team'] == team_b) & (df['role'] == role_filter)]

            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown(f"#### {team_a}")
                if df_a.empty:
                    st.info(f"No {role_filter} data available for {team_a}.")
                else:
                    # Group by stage to show chronological progression
                    stage_progression = df_a.groupby('stage')[sentiment_cols].mean()
                    st.dataframe(stage_progression.style.highlight_max(axis=1, color='lightgreen'))
                    st.bar_chart(df_a[sentiment_cols].mean(), height=300)

            with c2:
                st.markdown(f"#### {team_b}")
                if df_b.empty:
                    st.info(f"No {role_filter} data available for {team_b}.")
                else:
                    # Group by stage to show chronological progression
                    stage_progression = df_b.groupby('stage')[sentiment_cols].mean()
                    st.dataframe(stage_progression.style.highlight_max(axis=1, color='lightgreen'))
                    st.bar_chart(df_b[sentiment_cols].mean(), height=300)

        with role_tab:
            st.markdown("Full roster averages (combining coach, star, and teammate outputs) across all available playoff stages.")
            display_team_comparison("aggregate")

        with coach_tab:
            st.markdown("Isolated tactical and emotional responses from the Head Coach.")
            display_team_comparison("coach")

        with star_tab:
            st.markdown("Isolated linguistic markers from the primary franchise stars.")
            display_team_comparison("star")

        with teammate_tab:
            st.markdown("Isolated chemistry and alignment metrics from the supporting role players.")
            display_team_comparison("teammate")

# Informational placeholders for other horizontal tabs
for idx, tab_title in enumerate(["Introduction & Overview", "Interactive RAG Engine", "2026 Finals Live Predictor", "Engineering Journey"]):
    # Adjust index to route around the active tab
    target_idx = idx if idx < 1 else idx + 1
    with nav_tabs[target_idx]:
        st.info(f"Navigate to the respective sub-file to view the full {tab_title} interface.")