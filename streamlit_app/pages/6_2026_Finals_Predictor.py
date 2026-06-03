import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Live Predictor", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>[data-testid="stSidebar"] { display: none; }</style>""", unsafe_allow_html=True)
st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

nav_tabs = st.tabs(["Introduction", "Historical Baselines", "Modern Era Analytics", "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"])

with nav_tabs[4]:
    st.header("2026 Live Conference Finals Tracker")
    st.markdown("This dashboard maps the real-time emotional features extracted from the 2026 Conference Finals. The Thunder and Cavs are mapped specifically as the baseline opponents against the Spurs and Knicks, respectively, allowing us to trace the elimination volatility.")

    data_path = os.path.join(".", "data", "historical", "scored_2025_2026.csv")
    
    if (not os.path.exists(data_path)):
        st.warning("2026 Live data file not found. Ensure the ingestion pipeline is running for the current bracket.")
    else:
        df = pd.read_csv(data_path)
        sentiment_cols = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        st.markdown("### Western Conference: Spurs vs. Thunder")
        col_w1, col_w2 = st.columns(2)
        
        spurs_df = df[(df['team'] == 'Spurs')]
        thunder_df = df[(df['team'] == 'Thunder')]
        
        with col_w1:
            st.markdown("#### San Antonio Spurs")
            if (not spurs_df.empty):
                st.line_chart(spurs_df.groupby('stage')[sentiment_cols].mean())
            else:
                st.info("Awaiting live data streams.")
                
        with col_w2:
            st.markdown("#### Oklahoma City Thunder (Opponent)")
            if (not thunder_df.empty):
                st.line_chart(thunder_df.groupby('stage')[sentiment_cols].mean())
            else:
                st.info("Awaiting live data streams.")
                
        st.markdown("---")
        
        st.markdown("### Eastern Conference: Knicks vs. Cavs")
        col_e1, col_e2 = st.columns(2)
        
        knicks_df = df[(df['team'] == 'Knicks')]
        cavs_df = df[(df['team'] == 'Cavs')]
        
        with col_e1:
            st.markdown("#### New York Knicks")
            if (not knicks_df.empty):
                st.line_chart(knicks_df.groupby('stage')[sentiment_cols].mean())
            else:
                st.info("Awaiting live data streams.")
                
        with col_e2:
            st.markdown("#### Cleveland Cavaliers (Opponent)")
            if (not cavs_df.empty):
                st.line_chart(cavs_df.groupby('stage')[sentiment_cols].mean())
            else:
                st.info("Awaiting live data streams.")

for idx, tab_title in enumerate(["Introduction", "Historical Baselines", "Modern Era Analytics", "RAG Engine", "Finals Matchup", "Engineering Journey"]):
    target_idx = idx if (idx < 4) else (idx + 1)
    with nav_tabs[target_idx]:
        st.info(f"Navigate to the respective sub-file to view the full {tab_title} interface.")