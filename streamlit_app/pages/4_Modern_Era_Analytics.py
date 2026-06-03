import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Modern Era Analytics", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>[data-testid="stSidebar"] { display: none; }</style>""", unsafe_allow_html=True)
st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

nav_tabs = st.tabs(["Introduction", "Historical Baselines", "Modern Era Analytics", "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"])

with nav_tabs[2]:
    st.header("Modern Era Deep Analytics")
    
    season_map = {
        "2023-2024 Playoff Archive": "scored_2023_2024.csv",
        "2024-2025 Playoff Archive": "scored_2024_2025.csv"
    }
    
    selected_season = st.selectbox("Select Modern Data Archive", list(season_map.keys()))
    
    st.markdown("### Expanding the Data Footprint")
    st.markdown("The winning franchise conquered their NBA Finals run by establishing a rigid, emotionally flat baseline that proved entirely resistant to external media narratives. Their ability to regulate internal frustration and project unwavering collective confidence allowed them to dictate the pace of the postseason from start to finish. In this modern tracking era, we have expanded our data footprint to capture the full runner-up trajectory, allowing us to pinpoint the exact moments their opponents succumbed to locker-room panic and tactical anxiety.")
    
    data_path = os.path.join(".", "data", "historical", season_map[selected_season])
    if (not os.path.exists(data_path)):
        st.warning("Data file not found. Please run the ingestion pipeline.")
    else:
        df = pd.read_csv(data_path)
        available_teams = df['team'].unique().tolist()
        sentiment_cols = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        col1, col2 = st.columns(2)
        with col1:
            team_a = st.selectbox("Select Primary Team (Champion)", available_teams, index=0)
        with col2:
            team_b = st.selectbox("Select Opponent Team (Runner-Up)", available_teams, index=1 if (len(available_teams) > 1) else 0)

        st.markdown("---")
        role_tab, coach_tab, star_tab, teammate_tab = st.tabs(["Team Aggregates", "Coach Podiums", "Star Dynamics", "Teammate Chemistry"])

        def display_team_comparison(role_filter):
            if (role_filter == "aggregate"):
                df_a = df[(df['team'] == team_a)]
                df_b = df[(df['team'] == team_b)]
            else:
                df_a = df[(df['team'] == team_a) & (df['role'] == role_filter)]
                df_b = df[(df['team'] == team_b) & (df['role'] == role_filter)]

            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"#### {team_a}")
                if (df_a.empty):
                    st.info(f"No {role_filter} data available.")
                else:
                    stage_progression = df_a.groupby('stage')[sentiment_cols].mean()
                    st.dataframe(stage_progression.style.highlight_max(axis=1, color='lightgreen'))
                    st.bar_chart(df_a[sentiment_cols].mean(), height=300)

            with c2:
                st.markdown(f"#### {team_b}")
                if (df_b.empty):
                    st.info(f"No {role_filter} data available.")
                else:
                    stage_progression = df_b.groupby('stage')[sentiment_cols].mean()
                    st.dataframe(stage_progression.style.highlight_max(axis=1, color='lightgreen'))
                    st.bar_chart(df_b[sentiment_cols].mean(), height=300)

        with role_tab: 
            display_team_comparison("aggregate")
        with coach_tab: 
            display_team_comparison("coach")
        with star_tab: 
            display_team_comparison("star")
        with teammate_tab: 
            display_team_comparison("teammate")

for idx, tab_title in enumerate(["Introduction", "Historical Baselines", "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"]):
    target_idx = idx if (idx < 2) else (idx + 1)
    with nav_tabs[target_idx]:
        st.info(f"Navigate to the respective sub-file to view the full {tab_title} interface.")