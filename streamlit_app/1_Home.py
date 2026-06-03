import streamlit as st
import base64
import os

# Configure the page layout and strictly collapse the vertical sidebar navigation
st.set_page_config(
    page_title="2026 NBA Finals NLP Predictor", 
    page_icon="🏀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

def get_base64_bg(img_path):
    """Helper function to convert local image to base64 for background injection."""
    if (os.path.exists(img_path)):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpg;base64,{encoded_string}"
    return ""

# Target the uploaded NBA silk background asset
bg_base64 = get_base64_bg("image_04fa1b.jpg")

# Inject custom background styling using your exact provided image layer
if (bg_base64):
    st.markdown(f"""
        <style>
            /* Hide the default Streamlit sidebar */
            [data-testid="stSidebar"] {{
                display: none;
            }}
            
            /* Apply the full silk background image with a dark overlay for text scannability */
            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(rgba(11, 26, 48, 0.85), rgba(11, 26, 48, 0.95)), url("{bg_base64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* Make the header background transparent so it blends perfectly */
            [data-testid="stHeader"] {{
                background-color: transparent;
            }}
        </style>
    """, unsafe_allow_html=True)
else:
    # Fallback to standard theme color if the asset file is missing temporarily
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
            [data-testid="stAppViewContainer"] { background-color: #0b1a30; }
            [data-testid="stHeader"] { background-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

# Main Header Banner
st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Comprehensive 7-page horizontal navigation bar
nav_tabs = st.tabs([
    "Introduction", 
    "Historical Baselines", 
    "Modern Era Analytics", 
    "RAG Engine", 
    "Live Predictor", 
    "Finals Matchup", 
    "Engineering Journey"
])

# Render the primary introduction content
with nav_tabs[0]:
    
    # Hero Visual Section updated with correct 2026 stretch width parameter
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
    *   **Transcript Ingestion:** The pipeline maps game indexes to video tags, pulling available text tracks or sending media audio streams directly into a local speech-to-text model when requests face network limits.
    *   **Linguistic Feature Extraction:** The system breaks down post-game statements across a specialized language model to measure precise readings for specific emotions, including *confidence, contentment, neutrality, frustration, upset, anxiety, and surprise*.
    *   **The Scoring Filter Boundary:** To protect the models from data corruption, we explicitly stop collecting transcript data exactly one game before any series is decided. This prevents the highly celebratory, anomalous emotional spikes of a clinching game from poisoning our regular series indicators.
    *   **Roster Layer Classification:** The data is flattened independently across coaches, franchise stars, and supporting teammates to see how closely aligned a group stays during a series.
    
    ### Phase 2: Search Index and Retrieval Augmentation (RAG)
    *   **Text Partitioning:** The engine divides long interview documents into small paragraphs to make sure text strings do not get clipped by processing thresholds.
    *   **Semantic Local Storage:** Passages are saved into a localized search database, allowing us to query exact quotes by team filters or specific game scenarios.
    *   **Query Interface:** A simple terminal lets users query real context directly from historical playoff files, making it easy to see exactly what players said without reading through hours of text manually.
    """)
    
    st.markdown("---")
    
    st.markdown("## Computing Priorities and Resource Mindfulness")
    st.markdown("""
    A major personal goal while designing this tool was keeping things computationally lightweight and runnable on standard hardware. Instead of relying on heavy cloud servers or paid online interfaces that require massive computing steps, this tracking pipeline handles everything locally to keep a small processing footprint.
    
    *   **Compact Models:** All text parsing is done using localized transformer architectures. This lets us compute complex language shapes on consumer-grade hardware with zero network dependencies.
    *   **Smart Memory Boundaries:** The ingestion system processes data using a custom context generator to stay safely inside system memory layout limits.
    *   **Fast Binary Indexing:** Storing data coordinates in local database tables keeps lookup speeds under a millisecond while entirely skipping heavy software overhead.
    """)

# Render empty redirection containers for remaining tabs
# Render functional page routing buttons for the remaining tabs
with nav_tabs[1]:
    st.info("Explore the legacy data constraints and historical baselines.")
    if (os.path.exists("pages/3_Historical_Baselines.py")):
        st.page_link("pages/3_Historical_Baselines.py", label="Load Historical Baselines", icon="🏀")

with nav_tabs[2]:
    st.info("Compare emotional matrices between champions and runner-ups.")
    if (os.path.exists("pages/4_Modern_Era_Analytics.py")):
        st.page_link("pages/4_Modern_Era_Analytics.py", label="Load Modern Era Analytics", icon="🏀")

with nav_tabs[3]:
    st.info("Query the vector database for exact context.")
    if (os.path.exists("pages/5_AI_Intelligence_Engine.py")):
        st.page_link("pages/5_AI_Intelligence_Engine.py", label="Load RAG Engine", icon="🏀")

with nav_tabs[4]:
    st.info("Track the live emotional trajectory of the active bracket.")
    if (os.path.exists("pages/6_2026_Finals_Predictor.py")):
        st.page_link("pages/6_2026_Finals_Predictor.py", label="Load Live Predictor", icon="🏀")

with nav_tabs[5]:
    st.info("View the final algorithmic verdict for the championship.")
    if (os.path.exists("pages/7_Finals_Matchup.py")):
        st.page_link("pages/7_Finals_Matchup.py", label="Load Finals Matchup", icon="🏀")

with nav_tabs[6]:
    st.info("Review the architectural pivot from V1 to V2.")
    if (os.path.exists("pages/2_Methodology.py")):
        st.page_link("pages/2_Methodology.py", label="Load Engineering Journey", icon="🏀")