import streamlit as st
import os
from PIL import Image

st.set_page_config(page_title="Historical Data", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

st.title("Historical Baselines (2024 - 2025)")
st.markdown("Before predicting the future, the algorithm had to learn the past. Here is how the AI views recent NBA Champions.")

st.header("2024 NBA Finals: Celtics vs. Mavericks")
st.markdown("**Winner:** Boston Celtics")
st.markdown("*Analysis:* The Celtics exhibited the ultimate 'stoic' profile. Their neutrality scores were exceptionally high, and their emotional volatility was nearly flat. The Mavericks displayed high raw confidence, which the model learned to associate with a losing mindset.")

# Replace with your actual historical filenames if you have them saved, or just use placeholders
col1, col2 = st.columns(2)
with col1:
    st.info("Historical visual for Celtics trajectory would go here.")
with col2:
    st.info("Historical visual for Mavericks trajectory would go here.")

st.markdown("---")

st.header("2025 NBA Finals: Thunder vs. Pacers")
st.markdown("**Winner:** Oklahoma City Thunder")
st.markdown("*Analysis:* Similar to the 2024 Celtics, the Thunder maintained a tight, business-like grouping of Contentment and Neutrality, while the Pacers showed higher spikes in Frustration during losses.")