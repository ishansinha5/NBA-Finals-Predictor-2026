import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Finals Matchup", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>[data-testid="stSidebar"] { display: none; }</style>""", unsafe_allow_html=True)
st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

nav_tabs = st.tabs(["Introduction", "Historical Baselines", "Modern Era Analytics", "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"])

with nav_tabs[5]:
    st.header("The Ultimate 2026 Finals Prediction: Spurs vs. Knicks")
    st.markdown("By directly pitting the psychological trajectories of the San Antonio Spurs against the New York Knicks, our dual-checkpoint Random Forest architecture has synthesized thousands of text vectors into a single probabilistic outcome.")
    
    st.markdown("### The Verdict")
    st.success("**Projected 2026 NBA Champion: San Antonio Spurs in 6 Games**")
    
    st.markdown("""
    **The Algorithmic Justification:**
    When normalizing the emotional feature matrices of both rosters across the grueling Conference Finals stretch, the Spurs exhibited a phenomenally high **Neutrality** and **Contentment** moving average, mirroring the exact baseline set by the 2024 Celtics and the 2020 Lakers. 
    
    Conversely, while the Knicks survived the East, their semantic vectors revealed underlying spikes in **Anxiety** and **Frustration** during tight games. The model detects this latent volatility as an exploitable vulnerability under peak Finals pressure.
    """)
    
    st.markdown("---")
    st.markdown("### Head-to-Head Emotion Vector Comparison")
    
    data_path = os.path.join(".", "data", "historical", "scored_2025_2026.csv")
    if (os.path.exists(data_path)):
        df = pd.read_csv(data_path)
        spurs_df = df[(df['team'] == 'Spurs')]
        knicks_df = df[(df['team'] == 'Knicks')]
        sentiment_cols = ['confidence', 'content', 'neutrality', 'frustration', 'upset', 'anxiety', 'surprise']
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("#### San Antonio Spurs Profile")
            if (not spurs_df.empty):
                st.bar_chart(spurs_df[sentiment_cols].mean(), color="#000000")
        with c2:
            st.markdown("#### New York Knicks Profile")
            if (not knicks_df.empty):
                st.bar_chart(knicks_df[sentiment_cols].mean(), color="#F58426")
    else:
        st.warning("Live 2026 data file not found to map the direct comparison.")

for idx, tab_title in enumerate(["Introduction", "Historical Baselines", "Modern Era Analytics", "RAG Engine", "Live Predictor", "Engineering Journey"]):
    target_idx = idx if (idx < 5) else (idx + 1)
    with nav_tabs[target_idx]:
        st.info(f"Navigate to the respective sub-file to view the full {tab_title} interface.")