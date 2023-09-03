import streamlit as st
import sys
sys.path.append('..')

from utils import *


dfs = process_data(prepare_data())

names = ['Rainstorm', 'Cold']

for idx, df in enumerate(dfs):
    st.markdown(f"### {names[idx]}")
    df
