import streamlit as st
from PIL import Image
import os

st.set_page_config(page_title="Matchups", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

st.title("Live 2026 Head-to-Head Matchups")

teams = ["Spurs", "Thunder", "Knicks", "Cavaliers"]

col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Team 1", teams, index=0)
with col2:
    team2 = st.selectbox("Team 2", [t for t in teams if t != team1], index=2)

st.markdown("---")

# Dynamic 50/50 Image Split based on dropdown
img_col1, img_col2 = st.columns(2)
with img_col1:
    # Ensure your images are named 'spurs_image.jpg', 'knicks_image.jpg', etc.
    t1_img_path = f"streamlit_app/assets/{team1.lower()}_image.jpg"
    if os.path.exists(t1_img_path):
        st.image(t1_img_path, use_container_width=True)
with img_col2:
    t2_img_path = f"streamlit_app/assets/{team2.lower()}_image.jpg"
    if os.path.exists(t2_img_path):
        st.image(t2_img_path, use_container_width=True)

st.markdown("---")

# Prediction Text 
txt_path_1 = f"streamlit_app/assets/{team1}_vs_{team2}.txt"
txt_path_2 = f"streamlit_app/assets/{team2}_vs_{team1}.txt"

if os.path.exists(txt_path_1):
    with open(txt_path_1, "r") as f:
        st.success(f.read())
elif os.path.exists(txt_path_2):
    with open(txt_path_2, "r") as f:
        st.success(f.read())

st.markdown("---")

# Make comparison graph massive
st.subheader("Aggregate Emotional Profile")
img_path_1 = f"streamlit_app/assets/{team1}_vs_{team2}_comparison.png"
img_path_2 = f"streamlit_app/assets/{team2}_vs_{team1}_comparison.png"

if os.path.exists(img_path_1):
    st.image(Image.open(img_path_1), use_container_width=True)
elif os.path.exists(img_path_2):
    st.image(Image.open(img_path_2), use_container_width=True)

st.markdown("---")

# Trajectories stacked vertically
st.subheader("Chronological Playoff Trajectories")
t1_traj = f"streamlit_app/assets/{team1}_sentiment_trajectory.png"
t2_traj = f"streamlit_app/assets/{team2}_sentiment_trajectory.png"

if os.path.exists(t1_traj):
    st.image(Image.open(t1_traj), use_container_width=True)
if os.path.exists(t2_traj):
    st.image(Image.open(t2_traj), use_container_width=True)