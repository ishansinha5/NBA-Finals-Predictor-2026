import os
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SportsIntelligenceRAG:
    def __init__(self, persist_directory="./data/vector_store/"):
        self.persist_directory = persist_directory
        # Local free, highly resilient zero-overhead embedding architecture
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.vector_store = None

    def build_vector_database(self, data_directory="./data/historical/"):
        """Scans specified files to build the vector store."""
        logging.info("Initializing vectorization pipeline for modern era profiles...")
        
        # Strictly scope to the 2024, 2025 and future 2026 dataset footprints
        allowed_files = ["scored_2023_2024.csv", "scored_2024_2025.csv", "scored_2025_2026.csv"]
        all_documents = []
        metadata_list = []
        
        for file_target in allowed_files:
            filepath = os.path.join(data_directory, file_target)
            if (not os.path.exists(filepath)):
                continue
                
            df = pd.read_csv(filepath)
            for idx, row in df.iterrows():
                transcript = str(row['transcript'])
                # Segment raw texts into semantic paragraphs
                chunks = self.text_splitter.split_text(transcript)
                
                for chunk in chunks:
                    all_documents.append(chunk)
                    metadata_list.append({
                        "team": row['team'],
                        "stage": row['stage'],
                        "role": row['role'],
                        "source_file": file_target
                    })
                    
        if (not all_documents):
            logging.warning("No documents matched the premium vectorization scope constraints.")
            return False
            
        logging.info(f"Embedding {len(all_documents)} text chunks into local storage...")
        self.vector_store = Chroma.from_texts(
            texts=all_documents,
            metadatas=metadata_list,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        logging.info("Vector database compilation successful.")
        return True

    def query_transcript_intelligence(self, user_query, filter_team=None):
        """Retrieves exact relevant text paragraphs to augment context blocks"""
        if (self.vector_store is None):
            if (os.path.exists(self.persist_directory)):
                self.vector_store = Chroma(persist_directory=self.persist_directory, embedding_function=self.embeddings)
            else:
                return "Vector database has not been initialized yet."
                
        kwargs = {}
        if (filter_team):
            kwargs["filter"] = {"team": filter_team}
            
        # Extract the top 4 most relevant text blocks from the transcripts
        search_results = self.vector_store.similarity_search(user_query, k=4, **kwargs)
        
        # Build prompt context block
        context_block = "\n---\n".join([f"[{doc.metadata['team']} - {doc.metadata['stage']} - {doc.metadata['role']}]: {doc.page_content}" for doc in search_results])
        
        # This augmented block gets passed directly to an LLM completion interface inside your Streamlit UI
        augmented_prompt = f"""
        You are an expert sports intelligence system. Answer the query based strictly on the provided playoff media transcripts.
        If the transcript details do not contain information to answer the question, state that clearly.
        
        Context:
        {context_block}
        
        Question: {user_query}
        Answer:"""
        
        return augmented_prompt