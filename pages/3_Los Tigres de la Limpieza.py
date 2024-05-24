import streamlit as st
import pandas as pd
# import altair as alt
# import plotly.express as px
from utils import css
from datetime import datetime
from deep_translator import GoogleTranslator

traductor = GoogleTranslator(source='en', target='es')

import calendar

st.set_page_config(
    page_title="Patitia - Unilever | Los Tigres de la Limpieza",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("Los tigres de la Limpieza")