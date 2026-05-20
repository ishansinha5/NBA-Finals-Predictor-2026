import streamlit as st

st.set_page_config(page_title="Historical Data", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

st.title("Historical Baselines (2024 - 2025)")
st.markdown("Before predicting the future, the algorithm had to learn the past. Here is how the AI views recent NBA Champions.")

st.header("2024 NBA Finals: Celtics vs. Mavericks")
st.markdown("**Winner:** Boston Celtics")

# Asymmetric columns to make the winner visually larger
col1, col2 = st.columns([1.5, 1])
with col1:
    st.image("streamlit_app/assets/Boston-Celtics-logo.png", caption="2024 Champions: Boston Celtics", use_container_width=True)
with col2:
    st.image("streamlit_app/assets/Dallas-Mavericks-Logo.png", caption="2024 Runner-Up: Dallas Mavericks", use_container_width=True)

st.markdown("*Analysis:* The Celtics exhibited the ultimate 'stoic' profile. Their neutrality scores were exceptionally high, and their emotional volatility was nearly flat. The Mavericks displayed high raw confidence, which the model learned to associate with a losing mindset.")

st.subheader("Series Trajectories")
st.image("streamlit_app/assets/Celtics_sentiment_trajectory.png", use_container_width=True)
st.image("streamlit_app/assets/Mavericks_sentiment_trajectory.png", use_container_width=True)

st.markdown("---")

st.header("2025 NBA Finals: Thunder vs. Pacers")
st.markdown("**Winner:** Oklahoma City Thunder")

col3, col4 = st.columns([1.5, 1])
with col3:
    st.image("streamlit_app/assets/Oklahoma-City-Thunder-logo.png", caption="2025 Champions: OKC Thunder", use_container_width=True)
with col4:
    st.image("streamlit_app/assets/Indiana-Pacers-Logo-2017-Present.png", caption="2025 Runner-Up: Indiana Pacers", use_container_width=True)

st.markdown("*Analysis:* Similar to the 2024 Celtics, the Thunder maintained a tight, business-like grouping of Contentment and Neutrality, while the Pacers showed higher spikes in Frustration during losses.")

st.subheader("Series Trajectories")
st.image("streamlit_app/assets/Thunder_sentiment_trajectory copy.png", use_container_width=True)
st.image("streamlit_app/assets/Pacers_sentiment_trajectory.png", use_container_width=True)