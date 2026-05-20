import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def repair_spurs_data():
    csv_path = "./data/live_2026/raw_live_2026.csv"
    
    logging.info("Loading corrupted CSV...")
    df = pd.read_csv(csv_path)
    
    # 1. Identify the rows where the schema shifted
    # (Team is Spurs AND transcript column is empty/NaN)
    spurs_mask = (df['team'] == 'Spurs') & (df['transcript'].isna())
    
    affected_rows = spurs_mask.sum()
    logging.info(f"Found {affected_rows} misaligned Spurs rows.")
    
    if affected_rows > 0:
        logging.info("Shifting transcript data into the correct column...")
        # 2. Move the mountain of text from 'won_championship' to 'transcript'
        df.loc[spurs_mask, 'transcript'] = df.loc[spurs_mask, 'won_championship']
        
        # 3. Reset the 'won_championship' column back to string "0" to pass PyArrow typing
        df.loc[spurs_mask, 'won_championship'] = "0"
        
        # 4. Save it back to disk
        df.to_csv(csv_path, index=False)
        logging.info("CSV repaired successfully! The schema is aligned.")
    else:
        logging.info("No misaligned rows found.")

if __name__ == "__main__":
    repair_spurs_data()