import streamlit as st
import os
import random

# Configure the page layout and strictly collapse the vertical sidebar navigation
st.set_page_config(
    page_title="Interactive RAG Engine", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Injected CSS to match the vertical sidebar suppression across the app
st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Safely handle pipeline class imports
try:
    from scripts.rag_pipeline import SportsIntelligenceRAG
except ImportError:
    SportsIntelligenceRAG = None

# Main Header
st.title("NBA Post-Game NLP Engine: Decoding Championship Psychology")
st.markdown("---")

# Horizontal Navigation Bar
nav_tabs = st.tabs([
    "Introduction & Overview", 
    "Multi-Role Analytics", 
    "Interactive RAG Engine", 
    "2026 Finals Live Predictor",
    "Engineering Journey"
])

# Route all content directly into the 3rd tab (Interactive RAG Engine)
with nav_tabs[2]:
    st.header("Interactive Transcript RAG Engine")
    st.subheader("Semantic Search Layer Traversing 5,762 Document Vector Nodes")
    st.markdown("---")

    # Technical Overview Expansion
    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("### Why We Implemented RAG")
        st.markdown("""
        Tabular classification models excel at capturing broad numerical sentiment shifts, but they strip away the qualitative, context-rich prose that defines playoff communication. If the Random Forest flags a surge in frustration, we need to understand the source. 
        
        By implementing a Retrieval-Augmented Generation track, we append an evidence-gathering engine to our predictive stack. This allows us to ground our abstract mathematical insights in raw transcript verification, providing semantic accountability for our numerical predictions.
        """)
    with col_right:
        st.markdown("### How the Pipeline Operates")
        st.markdown("""
        *   **Sliding Matrix Ingestion:** Press conference documents are partitioned into sliding 400-word segments to protect the structural continuity of multi-sentence adjustments.
        *   **Vector Construction:** Passages are mathematically embedded into 384-dimensional dense arrays using a local Sentence Transformers indexer.
        *   **Similarity Mapping:** User queries are vectorized in real time and mapped using cosine distance filters to isolate the top contextual records stored inside the ChromaDB instance.
        """)

    st.markdown("---")

    # Anatomy of a Query Section
    st.subheader("Anatomy of a High-Yield Search Query")
    
    # Define pool of 8 technical example queries
    query_pool = [
        "How does the coaching staff evaluate spatial coverage adjustments and pick-and-roll defensive schemes after dropping consecutive road matchups?",
        "What specific words do the star players use to articulate locker room cohesion and composure when facing a dominant third-quarter scoring run?",
        "Identify references to fatigue, rotational physical conditioning, and depth maintenance during back-to-back high-stakes playoff games.",
        "How does team language shift regarding officiating, free throw disparity, and referee performance following an elimination loss?",
        "What linguistic markers indicate coach tactical stubbornness or willingness to completely alter bench patterns mid-series?",
        "Trace player accountability responses when evaluating personal high-turnover margins or poor true-shooting percentages at the podium.",
        "How do complementary role players express cognitive strain or emotional alignment with marquee franchise stars during critical away games?",
        "Examine the text records for indications of championship complacency or heightened collective focus following a blowout victory."
    ]

    # Initialize session state for random query selection to preserve selections across input ticks
    if "selected_examples" not in st.session_state:
        st.session_state.selected_examples = random.sample(query_pool, 2)

    # Button to allow refreshing the random selections manually
    if st.button("Rotate Example Queries"):
        st.session_state.selected_examples = random.sample(query_pool, 2)

    # Display the two current example blocks inside column containers
    ex_col1, ex_col2 = st.columns(2)
    with ex_col1:
        st.info(f"Sample Technical Query Alpha:\n\n*\"{st.session_state.selected_examples[0]}\"*")
    with ex_col2:
        st.info(f"Sample Technical Query Beta:\n\n*\"{st.session_state.selected_examples[1]}\"*")

    # Query criteria rules
    rule_col1, rule_col2 = st.columns(2)
    with rule_col1:
        st.markdown("#### What Makes a Query Work")
        st.markdown("""
        *   **Focus on Specific Adjustments:** Use precise terminology like 'rotations', 'schemes', 'composure', or 'execution'.
        *   **Target Organizational Layers:** Specify who you are evaluating ('coaching staff', 'role players', 'starters').
        *   **Incorporate Series Context:** Reference historical scenarios ('blown double-digit leads', 'consecutive away losses') to hit relevant vector clusters.
        """)
    with rule_col2:
        st.markdown("#### What Makes a Query Fail")
        st.markdown("""
        *   **Asking for Direct Box Scores:** Searching 'Who scored 30 points in game 3?' fails because vector indexes evaluate conceptual sentiment context, not deterministic database metrics.
        *   **Broad, Ambiguous Text Entries:** Queries like 'tell me about the game' map to thousands of loose nodes, washing out the specificity of your retrieval block.
        *   **Speculative Projections:** Asking 'Will the Knicks win tonight?' returns historical instances of confidence or anxiety rather than a crystal ball.
        """)

    st.markdown("---")

    # The Live Execution Terminal
    st.subheader("Context-Augmented Dialogue Terminal")
    
    if SportsIntelligenceRAG is None:
        st.error("RAG pipeline module loading failure. Ensure dependencies are correctly pinned inside your virtual environment.")
    else:
        # Team scoping options
        team_scope = st.selectbox(
            "Isolate Team Vector Group (Optional Filter)", 
            ["All Modern Teams", "Knicks", "Spurs", "Celtics", "Thunder", "Mavericks", "Pacers"]
        )
        
        query_string = st.text_input(
            "Enter your structured query regarding tactical variables or emotional alignment:",
            placeholder="Type your question here..."
        )
        
        if st.button("Query Vector Store Database"):
            if not query_string.strip():
                st.warning("Please type a valid question before executing the vector search database.")
            else:
                with st.spinner("Executing similarity mapping across 5,762 vector nodes inside local memory..."):
                    # Pass clean tracking parameters
                    filter_arg = None if "All" in team_scope else team_scope
                    
                    # Initialize the engine block
                    rag_engine = SportsIntelligenceRAG()
                    
                    # Pull the structured context prompt block directly out of ChromaDB
                    prompt_matrix = rag_engine.query_transcript_intelligence(query_string, filter_team=filter_arg)
                    
                    if "Vector database has not been initialized" in prompt_matrix:
                        st.error("Local vector database directory missing. Execute the pipeline in your terminal to build `./data/vector_store/` first.")
                    else:
                        st.success("Semantic Context Nodes Located Successfully!")
                        st.markdown("#### Augmented Prompt Blueprint Generated")
                        st.markdown("This structured raw text matrix contains the exact historical quotes retrieved from ChromaDB, optimized for synthesis:")
                        
                        # Output raw structural text blocks inside a scannable text frame
                        st.text_area("LangChain Retrieval Context Output:", value=prompt_matrix, height=400)

# Informational placeholders for other horizontal tabs
for idx, tab_title in enumerate(["Introduction & Overview", "Multi-Role Analytics", "2026 Finals Live Predictor", "Engineering Journey"]):
    # Adjust index to route around the active tab slot smoothly
    target_idx = idx if idx < 2 else idx + 1
    with nav_tabs[target_idx]:
        st.info(f"Navigate to the respective sub-file to view the full {tab_title} interface.")