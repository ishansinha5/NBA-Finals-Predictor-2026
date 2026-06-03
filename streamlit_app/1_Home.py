import streamlit as st
import base64
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

def get_base64_bg(img_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
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
        @import url('https://fonts.googleapis.com/css2?family=Russo+One&display=swap');

        [data-testid="stSidebar"] {{ display: none !important; }}
        
        /* Russo One exclusively for title sections */
        h1, h2, h3 {{
            font-family: 'Russo One', Impact, 'Arial Black', sans-serif !important;
            color: #ffffff !important;
            letter-spacing: 1px;
        }}
        
        /* Keep Helvetica locked for text layouts to preserve smooth scannability */
        html, body, [class*="st-"], h4, p, span, div, li {{
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            color: #ffffff !important;
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

def render_navigation():
    col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
    
    with col1: st.page_link("1_Home.py", label="Introduction", icon="🏀")
    with col2: st.page_link("pages/3_Historical_Analysis.py", label="Historical", icon="🏀")
    with col3: st.page_link("pages/4_Modern_Era_Analytics.py", label="Analytics", icon="🏀")
    with col4: st.page_link("pages/5_AI_Intelligence_Engine.py", label="RAG Engine", icon="🏀")
    with col5: st.page_link("pages/6_2026_Finals_Predictor.py", label="Predictor", icon="🏀")
    with col6: st.page_link("pages/7_Finals_Matchup.py", label="Matchup", icon="🏀")
    with col7: st.page_link("pages/2_Methodology.py", label="Engineering", icon="🏀")
    
    st.markdown("---")


# ── Page entry point ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="2026 NBA Finals NLP Predictor",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

apply_global_styles()
render_navigation()

# Main Header Banner
st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Hero Visual Section
st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop", width="stretch")

st.markdown("## Project Motivation")
st.markdown("""
Standard basketball analytics usually focus on box score statistics like field goal rates, defensive metrics, and true shooting efficiency. While those numbers do a great job of showing *what* happened on the court, they cannot quite capture the mental mindset and emotional state of a locker room dealing with playoff intensity. 

I wanted to see if we could find a new angle by looking at text data from post-game podium press conferences. This project converts those transcripts into clear emotional scores. My goal was to discover whether steady linguistic composure can actually act as a helpful indicator for tracking championship runs.
""")

st.markdown("---")

st.markdown("## Core Project Steps")
st.markdown("""
The overall architecture processes language data across two straightforward layers to build our sports intelligence backend:

### Phase 1: Tabular Sentiment and Predictive Analysis
* **Transcript Ingestion:** The pipeline maps game indexes to video tags, pulling available text tracks or sending media audio streams directly into a local speech-to-text model when requests face network limits.
* **Linguistic Feature Extraction:** The system breaks down post-game statements across a specialized language model to measure precise readings for specific emotions, including *confidence, contentment, neutrality, frustration, upset, anxiety, and surprise*.
* **The Scoring Filter Boundary:** To protect the models from data corruption, we explicitly stop collecting transcript data exactly one game before any series is decided. This prevents the highly celebratory, anomalous emotional spikes of a clinching game from poisoning our regular series indicators.
* **Roster Layer Classification:** The data is flattened independently across coaches, franchise stars, and supporting teammates to see how closely aligned a group stays during a series.

### Phase 2: Search Index and Retrieval Augmentation (RAG)
* **Text Partitioning:** The engine divides long interview documents into small paragraphs to make sure text strings do not get clipped by processing thresholds.
* **Semantic Local Storage:** Passages are saved into a localized search database, allowing us to query exact quotes by team filters or specific game scenarios.
* **Query Interface:** A simple terminal lets users query real context directly from historical playoff files, making it easy to see exactly what players said without reading through hours of text manually.
""")

st.markdown("---")

st.markdown("## Computing Priorities and Resource Mindfulness")
st.markdown("""
A major personal goal while designing this tool was keeping things computationally lightweight and runnable on standard hardware. Instead of relying on heavy cloud servers or paid online interfaces that require massive computing steps, this tracking pipeline handles everything locally to keep a small processing footprint.

* **Compact Models:** All text parsing is done using localized transformer architectures. This lets us compute complex language shapes on consumer-grade hardware with zero network dependencies.
* **Smart Memory Boundaries:** The ingestion system processes data using a custom context generator to stay safely inside system memory layout limits.
* **Fast Binary Indexing:** Storing data coordinates in local database tables keeps lookup speeds under a millisecond while entirely skipping heavy software overhead.
""")