import streamlit as st
import base64
import os

# Configure the page layout and strictly collapse the vertical sidebar navigation
st.set_page_config(
    page_title="Design Journey and Methodology", 
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

# Inject custom background styling using the same silk image layer
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
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none; }
            [data-testid="stAppViewContainer"] { background-color: #0b1a30; }
            [data-testid="stHeader"] { background-color: transparent; }
        </style>
    """, unsafe_allow_html=True)

# Main Header
st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Horizontal Navigation Bar matching 1_Home.py exactly
nav_tabs = st.tabs([
    "Introduction", 
    "Historical Baselines", 
    "Modern Era Analytics", 
    "RAG Engine", 
    "Live Predictor", 
    "Finals Matchup", 
    "Engineering Journey"
])

# Route content directly to the 7th tab slot (Engineering Journey)
with nav_tabs[6]:
    st.header("The Architectural Evolution: V1 vs. V2")
    st.subheader("An Engineering Overhaul Across Data Footprints, Feature Matrices, and Filtering Mechanics")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Legacy V1 Paradigm: The Proof of Concept")
        st.markdown("""
        *   **Restricted Data Footprint:** The initial framework evaluated only two years of high-density data, specifically targeting the 2024 and 2025 Finals runs.
        *   **Linguistic Truncation:** Passages were shortened using basic hard truncation at 2500 characters, which frequently missed crucial late press conference adjustments.
        *   **Tabular Blind Spot:** The system lacked granular multi-role separation and simply averaged entire roster outputs together into a single monolithic team bucket.
        *   **The Survival Bias Flaw:** By only training on teams that successfully reached the Finals, the model never learned what an early round exit looked like, making it difficult to accurately evaluate first round panic.
        """)

    with col2:
        st.markdown("### Upgraded V2 Framework: The Production Pipeline")
        st.markdown("""
        *   **Preservation of the Score Filter:** I stopped collecting transcript data exactly one game before any series wraps up. Post-series celebration scripts introduce massive emotional spikes that do not reflect sustainable championship readiness. 
        *   **Tri-Tier Role Isolation:** The feature matrix now separates unique team dynamics across three distinct roles: coaches, star players, and role players. This captures internal alignment and tracks leadership stability versus locker room panic.
        *   **Multi-Season Historical Scaling:** The pipeline expands to include other older seasons, like the 2020 bubble run, via an adaptive data tiering approach to broaden our historical baselines.
        *   **Dual Hybrid Processing:** For our most recent high-density cohorts, I built a generative RAG pipeline to pull source transcripts alongside a dedicated opponent model tracking matrix.
        *   **Sliding Window Chunking:** The pipeline runs a chunking generator that steps across text files in 400-word blocks to stay safely inside the local transformer ceiling without dropping a single word.
        """)

    st.markdown("---")

    st.subheader("The Local Ingestion and Vector Pipeline Map")
    st.markdown("""
    1.  **Ingestion:** The script checks a global transcript cache to avoid hitches. If automated captions are missing, the system captures raw audio streams and passes them into a local whisper speech to text instance.
    2.  **Scoring Matrix:** The system loops through text slices using a specialized language model to group structural nuances into seven composite sentiment dimensions: confidence, contentment, neutrality, frustration, upset, anxiety, and surprise.
    3.  **Tabular Matrix Optimization:** The engine computes round level and series level weighted aggregates to train a Random Forest Classifier equipped with class balancing hooks.
    """)

    # Display pipeline conversion graphic with updated modern width parameter
    example_img = "assets/historical/cavaliers_aggregate_trajectory.png"
    if (os.path.exists(example_img)):
        st.image(example_img, caption="Pipeline Output: Chronological Emotional Path Conversion.", width="stretch")
    else:
        st.info("Ingestion pipeline is currently compiling live data charts.")

# Render empty redirection containers for remaining tabs
for idx, tab_title in enumerate(["Introduction", "Historical Baselines", "Modern Era Analytics", "RAG Engine", "Live Predictor", "Finals Matchup"], start=0):
    with nav_tabs[idx]:
        st.info(f"Navigate to the {tab_title} page using your app folder menu to open this functional module.")