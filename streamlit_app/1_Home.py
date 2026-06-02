import streamlit as st

st.set_page_config(page_title="2026 NBA Finals Predictor", page_icon="🏀", layout="wide", initial_sidebar_state="expanded")

# Basketball banner
st.image("https://images.unsplash.com/photo-1546519638-68e109498ffc?q=80&w=2000&auto=format&fit=crop", use_container_width=True)

st.title("2026 NBA Finals NLP Predictor (V2)")
st.subheader("Quantifying Championship Readiness Through Press Conference Emotion Vectors")

st.markdown("""
### The Question: Can we mathematically isolate a "Championship Mindset"?
While standard box scores, true shooting metrics, and defensive ratings tell you *what* happened on the court, this project captures the *human element* of a deep playoff run. By tracking how players and coaches handle intense post-game media scrutiny, this application converts text patterns into psychological markers of a title-winning team.

### What's New in the V2 Framework
*   **Dual-Model Track Architecture:** Separates an era-robust full baseline model from an optimized, ultra-rich modern-era predictive model.
*   **Multi-Role Feature Isolation:** Extracts standalone metrics across unique team roles (**Coach, Star, Teammate**) to map team-wide emotional alignments.
*   **Generative Transcript RAG Engine:** Houses a local semantic database containing thousands of chunked media paragraphs for context retrieval.
*   **Asymmetric Bracket Tracking:** Unlocks detailed runner-up bracket profiles for modern high-density data cohorts while safely tracking older scarcity eras.

### Architectural Priority: Sustainable, Lean Computing
A core priority for this build is computational efficiency. Instead of brute-forcing text scripts through heavy cloud APIs or massive, energy-intensive LLMs, this architecture relies entirely on locally executed, highly specialized small-parameter layers (like `roberta-base-go_emotions` and localized text-embedding models). It delivers deep predictive intelligence with a clean, low-overhead hardware footprint.

**(Expand the sidebar on the top left to navigate through the data pipeline stages.)**
""")