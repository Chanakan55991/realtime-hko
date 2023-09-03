import streamlit as st
import pandas as pd

@st.cache_data
def prepare_data():
    cold_df = pd.read_csv('https://www.hko.gov.hk/dps/wxinfo/climat/warndb/cold.dat', sep='\t', header=None)
    rs_df = pd.read_csv('https://www.hko.gov.hk/dps/wxinfo/climat/warndb/rstorm.dat', sep='\t', header=None)

    column_mapping_cold = {0: 'start_year', 1: 'start_month', 2: 'start_date', 3: 'start_hour', 4: 'start_minute', 5: 'end_year', 6: 'end_month', 7: 'end_date', 8: 'end_hour', 9: 'end_minute'}
    column_mapping_rs = {0: 'warnings', 1: 'start_year', 2: 'start_month', 3: 'start_date', 4: 'start_hour', 5: 'start_minute', 6: 'end_year', 7: 'end_month', 8: 'end_date', 9: 'end_hour', 10: 'end_minute'}

    # Rename the columns using the dictionary
    cold_df.rename(columns=column_mapping_cold, inplace=True)
    rs_df.rename(columns=column_mapping_rs, inplace=True)

    rs_df_cleaned = rs_df.dropna(subset=11)
    cold_cleaned = cold_df.dropna(subset=11)
    return (rs_df_cleaned, cold_cleaned)

def process_data(hko_df_list):
    for df in hko_df_list:
        df['start_hour'] = df['start_hour'].replace(24, 0)
        df['end_hour'] = df['end_hour'].replace(24, 0)
        df['start_datetime'] = pd.to_datetime(df['start_year'].astype(int).astype(str) + '/' + df['start_month'].astype(int).astype(str) + '/' + df['start_date'].astype(int).astype(str) + ' ' +  df['start_hour'].astype(int).astype(str) + ':' + df['start_minute'].astype(int).astype(str))
        df['end_datetime'] = pd.to_datetime(df['end_year'].astype(int).astype(str) + '/' + df['end_month'].astype(int).astype(str) + '/' + df['end_date'].astype(int).astype(str) + ' ' +  df['end_hour'].astype(int).astype(str) + ':' + df['end_minute'].astype(int).astype(str))


    return hko_df_list
