import streamlit as st
from PIL import Image
import os

st.title("Head-to-Head Matchup Analysis")

teams = ["Spurs", "Thunder", "Knicks", "Cavaliers"]

col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Team 1", teams, index=0)
with col2:
    team2 = st.selectbox("Team 2", [t for t in teams if t != team1], index=1)

st.markdown("---")

# Load Prediction Text
txt_path_1 = f"streamlit_app/assets/{team1}_vs_{team2}.txt"
txt_path_2 = f"streamlit_app/assets/{team2}_vs_{team1}.txt"

if os.path.exists(txt_path_1):
    with open(txt_path_1, "r") as f:
        st.info(f.read())
elif os.path.exists(txt_path_2):
    with open(txt_path_2, "r") as f:
        st.info(f.read())

# Load Bar Chart
img_path_1 = f"streamlit_app/assets/{team1}_vs_{team2}_comparison.png"
img_path_2 = f"streamlit_app/assets/{team2}_vs_{team1}_comparison.png"

try:
    if os.path.exists(img_path_1):
        st.image(Image.open(img_path_1), use_container_width=True)
    elif os.path.exists(img_path_2):
        st.image(Image.open(img_path_2), use_container_width=True)
except Exception as e:
    st.error("Error loading comparison graphic.")

# Load Trajectory Charts
st.subheader("Series Emotional Trajectories")
col3, col4 = st.columns(2)

t1_traj = f"streamlit_app/assets/{team1}_sentiment_trajectory.png"
with col3:
    if os.path.exists(t1_traj):
        st.image(Image.open(t1_traj), use_container_width=True)

t2_traj = f"streamlit_app/assets/{team2}_sentiment_trajectory.png"
with col4:
    if os.path.exists(t2_traj):
        st.image(Image.open(t2_traj), use_container_width=True)