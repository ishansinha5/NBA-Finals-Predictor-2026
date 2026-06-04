import streamlit as st
import base64
import os

def get_base64_bg(img_name):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img_path = os.path.join(base_dir, img_name)
    
    if (os.path.exists(img_path) == False):
        img_path = os.path.join(os.getcwd(), img_name)
        
    if (os.path.exists(img_path) == True):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
            
        return encoded_string
        
    return ""

def apply_global_styles():
    bg_base64 = get_base64_bg("image_04fa1b.jpg")
    
    if (bg_base64 != ""):
        bg_css = f'background: linear-gradient(rgba(11, 26, 48, 0.85), rgba(11, 26, 48, 0.95)), url("data:image/jpg;base64,{bg_base64}"); background-size: cover; background-position: center; background-attachment: fixed;'
    else:
        bg_css = 'background-color: #0b1a30;'

    css = f"""
    <style>
        [data-testid="stSidebar"] {{ display: none !important; }}
        
        /* Force Helvetica and white text globally */
        html, body, [class*="st-"], h1, h2, h3, h4, p, span, div, li {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* Drop the font size of the links slightly so they never overflow */
        [data-testid="stPageLink"] p {{
            font-size: 0.95rem !important;
        }}
        
        /* Hide those ugly chain link icons next to headers */
        h1 a, h2 a, h3 a, h4 a, h5 a, h6 a, .st-emotion-cache-1629p8f a {{
            display: none !important;
            pointer-events: none !important;
        }}
        
        [data-testid="stAppViewContainer"] {{
            {bg_css}
        }}
        
        [data-testid="stHeader"] {{ background-color: transparent !important; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_navigation():
    # Responsive nav: 7-column row on desktop, expander on mobile
    st.markdown("""
        <style>
            /* Fix desktop tab truncation — allow page link text to wrap */
            [data-testid="stPageLink"] p {
                font-size: 0.85rem !important;
                white-space: normal !important;
                word-break: break-word !important;
                text-align: center !important;
                line-height: 1.3 !important;
            }
            @media (max-width: 768px) {
                .desktop-nav { display: none !important; }
            }
            @media (min-width: 769px) {
                .mobile-nav { display: none !important; }
            }
        </style>
    """, unsafe_allow_html=True)

    # Desktop: 7-column row
    st.markdown('<div class="desktop-nav">', unsafe_allow_html=True)
    col1, col2, col3, col4, col5, col6, col7 = st.columns([1.1, 1.1, 1.2, 1.1, 1.2, 1.2, 1.2])
    with col1: st.page_link("1_Home.py", label="Introduction", icon="🏀")
    with col2: st.page_link("pages/2_Methodology.py", label="Engineering", icon="🏀")
    with col3: st.page_link("pages/3_Historical_Analysis.py", label="Historical Era", icon="🏀")
    with col4: st.page_link("pages/4_Modern_Era_Analytics.py", label="Modern Era", icon="🏀")
    with col5: st.page_link("pages/5_AI_Intelligence_Engine.py", label="RAG Engine", icon="🏀")
    with col6: st.page_link("pages/6_2026_Finals_Predictor.py", label="2026 Predictor", icon="🏀")
    with col7: st.page_link("pages/7_Finals_Matchup.py", label="Finals Matchup", icon="🏀")
    st.markdown('</div>', unsafe_allow_html=True)

    # Mobile: expander dropdown
    st.markdown('<div class="mobile-nav">', unsafe_allow_html=True)
    with st.expander("🏀 Navigation Menu"):
        st.page_link("1_Home.py", label="🏀 Introduction")
        st.page_link("pages/2_Methodology.py", label="🏀 Engineering")
        st.page_link("pages/3_Historical_Analysis.py", label="🏀 Historical Era")
        st.page_link("pages/4_Modern_Era_Analytics.py", label="🏀 Modern Era")
        st.page_link("pages/5_AI_Intelligence_Engine.py", label="🏀 RAG Engine")
        st.page_link("pages/6_2026_Finals_Predictor.py", label="🏀 2026 Predictor")
        st.page_link("pages/7_Finals_Matchup.py", label="🏀 Finals Matchup")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")