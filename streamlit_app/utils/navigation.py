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

def _inject_viewport_detector():
    """
    Injects a tiny JS snippet that writes window.innerWidth into a hidden
    Streamlit text input on first load. This lets Python read the real
    viewport width and decide which nav to render — no CSS trickery needed.
    """
    st.markdown("""
        <style>
            /* Viewport detector input: completely invisible */
            #viewport-width-container { display: none !important; }
        </style>
        <div id="viewport-width-container">
            <input id="viewport-width-input" type="text" />
        </div>
        <script>
            (function() {
                var w = window.innerWidth;
                // Write into Streamlit session via URL param trick — we use
                // localStorage as a relay since we can't call Python directly
                try { localStorage.setItem('st_viewport_width', String(w)); } catch(e) {}
                // Also try to patch the hidden input for frameworks that watch it
                var el = document.getElementById('viewport-width-input');
                if (el) { el.value = String(w); }
            })();
        </script>
    """, unsafe_allow_html=True)

def _is_mobile():
    """
    Returns True when the viewport is mobile-sized.
    Uses st.query_params as the JS→Python bridge: the injected script
    sets ?vw=<width> on first paint, which Streamlit picks up on rerun.
    Falls back to False (desktop) if width is unknown.
    """
    # Check query param set by the JS below
    params = st.query_params
    vw = params.get("vw", None)
    if vw is not None:
        try:
            return int(vw) <= 768
        except (ValueError, TypeError):
            pass
    return False

def render_navigation():
    # Inject JS that appends ?vw=<innerWidth> to the URL on first load,
    # which causes Streamlit to rerun with the width available in query_params.
    st.markdown("""
        <script>
            (function() {
                var params = new URLSearchParams(window.location.search);
                if (!params.has('vw')) {
                    params.set('vw', String(window.innerWidth));
                    var newUrl = window.location.pathname + '?' + params.toString()
                                 + window.location.hash;
                    window.history.replaceState(null, '', newUrl);
                    // Trigger Streamlit rerun by dispatching a storage event
                    window.dispatchEvent(new Event('popstate'));
                }
            })();
        </script>

        <style>
            /* Viewport-relative font size so tabs never clip regardless of
               browser zoom or OS font scale setting */
            [data-testid="stPageLink"] p {
                font-size: clamp(0.65rem, 1.1vw, 0.9rem) !important;
                white-space: normal !important;
                word-break: break-word !important;
                overflow-wrap: break-word !important;
                text-align: center !important;
                line-height: 1.3 !important;
                overflow: visible !important;
            }
        </style>
    """, unsafe_allow_html=True)

    mobile = _is_mobile()

    if mobile:
        # Mobile: single expander dropdown — no column grid
        with st.expander("🏀 Navigation Menu"):
            st.page_link("1_Home.py",                              label="🏀 Introduction")
            st.page_link("pages/2_Methodology.py",                 label="🏀 Engineering")
            st.page_link("pages/3_Historical_Analysis.py",         label="🏀 Historical Era")
            st.page_link("pages/4_Modern_Era_Analytics.py",        label="🏀 Modern Era")
            st.page_link("pages/5_AI_Intelligence_Engine.py",      label="🏀 RAG Engine")
            st.page_link("pages/6_2026_Finals_Predictor.py",       label="🏀 2026 Predictor")
            st.page_link("pages/7_Finals_Matchup.py",              label="🏀 Finals Matchup")
    else:
        # Desktop: 7-column row
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1.1, 1.1, 1.2, 1.1, 1.2, 1.2, 1.2])
        with col1: st.page_link("1_Home.py",                             label="Introduction",  icon="🏀")
        with col2: st.page_link("pages/2_Methodology.py",                label="Engineering",   icon="🏀")
        with col3: st.page_link("pages/3_Historical_Analysis.py",        label="Historical Era",icon="🏀")
        with col4: st.page_link("pages/4_Modern_Era_Analytics.py",       label="Modern Era",    icon="🏀")
        with col5: st.page_link("pages/5_AI_Intelligence_Engine.py",     label="RAG Engine",    icon="🏀")
        with col6: st.page_link("pages/6_2026_Finals_Predictor.py",      label="2026 Predictor",icon="🏀")
        with col7: st.page_link("pages/7_Finals_Matchup.py",             label="Finals Matchup",icon="🏀")

    st.markdown("---")