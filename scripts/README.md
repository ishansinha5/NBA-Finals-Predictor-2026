# Execution Scripts

* `data_ingestion.py`: Handles API routing and file persistence.
* `sentiment_engine.py`: Transformer execution. Implements head-truncation (2500 chars) to prevent context window bloat and isolate primary player sentiment.
* `visualization.py`: Dry execution of graphing libraries.
* `predictor.py`: Generates the Random Forest probability matrix and translates delta-weights into plain-text summaries.