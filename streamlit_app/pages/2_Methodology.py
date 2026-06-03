import streamlit as st
import base64
import os

st.set_page_config(
    page_title="Design Journey", 
    page_icon="🏀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

def get_base64_bg(img_name):
    # Step up one directory from pages/ to find the image in streamlit_app/
    img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), img_name)
    if (os.path.exists(img_path)):
        with open(img_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return f"data:image/jpg;base64,{encoded_string}"
    return ""

bg_base64 = get_base64_bg("image_04fa1b.jpg")

if (bg_base64):
    st.markdown(f"""
        <style>
            [data-testid="stSidebar"] {{ display: none; }}
            [data-testid="stAppViewContainer"] {{
                background: linear-gradient(rgba(11, 26, 48, 0.85), rgba(11, 26, 48, 0.95)), url("{bg_base64}");
                background-size: cover; background-position: center; background-attachment: fixed;
            }}
            [data-testid="stHeader"] {{ background-color: transparent; }}
            html, body, [class*="st-"], h1, h2, h3, h4, p, span, div, li {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("<style>[data-testid='stSidebar'] { display: none; } [data-testid='stAppViewContainer'] { background-color: #0b1a30; } [data-testid='stHeader'] { background-color: transparent; }</style>", unsafe_allow_html=True)

st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

nav_tabs = st.tabs([
    "Introduction", "Historical Baselines", "Modern Era Analytics", 
    "RAG Engine", "Live Predictor", "Finals Matchup", "Engineering Journey"
])

# Engineering content belongs in the 7th tab (index 6)
with nav_tabs[6]:
    st.header("The Architectural Evolution: V1 vs. V2")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Legacy V1 Paradigm: Proof of Concept")
        st.markdown("""
        * **Restricted Data:** Evaluated only two years of data.
        * **Linguistic Truncation:** Used hard truncation, which missed context.
        * **Tabular Blind Spot:** Lacked granular multi-role separation.
        * **Survival Bias:** Only trained on Finals teams, missing early exit dynamics.
        """)

    with col2:
        st.markdown("### Upgraded V2 Framework: Production Pipeline")
        st.markdown("""
        * **Preservation of the Score Filter:** I intentionally stop collecting transcript data exactly one game before a playoff series is decided. This prevents the anomalous emotional spikes inherent in series-clinching celebrations from skewing our training baselines.
        * **Tri-Tier Role Isolation:** The matrix separates team dynamics across three roles: coaches, star players, and role players.
        * **Multi-Season Scaling:** The pipeline includes older seasons to broaden baselines.
        * **Dual Hybrid Processing:** Integrated a generative RAG pipeline alongside a dedicated opponent model.
        """)

# Map out routing for the other tabs back to their source pages
page_routes = [
    (0, "../1_Home.py", "Introduction"),
    (1, "3_Historical_Analysis.py", "Historical Baselines"),
    (2, "4_Modern_Era_Analytics.py", "Modern Era Analytics"),
    (3, "5_AI_Intelligence_Engine.py", "RAG Engine"),
    (4, "6_2026_Finals_Predictor.py", "Live Predictor"),
    (5, "7_Finals_Matchup.py", "Finals Matchup")
]

for idx, page_path, tab_title in page_routes:
    with nav_tabs[idx]:
        st.info(f"Explore the {tab_title} module.")
        st.page_link(page_path, label=f"Open {tab_title}", icon="🏀")