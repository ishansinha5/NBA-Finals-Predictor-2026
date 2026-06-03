import streamlit as st
import pandas as pd
import base64
import os

st.set_page_config(
    page_title="Historical Baselines", 
    page_icon="🏀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

def get_base64_bg(img_name):
    # Step up one directory from pages/ to find the image in streamlit_app/
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), img_name)
    if (os.path.exists(img_path)):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpg;base64,{encoded_string}"
    return ""

bg_base64 = get_base64_bg("image_04fa1b.jpg")

if (bg_base64):
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"] {{ display: none; }}
            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(rgba(11, 26, 48, 0.85), rgba(11, 26, 48, 0.95)), url("{bg_base64}");
                background-size: cover; background-position: center; background-attachment: fixed;
            }}
            [data-testid="stHeader"] {{ background-color: transparent; }}
            html, body, [class*="st-"], h1, h2, h3, h4, p, span, div, li {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("<style>[data-testid='stSidebar'] { display: none; } [data-testid='stAppViewContainer'] { background-color: #0b1a30; } [data-testid='stHeader'] { background-color: transparent; }</style>", unsafe_allow_html=True)

st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

nav_tabs = st.tabs([
    "Introduction", "Historical Baselines", "Modern Era Analytics", 
    "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"
])

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
    
    # Pathing up 3 levels: pages -> streamlit_app -> root -> data -> historical
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_path = os.path.join(base_dir, "data", "historical", file_name)

    if (not os.path.exists(data_path)):
        st.warning("Data file not found. Please run the ingestion pipeline.")
    else:
        df = pd.read_csv(data_path)
        sentiment_cols = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        st.markdown("---")
        st.subheader("Team Aggregates")
        df_agg = df[(df['team'] == champ_team)]
        if (not df_agg.empty):
            stage_progression = df_agg.groupby('stage')[sentiment_cols].mean()
            st.dataframe(stage_progression.style.highlight_max(axis=1, color='lightgreen'))
            st.bar_chart(df_agg[sentiment_cols].mean(), height=300)
        else:
            st.info("No aggregate data available.")
            
        st.markdown("---")
        col_c, col_s, col_t = st.columns(3)
        
        with col_c:
            st.markdown("#### Coach Podiums")
            df_coach = df[(df['team'] == champ_team) & (df['role'] == 'coach')]
            if (not df_coach.empty):
                st.bar_chart(df_coach[sentiment_cols].mean(), height=250)
                
        with col_s:
            st.markdown("#### Star Dynamics")
            df_star = df[(df['team'] == champ_team) & (df['role'] == 'star')]
            if (not df_star.empty):
                st.bar_chart(df_star[sentiment_cols].mean(), height=250)
                
        with col_t:
            st.markdown("#### Teammate Chemistry")
            df_team = df[(df['team'] == champ_team) & (df['role'] == 'teammate')]
            if (not df_team.empty):
                st.bar_chart(df_team[sentiment_cols].mean(), height=250)

# Map out routing for the other tabs back to their source pages
page_routes = [
    (0, "../1_Home.py", "Introduction"),
    (2, "4_Modern_Era_Analytics.py", "Modern Era Analytics"),
    (3, "5_AI_Intelligence_Engine.py", "RAG Engine"),
    (4, "6_2026_Finals_Predictor.py", "Live Predictor"),
    (5, "7_Finals_Matchup.py", "Finals Matchup"),
    (6, "2_Methodology.py", "Engineering Journey")
]

for idx, page_path, tab_title in page_routes:
    with nav_tabs[idx]:
        st.info(f"Explore the {tab_title} module.")
        st.page_link(page_path, label=f"Open {tab_title}", icon="🏀")