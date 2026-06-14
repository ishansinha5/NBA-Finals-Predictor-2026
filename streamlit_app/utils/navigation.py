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
        /* Hide the default sidebar and the mobile toggle button completely */
        [data-testid="stSidebar"] {{ display: none !important; }}
        [data-testid="collapsedControl"] {{ display: none !important; }}
        
        html, body, [class*="st-"], h1, h2, h3, h4, p, span, div, li {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            color: #ffffff !important;
        }}
        
        /* Protect material icons from the global font overwrite so they render correctly */
        span.stIconMaterial, 
        span[data-testid="stIconMaterial"], 
        .material-symbols-rounded,
        i.material-icons {{
            font-family: 'Material Symbols Rounded', 'Material Icons' !important;
        }}
        
        [data-testid="stPageLink"] p {{
            font-size: 0.95rem !important;
        }}
        
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

def _is_mobile():
    params = st.query_params
    vw = params.get("vw", None)
    if vw is not None:
        try:
            return int(vw) <= 768
        except (ValueError, TypeError):
            pass
    return False

def render_navigation():
    st.markdown("""
        <script>
            (function() {
                var params = new URLSearchParams(window.location.search);
                if (!params.has('vw')) {
                    params.set('vw', String(window.innerWidth));
                    var newUrl = window.location.pathname + '?' + params.toString()
                                 + window.location.hash;
                    window.history.replaceState(null, '', newUrl);
                    window.dispatchEvent(new Event('popstate'));
                }
            })();
        </script>

        <style>
            [data-testid="stPageLink"] p {
                font-size: clamp(0.65rem, 1.1vw, 0.9rem) !important;
                white-space: normal !important;
                word-break: break-word !important;
                overflow-wrap: break-word !important;
                text-align: center !important;
                line-height: 1.3 !important;
                overflow: visible !important;
            }
            [data-testid="stPageLink"] a[aria-current="page"] p {
                font-size: clamp(0.45rem, 0.65vw, 0.65rem) !important;
            }
        </style>
    """, unsafe_allow_html=True)

    mobile = _is_mobile()

    if mobile:
        with st.expander("Navigation Menu"):
            st.page_link("1_Home.py",                              label="Introduction")
            st.page_link("pages/2_Methodology.py",                 label="Engineering")
            st.page_link("pages/3_Historical_Analysis.py",         label="Historical Era")
            st.page_link("pages/4_Modern_Era_Analytics.py",        label="Modern Era")
            st.page_link("pages/5_AI_Intelligence_Engine.py",      label="RAG Engine")
            st.page_link("pages/6_2026_Finals_Predictor.py",       label="2026 Predictor")
            st.page_link("pages/7_Finals_Matchup.py",              label="Finals Matchup")
            st.page_link("pages/8_Prediction_Validation.py",       label="Validation")
    else:
        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1.1, 1.1, 1.2, 1.1, 1.1, 1.2, 1.2, 1.1])
        with col1: st.page_link("1_Home.py",                             label="Introduction")
        with col2: st.page_link("pages/2_Methodology.py",                label="Engineering")
        with col3: st.page_link("pages/3_Historical_Analysis.py",        label="Historical Era")
        with col4: st.page_link("pages/4_Modern_Era_Analytics.py",       label="Modern Era")
        with col5: st.page_link("pages/5_AI_Intelligence_Engine.py",     label="RAG Engine")
        with col6: st.page_link("pages/6_2026_Finals_Predictor.py",      label="2026 Predictor")
        with col7: st.page_link("pages/7_Finals_Matchup.py",             label="Finals Matchup")
        with col8: st.page_link("pages/8_Prediction_Validation.py",      label="Validation")

    st.markdown("---")