import streamlit as st
import pandas as pd
from funtions import eliminar

st.set_page_config(
    page_title="Dashboard Unilever",
    page_icon=":bar_chart:",
    layout="wide"
)

def load_data(path: str):
    data = pd.read_excel(path)
    eliminar("./data/actualizada.xlsx")
    data.to_excel("./data/actualizada.xlsx")
    return data

st.header("Actualizar Data")
upload_file = st.file_uploader("Cambiar el archivo excel")

if upload_file is None:
    st.info("Subir un archivo para actualizar la data principal", icon="✨")
    st.stop()

df = load_data(upload_file)

#with st.expander("Visualizacion previa"):
#    st.dataframe(df)