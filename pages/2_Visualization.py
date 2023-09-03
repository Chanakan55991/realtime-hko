import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
from datetime import date
sys.path.append('..')

from utils import *

st.set_page_config(layout='wide')

dfs = process_data(prepare_data())

left, right = st.columns(2)

with left:
    year_counts = dfs[0]['start_datetime'].dt.year.value_counts().reset_index().sort_values(by='start_datetime')
        
    fig = px.line(year_counts, x="start_datetime", y="count", title=f'Count of Warnings issued for Rainstorm')
    st.plotly_chart(fig, use_container_width=True)

with right:
    today = date.today().year
    last_year = date.today().year - 1

    year_counts = dfs[0].query('start_datetime.dt.year == @today')['start_datetime'].dt.year.value_counts()
    last_year_counts = dfs[0].query('start_datetime.dt.year == @last_year')['start_datetime'].dt.year.value_counts()

    total_rs_warnings = go.Figure(go.Indicator(
        mode = 'number+delta',
        value = year_counts.sum(),
        delta = {'position': 'top', 'reference': last_year_counts.sum(), 'increasing.color': '#FF6961', 'decreasing.color': '#77DD77'},
        title={"text": "Total Rainstorm Warnings Issued This Year"}
    ))

    total_rs_warnings.update_layout(
        height=400
    )

    st.plotly_chart(total_rs_warnings, use_container_width=True)


left, right = st.columns(2)

year_counts = dfs[0].groupby([dfs[0]['start_datetime'].dt.year, 'warnings']).size().reset_index(name='count')
year_counts['warnings'] = year_counts['warnings'].replace({'R': 'Red', 'A': 'Amber', 'B': 'Black'})
    
fig = px.bar(year_counts, x='start_datetime', y='count', color='warnings', title='Total Rainstorm Warnings Issues by type each year')
st.plotly_chart(fig, use_container_width=True)
