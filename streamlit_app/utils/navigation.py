import streamlit as st
import base64
import os

def get_base64_bg(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpg;base64,{encoded_string}"
    return ""

def apply_global_styles():
    bg_base64 = get_base64_bg("image_04fa1b.jpg")
    css = f"""
    <style>
        [data-testid="stSidebar"] {{ display: none; }}
        body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
        [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(11, 26, 48, 0.85), rgba(11, 26, 48, 0.95)), url("data:image/jpg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stHeader"] {{ background-color: transparent; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_navigation():
    # Explicit columns for the navigation header
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    with col1: st.page_link("1_Home.py", label="Introduction", icon="🏀")
    with col2: st.page_link("pages/3_Historical_Analysis.py", label="Historical", icon="🏀")
    with col3: st.page_link("pages/4_Modern_Era_Analytics.py", label="Analytics", icon="🏀")
    with col4: st.page_link("pages/5_AI_Intelligence_Engine.py", label="RAG Engine", icon="🏀")
    with col5: st.page_link("pages/6_2026_Finals_Predictor.py", label="Predictor", icon="🏀")
    with col6: st.page_link("pages/7_Finals_Matchup.py", label="Matchup", icon="🏀")
    with col7: st.page_link("pages/2_Methodology.py", label="Engineering", icon="🏀")
    st.markdown("---")