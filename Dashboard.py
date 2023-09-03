from datetime import date, timedelta
import time
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils import *

st.set_page_config(layout='centered')


st.title("HKO Real-Time Warning & Signals")


processed_warnings = process_data(prepare_data())

warnings_today_count = 0

rs_today_warnings = (processed_warnings[0]['start_datetime'].dt.date == date(1998, 4, 26)) # 26
warnings_today_count += rs_today_warnings.sum()

cold_today_warnings = (processed_warnings[1]['start_datetime'].dt.date == date(1999, 12, 19))
warnings_today_count += cold_today_warnings.sum()

all_rs_warnings = []
all_cold_warnings = []

all_rs_warnings = processed_warnings[0][rs_today_warnings]
all_cold_warnings = processed_warnings[1][cold_today_warnings]


warnings_today = go.Figure(go.Indicator(
    mode = 'number',
    value = warnings_today_count,
    title={"text": "Warnings Issued Today"}
))


warnings_today.update_layout(
    margin=dict(l=0.1, r=0.1, t=0.1, b=0.1),
    height=200
)

signals = {'A': 'Amber', 'R': 'Red', 'B': 'Black'}

st.plotly_chart(warnings_today, use_container_width=True)


if not all_rs_warnings.empty and 'warnings' in all_rs_warnings:
    st.write('### Rainstorm')
    alerts_col = st.columns(len(all_rs_warnings['warnings']))
    for idx, signal in enumerate(all_rs_warnings['warnings']):
        with alerts_col[idx]:
            start_date = all_rs_warnings['start_datetime'][idx+1]
            end_date = all_rs_warnings['end_datetime'][idx+1]

            message = f"""### {signals[signal]}
        Start at: {start_date}
    End at: {end_date}
                         """
            if signal == 'R' or signal == 'B':
                st.error(message)
            elif signal == 'A':
                st.warning(message)

if not all_cold_warnings.empty:
    cold_col = st.columns(len(all_cold_warnings))
    for idx, (start_datetime, end_datetime) in enumerate(zip(all_cold_warnings['start_datetime'], all_cold_warnings['end_datetime'])):
        with cold_col[idx]:
            st.write('### Cold')
            st.warning(f"""
            ```
            Start at: {start_datetime}
            End at: {end_datetime}
            ```        """)
