# I use this script locally to dig out the quotes I want to feature on the website
from scripts.rag_pipeline import SportsIntelligenceRAG

if (__name__ == "__main__"):
    # Initialize our engine
    rag = SportsIntelligenceRAG()
    
    # Type the question you want to test here
    test_question = "How do the stars articulate their confidence levels?"
    
    # We can filter by team, or leave it None
    prompt_blueprint = rag.query_transcript_intelligence(test_question, filter_team="Spurs")
    
    print("\n--- RAW NODES FOUND ---")
    print(prompt_blueprint)