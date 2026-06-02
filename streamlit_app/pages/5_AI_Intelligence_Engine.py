import streamlit as st
import os
# Check imports carefully to avoid any environment disconnects
try:
    from scripts.rag_pipeline import SportsIntelligenceRAG
except ImportError:
    SportsIntelligenceRAG = None

st.set_page_config(page_title="Interactive RAG Engine", page_icon="🏀", layout="wide")

st.title("Interactive Transcript RAG Engine")
st.subheader("Semantic Search Layer Traversing 5,762 Document Vector Nodes")

st.markdown("""
---
### Context-Augmented Dialogue Terminal
This interactive workspace directly queries your localized **ChromaDB Vector Store**. 
By chunking long-form playoff press conference media into distinct paragraphs and converting them into mathematical vectors, the system can instantly isolate what players and coaches *actually said* behind the podium.

*This premium feature is restricted to high-density modern era data (2024-2026) to maintain crisp, high-fidelity context windows.*
---
""")

if SportsIntelligenceRAG is None:
    st.error("RAG pipeline module loading failure. Ensure dependencies are correctly pinned inside your virtual environment.")
else:
    # Team scoping options
    team_scope = st.selectbox("Isolate Team Vector Group (Optional)", ["All Modern Teams", "Knicks", "Spurs", "Celtics", "Thunder", "Mavericks", "Pacers"])
    
    query_string = st.text_input(
        "Enter a technical query regarding tactical adjustments, mindset shifts, or locker room dynamics:",
        placeholder="e.g., How does the coach address defensive execution or team composure following a close road loss?"
    )
    
    if st.button("Query Vector Store Database"):
        if not query_string.strip():
            st.warning("Please type a valid question before executing the vector search database.")
        else:
            with st.spinner("Executing similarity mapping across 5,762 vector nodes inside local memory..."):
                # Pass clean tracking params
                filter_arg = None if "All" in team_scope else team_scope
                
                # Initialize the engine block
                rag_engine = SportsIntelligenceRAG()
                
                # Pull the structured context prompt block directly out of ChromaDB
                prompt_matrix = rag_engine.query_transcript_intelligence(query_string, filter_team=filter_arg)
                
                if "Vector database has not been initialized" in prompt_matrix:
                    st.error("Local vector database directory missing. Execute the pipeline in your terminal to build `./data/vector_store/` first.")
                else:
                    st.success("Semantic Context Nodes Located Successfully!")
                    
                    st.markdown("### Augmented Prompt Blueprint Generated")
                    st.markdown("This raw, fully compiled context block is what gets passed straight to your generation engine to synthesize clean answers:")
                    
                    # Output raw structural text blocks inside a scannable text frame
                    st.text_area("LangChain Retrieval Context Output:", value=prompt_matrix, height=450)