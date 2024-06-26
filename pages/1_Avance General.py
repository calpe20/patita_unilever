import streamlit as st
import pandas as pd
import numpy as np
from utils import css, css_1
from datetime import datetime
import calendar


st.set_page_config(
    page_title="Dashboard Unilever",
    page_icon=":bar_chart:",
    layout="wide"
)

st.header("Avance de Ventas General")
df_venta = pd.read_excel("./data/actualizada.xlsx")
df_cuota = pd.read_excel("./data/cuota.xlsx")
df_dias = pd.read_excel("./data/dias.xlsx")
df_dias.columns = ("DIAS PROGRAMADOS", "DIAS TRABAJADOS", "DIAS FALTANTES")

df_avance_vendedor = df_venta.groupby('VendedorNombre')['Total'].sum()

df_avance_cobertur = df_venta.groupby('VendedorNombre')['ClienteCodigo'].nunique()
# st.dataframe(df_cuota)
col1, col2, col4 = st.columns(3)
canales = col1.multiselect('Canales', df_cuota['Canal'].unique())


def filter_vendedor(_canales):
    df_cuota_filtro = df_cuota.copy()

    if len(_canales)>0:
        df_cuota_filtro = df_cuota[df_cuota['Canal'].isin(_canales)]
    return df_cuota_filtro

df_cuota_filtro = filter_vendedor(canales)
df_cuota_filtro = df_cuota_filtro[["VendedorNombre", "VOL ONE UL", "COB ONE UL"]]
df_cuota_filtro = pd.merge(df_cuota_filtro, df_avance_vendedor, on="VendedorNombre", how="inner")
df_cuota_filtro = pd.merge(df_cuota_filtro, df_avance_cobertur, on="VendedorNombre", how="inner")
df_cuota_filtro.columns = ["VendedorNombre", "Cuota S/", "Cuota Cob", "Avance", "Avance PDV"]
df_cuota_filtro["Avance %"] = round(df_cuota_filtro["Avance"]/ df_cuota_filtro["Cuota S/"], 2)*100

df_cuota_filtro["Avance %"] = df_cuota_filtro["Avance %"].replace([np.inf, -np.inf], 0)
df_cuota_filtro['Avance'] = round(df_cuota_filtro["Avance"], 2)
df_cuota_filtro["Cuota S/"] = round(df_cuota_filtro["Cuota S/"], 2)
# Calculosdf_cuota_filtro["Cuota S/"] = round(df_cuota_filtro["Cuota S/"], 2)
df_cuota_filtro["Deberìa"] = round((df_cuota_filtro["Cuota S/"]/df_dias["DIAS PROGRAMADOS"].iloc[0])*df_dias["DIAS TRABAJADOS"].iloc[0], 2)
df_cuota_filtro["Proyección"] = round((df_cuota_filtro["Avance"]/df_dias["DIAS TRABAJADOS"].iloc[0])*df_dias["DIAS PROGRAMADOS"].iloc[0], 2)
df_cuota_filtro["Proy %"] = round((df_cuota_filtro["Proyección"]/df_cuota_filtro["Cuota S/"])*100)
df_cuota_filtro["Proy %"] = df_cuota_filtro["Proy %"].replace([np.inf, -np.inf], 0)
df_cuota_filtro["Faltante"] = np.where(round(df_cuota_filtro["Cuota S/"] - df_cuota_filtro["Avance"], 2) < 0, 0.00, round(df_cuota_filtro["Cuota S/"] - df_cuota_filtro["Avance"], 2))
df_cuota_filtro["Av PDV %"] = round((df_cuota_filtro["Avance PDV"] / df_cuota_filtro["Cuota Cob"]) * 100).replace([np.inf, -np.inf], 0)
#

total_cuota = round(df_cuota_filtro['Cuota S/'].sum())
total_avance = round(df_cuota_filtro['Avance'].sum())
col21, col22 = col2.columns(2)
col21.metric(label="Cuota", value='{:,.0f}'.format(total_cuota))
col22.metric(label="Avance", value='{:,.0f}'.format(total_avance))
col41, col42 = col4.columns(2)
col41.metric(label="Avance %", value='{:,.0f}%'.format(round(total_avance/total_cuota, 2)*100))
col42.metric(label="Recomendado %", value='{:,.0f}%'.format(round(df_dias["DIAS TRABAJADOS"].iloc[0]/df_dias["DIAS PROGRAMADOS"].iloc[0], 2)*100))
df_cuota_filtro = df_cuota_filtro[["VendedorNombre", "Cuota S/", "Avance", "Avance %", "Deberìa", "Proyección", "Proy %", "Faltante", "Cuota Cob", "Avance PDV", "Av PDV %"]]

st.markdown(css, unsafe_allow_html=True)
# st.dataframe(df_cuota_filtro)
df_transposed = df_dias.transpose()

# Renombrar la columna index
df_transposed.index.name = 'Variable'

# Renombrar la columna 0
df_transposed.columns = ['Dias']

total_row = df_cuota_filtro.sum().to_frame().T

total_row.columns = ("Total", "Cuota S/", "Avance", "Avance %", "Deberìa", "Proyección", "Proy %", "Faltante", "Cuota Cob", "Avance PDV", "Av PDV %")
total_row["Total"] = "Total"
total_row.index = ['Total']
df = pd.concat([df_cuota_filtro, total_row])
# df.columns = ("VendedorNombre", "Cuota S/", "Avance", "Avance %", "Deberìa", "Proyección", "Proy %", "Faltante", "Cuota Cob", "Avance PDV", "Av PDV %")
with st.container():
    total_ventas_por_dias = df_cuota_filtro.sum(axis=0)
    # Crear un nuevo DataFrame con los totales de ventas por vendedor
    total_ventas_dias_df = total_ventas_por_dias.rename('Total').to_frame().T
    # total_ventas_dias_df = total_ventas_dias_df.reset_index()
    total_ventas_dias_df["VendedorNombre"] = "Total"
    # Concatenar el DataFrame de totales al DataFrame original
    vendedor_ventas_tot = pd.concat([df_cuota_filtro, total_ventas_dias_df])
    st.write("Avance de Ventas por Vendedor:")
    st.markdown(f'<div class="row"><div class="col-2"><div class="responsive-table">{vendedor_ventas_tot.to_html(index=False)}</div>', unsafe_allow_html=True)
    st.write("---")
    st.write(df_transposed)
    