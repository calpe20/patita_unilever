import pandas as pd
import streamlit as st
from funtions import load_data

df = load_data("./data/actualizada.xlsx")
st.dataframe(df)