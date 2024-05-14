import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Unilever",
    page_icon=":bar_chart:",
    layout="wide"
)
st.title("Dashboard Unilever")
st.markdown("v1.0.0")
st.write("#Hola")

@st.cache_data
def load_data(path: str):
    data = pd.read_excel("venta detalle unilever al 10052024.xlsx")
    return data

with st.sidebar:
    st.header("Configuracion")
    upload_file = st.file_uploader("Cambiar el archivo")

if upload_file is None:
    st.info("Upload a file througt config", icon="✨")
    st.stop()
df = load_data(upload_file)

with st.expander("Visualizacion previa"):
    st.dataframe(df)