import pandas as pd
import logging

# importing my custom tools from the scripts folder
from scripts.data_ingestion import TranscriptIngestor
from scripts.sentiment_engine import SentimentEngine
from scripts.visualization import EmotionVisualizer

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    logging.info("Starting the 2026 NBA Finals NLP Pipeline...")
    logging.info("PHASE 2: Generating Historical Training Data")
    
    # Step 1: Define the videos we want to analyze
    # writing out every single video completely expanded so I can edit them easily if needed
    video_list = []
    
    # --- REGULAR SEASON ---
    
    vid1 = {}
    vid1['video_id'] = 'ti_MxSneUfg'
    vid1['team'] = 'Celtics'
    vid1['stage'] = 'Reg Season - Pistons'
    vid1['won_series'] = 1
    video_list.append(vid1)

    vid2 = {}
    vid2['video_id'] = '7b7Aymnhk7I'
    vid2['team'] = 'Celtics'
    vid2['stage'] = 'Reg Season - Pistons'
    vid2['won_series'] = 1
    video_list.append(vid2)

    vid3 = {}
    vid3['video_id'] = 'KIfVcS0O7j0'
    vid3['team'] = 'Celtics'
    vid3['stage'] = 'Reg Season - Bulls'
    vid3['won_series'] = 1
    video_list.append(vid3)

    vid4 = {}
    vid4['video_id'] = '6PG2NJXXepY'
    vid4['team'] = 'Bulls'
    vid4['stage'] = 'Reg Season - Celtics'
    vid4['won_series'] = 0
    video_list.append(vid4)

    vid5 = {}
    vid5['video_id'] = '39XuThBt5Nw'
    vid5['team'] = 'Lakers'
    vid5['stage'] = 'Reg Season - Celtics'
    vid5['won_series'] = 0
    video_list.append(vid5)

    vid6 = {}
    vid6['video_id'] = 'pgUHDN1XmHQ'
    vid6['team'] = 'Celtics'
    vid6['stage'] = 'Reg Season - Nuggets'
    vid6['won_series'] = 1
    video_list.append(vid6)

    vid7 = {}
    vid7['video_id'] = 'vjrBZ4FFpYc'
    vid7['team'] = 'Celtics'
    vid7['stage'] = 'Reg Season - Nuggets'
    vid7['won_series'] = 1
    video_list.append(vid7)

    vid8 = {}
    vid8['video_id'] = 'qT66693Llmg'
    vid8['team'] = 'Thunder'
    vid8['stage'] = 'Reg Season - Celtics'
    vid8['won_series'] = 0
    video_list.append(vid8)

    # --- PLAYOFFS ROUND 1 (HEAT) ---

    vid9 = {}
    vid9['video_id'] = '-0-cX7BB6HE'
    vid9['team'] = 'Celtics'
    vid9['stage'] = 'R1G1'
    vid9['won_series'] = 1
    video_list.append(vid9)

    vid10 = {}
    vid10['video_id'] = 'w0MIt0xm1FI'
    vid10['team'] = 'Celtics'
    vid10['stage'] = 'R1G1'
    vid10['won_series'] = 1
    video_list.append(vid10)

    vid11 = {}
    vid11['video_id'] = 'iQIhTOwAa84'
    vid11['team'] = 'Celtics'
    vid11['stage'] = 'R1G2'
    vid11['won_series'] = 1
    video_list.append(vid11)

    vid12 = {}
    vid12['video_id'] = 'fHrRy6SWeFo'
    vid12['team'] = 'Celtics'
    vid12['stage'] = 'R1G2'
    vid12['won_series'] = 1
    video_list.append(vid12)

    vid13 = {}
    vid13['video_id'] = 'o6Zreg31N8I'
    vid13['team'] = 'Celtics'
    vid13['stage'] = 'R1G3'
    vid13['won_series'] = 1
    video_list.append(vid13)

    vid14 = {}
    vid14['video_id'] = '-qWwewRfhuE'
    vid14['team'] = 'Celtics'
    vid14['stage'] = 'R1G3'
    vid14['won_series'] = 1
    video_list.append(vid14)

    vid15 = {}
    vid15['video_id'] = 'ctco1Ui3fOU'
    vid15['team'] = 'Celtics'
    vid15['stage'] = 'R1G4'
    vid15['won_series'] = 1
    video_list.append(vid15)

    vid16 = {}
    vid16['video_id'] = 'aY8op4mgj7k'
    vid16['team'] = 'Celtics'
    vid16['stage'] = 'R1G4'
    vid16['won_series'] = 1
    video_list.append(vid16)

    vid17 = {}
    vid17['video_id'] = 'VgV8aawoZiQ'
    vid17['team'] = 'Celtics'
    vid17['stage'] = 'R1G5'
    vid17['won_series'] = 1
    video_list.append(vid17)

    vid18 = {}
    vid18['video_id'] = 'TKU-ZWqXUzc'
    vid18['team'] = 'Celtics'
    vid18['stage'] = 'R1G5'
    vid18['won_series'] = 1
    video_list.append(vid18)

    # --- PLAYOFFS ROUND 2 (CAVS) ---

    vid19 = {}
    vid19['video_id'] = '5xNDL6oPZVI'
    vid19['team'] = 'Celtics'
    vid19['stage'] = 'R2G1'
    vid19['won_series'] = 1
    video_list.append(vid19)

    vid20 = {}
    vid20['video_id'] = '3g5UEYTjbMs'
    vid20['team'] = 'Celtics'
    vid20['stage'] = 'R2G1'
    vid20['won_series'] = 1
    video_list.append(vid20)

    vid21 = {}
    vid21['video_id'] = '6APEN2sIOzA'
    vid21['team'] = 'Cavs'
    vid21['stage'] = 'R2G2'
    vid21['won_series'] = 0
    video_list.append(vid21)

    vid22 = {}
    vid22['video_id'] = '2_irJPsEvOI'
    vid22['team'] = 'Cavs'
    vid22['stage'] = 'R2G2'
    vid22['won_series'] = 0
    video_list.append(vid22)

    vid23 = {}
    vid23['video_id'] = 'gfdjYLlT7zY'
    vid23['team'] = 'Celtics'
    vid23['stage'] = 'R2G3'
    vid23['won_series'] = 1
    video_list.append(vid23)

    vid24 = {}
    vid24['video_id'] = 's7v-QiXbuEg'
    vid24['team'] = 'Cavs'
    vid24['stage'] = 'R2G3'
    vid24['won_series'] = 0
    video_list.append(vid24)

    vid25 = {}
    vid25['video_id'] = 'ai7cK0Tk260'
    vid25['team'] = 'Celtics'
    vid25['stage'] = 'R2G4'
    vid25['won_series'] = 1
    video_list.append(vid25)

    vid26 = {}
    vid26['video_id'] = 'C_IWik5LI5g'
    vid26['team'] = 'Cavs'
    vid26['stage'] = 'R2G4'
    vid26['won_series'] = 0
    video_list.append(vid26)

    vid27 = {}
    vid27['video_id'] = 'iSYEBhKykaw'
    vid27['team'] = 'Celtics'
    vid27['stage'] = 'R2G5'
    vid27['won_series'] = 1
    video_list.append(vid27)

    vid28 = {}
    vid28['video_id'] = 'QI1dI5z7qB4'
    vid28['team'] = 'Celtics'
    vid28['stage'] = 'R2G5'
    vid28['won_series'] = 1
    video_list.append(vid28)

    # --- PLAYOFFS ROUND 3 (PACERS) ---

    vid29 = {}
    vid29['video_id'] = 'JWlldi545W4'
    vid29['team'] = 'Celtics'
    vid29['stage'] = 'R3G1'
    vid29['won_series'] = 1
    video_list.append(vid29)

    vid30 = {}
    vid30['video_id'] = 'p_fz4zuaebk'
    vid30['team'] = 'Pacers'
    vid30['stage'] = 'R3G1'
    vid30['won_series'] = 0
    video_list.append(vid30)

    vid31 = {}
    vid31['video_id'] = '7vw73RqXEtI'
    vid31['team'] = 'Celtics'
    vid31['stage'] = 'R3G2'
    vid31['won_series'] = 1
    video_list.append(vid31)

    vid32 = {}
    vid32['video_id'] = 'lr9XK78gEiI'
    vid32['team'] = 'Pacers'
    vid32['stage'] = 'R3G2'
    vid32['won_series'] = 0
    video_list.append(vid32)

    vid33 = {}
    vid33['video_id'] = 'UG-1VQVspq8'
    vid33['team'] = 'Celtics'
    vid33['stage'] = 'R3G3'
    vid33['won_series'] = 1
    video_list.append(vid33)

    vid34 = {}
    vid34['video_id'] = '2Zj-VQh15ak'
    vid34['team'] = 'Pacers'
    vid34['stage'] = 'R3G3'
    vid34['won_series'] = 0
    video_list.append(vid34)

    vid35 = {}
    vid35['video_id'] = 'tRAGilUcgDk'
    vid35['team'] = 'Celtics'
    vid35['stage'] = 'R3G4'
    vid35['won_series'] = 1
    video_list.append(vid35)

    vid36 = {}
    vid36['video_id'] = 'g_JGuPGruNQ'
    vid36['team'] = 'Celtics'
    vid36['stage'] = 'R3G4'
    vid36['won_series'] = 1
    video_list.append(vid36)

    # Step 2: Ingest the data
    logging.info("--- Phase 1: Data Ingestion (Historical) ---")
    
    # updating the path to point to the historical folder based on my new decompressed architecture
    ingestor = TranscriptIngestor(data_dir="./data/historical/")
    raw_df = ingestor.fetch_transcripts(video_list)
    
    if (raw_df.empty == True):
        logging.error("We didn't get any data! Stopping the pipeline.")
        return
    
    # saving the raw historical data
    ingestor.save_to_csv(raw_df, "raw_historical.csv")
    
    # Step 3: Run the Sentiment Engine
    logging.info("--- Phase 2: Sentiment Analysis (Historical) ---")
    engine = SentimentEngine()
    scored_df = engine.process_dataframe(raw_df)
    
    # saving the scored historical data so I can use it to train the Random Forest
    ingestor.save_to_csv(scored_df, "scored_historical.csv")
    
    # Step 4: Visualize the results
    # commenting this out for now because we don't need graphs of old data, we just need the csv for the AI
    # logging.info("--- Phase 3: Visualization ---")
    # visualizer = EmotionVisualizer(output_dir="./output/")
    # teams_to_graph = []
    # teams_to_graph.append('Celtics')
    # for team in teams_to_graph:
    #     visualizer.plot_time_series(scored_df, team)
        
    logging.info("Historical data pipeline finished successfully! Ready to train the Random Forest.")

if (__name__ == "__main__"):
    main()