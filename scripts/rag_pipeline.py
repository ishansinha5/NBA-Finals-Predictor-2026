import os
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

class SportsIntelligenceRAG:
    def __init__(self, persist_directory=None):
        # We enforce an absolute lookup path to the directory shown in image_856009.png
        if (persist_directory is None):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.persist_directory = os.path.abspath(os.path.join(base_dir, "data", "vector_store"))
        else:
            self.persist_directory = os.path.abspath(persist_directory)
            
        # Local, lightweight embedding model requiring zero cloud API dependencies
        self.embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        self.vector_store = None

    def build_vector_database(self, data_directory=None):
        logging.info("Initializing vectorization pipeline for modern era profiles...")
        
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Gathering our target modern files across all verified footprints
        allowed_files = ["scored_2023_2024.csv", "scored_2024_2025.csv", "scored_2025_2026.csv"]
        
        # Set up an expansive tracking array to handle alternate storage coordinates
        possible_dirs = [
            os.path.join(base_dir, "data", "historical"),
            os.path.join(base_dir, "data", "live_2026"),
            base_dir,
            os.getcwd()
        ]
            
        all_documents = []
        metadata_list = []
        
        for file_target in allowed_files:
            file_found = False
            filepath = ""
            
            for check_dir in possible_dirs:
                test_path = os.path.join(check_dir, file_target)
                if (os.path.exists(test_path) == True):
                    filepath = test_path
                    file_found = True
                    break
                    
            if (file_found == True):
                df = pd.read_csv(filepath)
                
                for idx, row in df.iterrows():
                    transcript = str(row['transcript'])
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
            
        logging.info(f"Embedding {len(all_documents)} text chunks into local storage targets...")
        self.vector_store = Chroma.from_texts(
            texts=all_documents,
            metadatas=metadata_list,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )
        
        logging.info(f"Vector database compilation successful. Locked at: {self.persist_directory}")
        return True

    def query_transcript_intelligence(self, user_query, filter_team=None):
        if (self.vector_store is None):
            if (os.path.exists(self.persist_directory) == True):
                self.vector_store = Chroma(
                    persist_directory=self.persist_directory, 
                    embedding_function=self.embeddings
                )
            else:
                return f"Vector database has not been initialized yet. Missing path: {self.persist_directory}"
                
        kwargs = {}
        if (filter_team != None):
            kwargs["filter"] = {"team": filter_team}
            
        # Extract the top 4 most conceptually relevant text snippets from the database
        search_results = self.vector_store.similarity_search(user_query, k=4, **kwargs)
        
        context_items = []
        for doc in search_results:
            item = f"[{doc.metadata['team']} - {doc.metadata['stage']} - {doc.metadata['role']}]: {doc.page_content}"
            context_items.append(item)
            
        context_block = "\n---\n".join(context_items)
        
        augmented_prompt = f"""You are an expert sports intelligence system. Answer the query based strictly on the provided playoff media transcripts.
If the transcript details do not contain information to answer the question, state that clearly.

Context:
{context_block}

Question: {user_query}
Answer:"""
        
        return augmented_prompt