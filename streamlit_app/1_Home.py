import streamlit as st

# Configure the page layout and strictly collapse the vertical sidebar navigation
st.set_page_config(
    page_title="2026 NBA Finals NLP Predictor", 
    page_icon="🏀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Custom CSS to inject to further clean up the default sidebar elements if necessary
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Main Header Banner
st.title("🏀 NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Horizontal Navigation Bar matching image_aa0064.png
# Since the application spans multiple functional modules, this central hub guides the user.
nav_tabs = st.tabs([
    "🏠 Introduction & Overview", 
    "👔 Multi-Role Analytics", 
    "🧠 Interactive RAG Engine", 
    "🔮 2026 Finals Live Predictor",
    "📝 Engineering Journey"
])

# Render the Home/Introduction content within the primary horizontal viewport slot
with nav_tabs[0]:
    
    # Hero Visual Section
    st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop", use_container_width=True)
    
    st.markdown("## Project Motivation")
    st.markdown("""
    Traditional sports analytics relies heavily on box-score tracking—field goal percentages, defensive ratings, and true shooting efficiency metrics. While these data columns reveal *what* happened on the hardwood, they fail to track the underlying cognitive and psychological vectors governing an active locker room under championship pressure. 
    
    This platform maps text data harvested straight from podium media sessions into high-dimensional emotional signatures, discovering whether the linguistic composure of key stakeholders serves as a leading indicator for winning the Larry O'Brien trophy.
    """)
    
    st.markdown("---")
    
    st.markdown("## Comprehensive Project Core Architecture")
    st.markdown("""
    The system processes language data across two major core phases to build a unified sports intelligence repository:
    
    ### 📊 Phase 1: High-Fidelity Tabular Predictive Modeling
    *   **Automated Audio Ingestion:** An automated pipeline maps game markers to YouTube video keys, pulling official closed captions or proxying headless media streams into a localized speech-to-text instance.
    *   **Emotional Vector Mapping:** Chunks and parses post-game scripts across a transformer model trained to track nuanced vocal dynamics, establishing scalar readings for: *Confidence, Contentment, Neutrality, Frustration, Upset, Anxiety, and Surprise*.
    *   **Dual-Track Classification:** Feeds downstream machine learning layers, optimizing a robust Full Historical Baseline Model paired with an isolated, high-density Modern-Era Track to track how performance mindsets shift across varying media settings.
    *   **Inter-Role Behavioral Isolation:** Flattens metrics independently across core organizational layers—maintaining explicit data pipelines for the **Head Coach**, the **Marquee Star**, and the **Supporting Teammates**.
    
    ### 🧠 Phase 2: Generative Context & Retrieval Augmentation (RAG)
    *   **Semantic Vector Matrix:** Slices raw media transcript files into sliding token windows to preserve the continuity of deep analytical statements.
    *   **ChromaDB Vector Store Embedding:** Maps text sequences into a high-density, multi-thousand-node semantic index cache, enabling instant localized vector lookup by team, player type, or playoff series context.
    *   **Recruiter Query Hub:** Supplies a dialogue terminal that isolates exactly what tactical or psychological shifts occurred following high-stakes wins or road losses without manual document reviewing.
    """)
    
    st.markdown("---")
    
    st.markdown("## Architectural Priority: Sustainable, Hardware-Aware Computing")
    st.markdown("""
    A foundational design pillar of this infrastructure is **Green AI**—maximizing structural, local prediction capability while intentionally minimizing environmental resource consumption. 
    
    Instead of passing heavy processing calls to massive, multi-billion parameter third-party APIs or running expensive cloud data scripts that inflate computing overhead, this pipeline utilizes a hardware-aware profiling pipeline engineered for a lean VRAM footprint and strict carbon reduction.
    
    *   **Edge Transformers:** Core parsing is executed through small-parameter local layers (like `roberta-base-go_emotions` and localized embedding matrices), compressing massive language sequences down to deterministic floating-point feature records at zero network toll.
    *   **Compute Footprint Minimization:** The preprocessing loops use optimized sliding context generators to stay safely within memory boundaries, extracting deep semantic structures directly on consumer-grade CPU and GPU rigs.
    *   **Optimized Local DB Architecture:** Utilizing file-mapped binary indices ensures retrieval latency drops to a fraction of a millisecond, completely bypassing heavy background infrastructure requirements.
    """)

# Render empty or redirect notices for the remaining tabs to help users click through the header row
for i, tab_title in enumerate(["Multi-Role Analytics", "Interactive RAG Engine", "2026 Finals Live Predictor", "Engineering Journey"], start=1):
    with nav_tabs[i]:
        st.info(f"Navigate to the **{tab_title}** page using your application workspace settings or custom link matrices to access the full system sub-modules.")