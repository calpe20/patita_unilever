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
st.title("Los Tigres de la Limpieza")

# Cargamos la data historica
df_data = pd.read_excel("./data/data_historico.xlsx")
df_mayo = pd.read_excel("./data/actualizada.xlsx")
df_mayo = df_mayo[["VendedorCodigo","VendedorNombre", "ProveedorCodigo", "ProveedorNombre", "NumPedido",
                   "Canal", "NumDocumento", "ClienteCodigo", "ClienteNombre", "Grupo", "CodFamilia",
                   "Familia", "ProductoCodigo", "ProductoDescripcion", "AbreviacionUnidadReferencia",
                   "Cantidad", "ValorVenta", "Total", "Fecha", "DocIdentidad", "DireccionEntrega", 
                   "Bonificacion", "Linea", "Categoria", "Marca", "Comision", "Peso", "CteCategoria",
                   "CantidadUMES", "Departamento", "Provincia", "Distrito"]]

df_data = pd.concat([df_data, df_mayo], axis=0)

df_data["PERIODO"] = df_data["Fecha"].dt.year.astype(str) + df_data["Fecha"].dt.month.astype(str).str.zfill(2)

df_vendedores = pd.DataFrame(list(df_data['VendedorNombre'].unique()))
df_vendedores.columns = ["VendedorNombre"]
df_productos = df_data[df_data["ProductoDescripcion"].str.contains("CIF")]
df_productos = pd.DataFrame(list(df_productos["ProductoDescripcion"].unique()))
df_productos.columns = ["ProductoDescripcion"]
df_ventas_cif = df_data[df_data["ProductoDescripcion"].isin(df_productos["ProductoDescripcion"])]

df_ventas_cif_grupo = df_ventas_cif.groupby(["VendedorNombre", "PERIODO"])["Total"].sum().reset_index()

df_ventas = df_ventas_cif_grupo.pivot_table(index="VendedorNombre", columns="PERIODO", values="Total", fill_value=0).reset_index()

df_ventas["Promedio Q1"] = round((df_ventas["202401"] + df_ventas["202402"] + df_ventas["202403"])/3,2)
# df_ventas["Promedio Q2"] = (df_ventas["202404"] + df_ventas["202405"] + df_ventas["202403"])/2
df_ventas["202401"] = round(df_ventas["202401"],2)
df_ventas["202402"] = round(df_ventas["202402"],2)
df_ventas["202403"] = round(df_ventas["202403"],2)
df_ventas["202404"] = round(df_ventas["202404"],2)
df_ventas["202405"] = round(df_ventas["202405"],2)
df_ventas["202406"] = round(0,2)
df_ventas["Promedio Q2"] = round((df_ventas["202404"] + df_ventas["202405"] + df_ventas["202406"])/3,2)
df_ventas["CIUDAD"] = "PUCALLPA"
df_ventas = df_ventas[["CIUDAD","VendedorNombre","202401","202402","202403","Promedio Q1","202404","202405","202406","Promedio Q2"]]
df_ventas.columns = ["CIUDAD","VENDEDOR","202401","202402","202403","PROMEDIO Q1","202404","202405","202406","PROMEDIO Q2"]

df_ventas.to_excel("./data/CLUB TIGRES DE LA LIMPIEZA CIF - PUCALLPA.xlsx", index=False)
st.dataframe(df_ventas)
