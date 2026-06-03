import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Historical Baselines", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""<style>[data-testid="stSidebar"] { display: none; }</style>""", unsafe_allow_html=True)
st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

nav_tabs = st.tabs(["Introduction", "Historical Baselines", "Modern Era Analytics", "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"])

with nav_tabs[1]:
    st.header("Historical Championship Baselines")
    
    season_map = {
        "2019-2020 Playoff Archive": ("scored_2019_2020.csv", "Lakers"),
        "2021-2022 Playoff Archive": ("scored_2021_2022.csv", "Warriors")
    }
    
    selected_season = st.selectbox("Select Historical Data Archive", list(season_map.keys()))
    file_name, champ_team = season_map[selected_season]
    
    st.markdown(f"### The {champ_team} Championship Profile")
    st.markdown(f"The {champ_team} conquered their respective NBA Finals run by establishing a rigid, emotionally flat baseline that proved entirely resistant to external media narratives. Their ability to regulate internal frustration and project unwavering collective confidence allowed them to dictate the pace of the postseason from start to finish.")
    
    data_path = os.path.join(".", "data", "historical", file_name)
    if (not os.path.exists(data_path)):
        st.warning("Data file not found. Please run the ingestion pipeline.")
    else:
        df = pd.read_csv(data_path)
        sentiment_cols = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        role_tab, coach_tab, star_tab, teammate_tab = st.tabs(["Team Aggregates", "Coach Podiums", "Star Dynamics", "Teammate Chemistry"])
        
        def display_champ_profile(role_filter):
            if (role_filter == "aggregate"):
                df_filtered = df[(df['team'] == champ_team)]
            else:
                df_filtered = df[(df['team'] == champ_team) & (df['role'] == role_filter)]
                
            if (df_filtered.empty):
                st.info(f"No {role_filter} data available for {champ_team}.")
            else:
                stage_progression = df_filtered.groupby('stage')[sentiment_cols].mean()
                st.dataframe(stage_progression.style.highlight_max(axis=1, color='lightgreen'))
                st.bar_chart(df_filtered[sentiment_cols].mean(), height=300)
                
        with role_tab:
            display_champ_profile("aggregate")
        with coach_tab:
            display_champ_profile("coach")
        with star_tab:
            display_champ_profile("star")
        with teammate_tab:
            display_champ_profile("teammate")

for idx, tab_title in enumerate(["Introduction", "Modern Era Analytics", "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"]):
    target_idx = idx if (idx < 1) else (idx + 1)
    with nav_tabs[target_idx]:
        st.info(f"Navigate to the respective sub-file to view the full {tab_title} interface.")