import streamlit as st

st.set_page_config(page_title="Conclusion", page_icon="🏀", layout="wide", initial_sidebar_state="collapsed")

st.title("The 2026 Prediction")

st.markdown("### And the winner is...")

# Centered column layout for maximum impact
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("streamlit_app/assets/New-York-Knicks-logo.png", use_container_width=True)
    st.markdown("<h1 style='text-align: center; font-size: 4.5em;'>NEW YORK KNICKS</h1>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
Based on the NLP analysis of the 2026 playoffs to date, the New York Knicks possess the strongest championship psychology. 

When mapped against the stoic, business-like demeanors of the 2024 Celtics and 2025 Thunder, the Knicks display the exact mix of high Neutrality and muted, stable Confidence that the Random Forest algorithm recognizes as a title-winning team. 

Conversely, highly emotional teams (like the young Spurs, who display massive spikes in raw Confidence and Frustration) are heavily penalized by the model. 

### Final Thoughts
This project was a massive leap from traditional box-score analysis into the world of Machine Learning and NLP. While stats tell you *what* happened on the court, language models can give us a glimpse into *how* the players are processing the pressure. 
""")