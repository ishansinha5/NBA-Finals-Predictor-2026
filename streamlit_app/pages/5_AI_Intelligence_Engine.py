import streamlit as st
import sys
import os

# --- BULLETPROOF ROUTING CORRECTION ---
# Forcing Python to step up to the root folder to resolve deep utility module linkages
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if (ROOT_DIR not in sys.path):
    sys.path.append(ROOT_DIR)

from utils.navigation import apply_global_styles, render_navigation

# Configure the page layout
st.set_page_config(
    page_title="Interactive RAG Engine", 
    page_icon="🏀",
    layout="wide"
)

# Apply global background configurations and render our 7-column horizontal link row
apply_global_styles()
render_navigation()

# Safely handle pipeline class imports
try:
    from scripts.rag_pipeline import SportsIntelligenceRAG
except ImportError:
    SportsIntelligenceRAG = None

# --- MAIN PAGE CONTENT ---
st.title("🏀 Interactive Transcript RAG Engine")
st.subheader("Semantic Search Layer Traversing Document Vector Nodes")
st.markdown("---")

# Technical Overview Expansion
col_left, col_right = st.columns(2)
with col_left:
    st.markdown("### Why We Implemented RAG")
    st.write(
        "Tabular classification models excel at capturing broad numerical sentiment shifts, but "
        "they strip away the qualitative, context-rich prose that defines playoff communication. "
        "If the Random Forest model flags a sudden surge in frustration, we need to locate the source. "
        "By implementing a Retrieval-Augmented Generation track, we append an evidence-gathering engine "
        "to our predictive stack. This allows us to ground our abstract mathematical insights in raw "
        "transcript verification, providing semantic accountability for our numerical predictions."
    )
with col_right:
    st.markdown("### How the Pipeline Operates")
    st.markdown("""
    * **Sliding Matrix Ingestion:** Press conference documents are partitioned into sliding 500-character segments to protect the structural continuity of multi-sentence adjustments.
    * **Vector Construction:** Passages are mathematically embedded into 384-dimensional dense arrays using a local Sentence Transformers indexer model.
    * **Similarity Mapping:** User queries are vectorized in real time and mapped using cosine distance filters to isolate the top contextual records stored inside the ChromaDB instance.
    """)

st.markdown("---")

# Anatomy of a Query Section
st.subheader("Anatomy of a High-Yield Search Query")

# Define pool of 4 targeted query examples matching our precise era scope constraints
query_pool = [
    "How does the coaching staff evaluate spatial coverage adjustments and pick-and-roll defensive schemes after dropping consecutive road matchups?",
    "What specific words do the star players use to articulate locker room cohesion and composure when facing a dominant third-quarter scoring run?",
    "Identify references to fatigue, rotational physical conditioning, and depth maintenance during back-to-back high-stakes playoff games.",
    "How do complementary teammates express cognitive strain or emotional alignment with marquee franchise stars during critical away games?"
]

# Display the example blocks inside column containers for scannability
ex_col1, ex_col2 = st.columns(2)
with ex_col1:
    st.info(f"Sample Technical Query Alpha:\n\n*\"{query_pool[0]}\"*")
with ex_col2:
    st.info(f"Sample Technical Query Beta:\n\n*\"{query_pool[1]}\"*")

# Query criteria rules
rule_col1, rule_col2 = st.columns(2)
with rule_col1:
    st.markdown("#### What Makes a Query Work")
    st.markdown("""
    * **Focus on Specific Adjustments:** Use precise terminology like 'rotations', 'schemes', 'composure', or 'execution'.
    * **Target Organizational Layers:** Specify who you are evaluating ('coaching staff', 'teammates', 'starters').
    * **Incorporate Series Context:** Reference historical scenarios to hit relevant vector clusters.
    """)
with rule_col2:
    st.markdown("#### What Makes a Query Fail")
    st.markdown("""
    * **Asking for Direct Box Scores:** Searching specific numeric stats fails because vector indexes evaluate conceptual sentiment context, not deterministic database metrics.
    * **Broad, Ambiguous Text Entries:** General queries map to thousands of loose nodes, washing out the specificity of your retrieval block.
    * **Speculative Projections:** Asking for an open prediction returns historical instances of confidence or anxiety rather than a absolute future projection.
    """)

st.markdown("---")

# The Live Execution Terminal
st.subheader("Context-Augmented Dialogue Terminal")

if (SportsIntelligenceRAG is None):
    st.error("RAG pipeline module loading failure. Ensure dependencies are correctly pinned inside your virtual environment.")
else:
    # Team scoping options restricted strictly to our verified team scope footprints
    team_scope = st.selectbox(
        "Isolate Team Vector Group (Optional Filter)", 
        ["All Modern Teams", "Knicks", "Spurs", "Celtics", "Thunder", "Mavericks", "Pacers"]
    )
    
    query_string = st.text_input(
        "Enter your structured query regarding tactical variables or emotional alignment:",
        placeholder="Type your question here..."
    )
    
    if st.button("Query Vector Store Database"):
        if (not query_string.strip()):
            st.warning("Please type a valid question before executing the vector search database.")
        else:
            with st.spinner("Executing similarity mapping across vector nodes inside local memory..."):
                filter_arg = None
                if ("All" not in team_scope):
                    filter_arg = team_scope
                
                # Initialize the engine block module
                rag_engine = SportsIntelligenceRAG()
                
                # Pull the structured context prompt block directly out of ChromaDB storage targets
                prompt_matrix = rag_engine.query_transcript_intelligence(query_string, filter_team=filter_arg)
                
                if ("Vector database has not been initialized" in prompt_matrix):
                    st.error("Local vector database directory missing. Execute the pipeline in your terminal to build `./data/vector_store/` first.")
                else:
                    st.success("Semantic Context Nodes Located Successfully!")
                    st.markdown("#### Augmented Prompt Blueprint Generated")
                    st.write("This structured text matrix contains the exact historical quotes retrieved from ChromaDB, optimized for synthesis:")
                    
                    # Output raw structural text blocks inside a clean text area
                    st.text_area("LangChain Retrieval Context Output:", value=prompt_matrix, height=400)