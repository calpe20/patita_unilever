import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Dashboard Unilever",
    page_icon=":bar_chart:",
    layout="wide"
)

st.header("Avance de Ventas General")
df_venta = pd.read_excel("./data/actualizada.xlsx")
df_cuota = pd.read_excel("./data/cuota.xlsx")
df_avance_vendedor = df_venta.groupby('VendedorNombre')['Total'].sum()

df_avance_cobertur = df_venta.groupby('VendedorNombre')['ClienteCodigo'].nunique()
# st.dataframe(df_cuota)
col1, col2, col3, col4 = st.columns(4)
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
df_cuota_filtro["Faltante"] = np.where(round(df_cuota_filtro["Cuota S/"] - df_cuota_filtro["Avance"], 2) < 0, 0.00, round(df_cuota_filtro["Cuota S/"] - df_cuota_filtro["Avance"], 2))
df_cuota_filtro["Avance %"] = df_cuota_filtro["Avance %"].replace([np.inf, -np.inf], 0)
df_cuota_filtro['Avance'] = round(df_cuota_filtro["Avance"], 2)
df_cuota_filtro["Cuota S/"] = round(df_cuota_filtro["Cuota S/"], 2)

total_cuota = round(df_cuota_filtro['Cuota S/'].sum())
total_avance = round(df_cuota_filtro['Avance'].sum())
col2.metric(label="Cuota", value='{:,.0f}'.format(total_cuota))
col3.metric(label="Avance", value='{:,.0f}'.format(total_avance))
col4.metric(label="Avance %", value='{:,.0f}%'.format(round(total_avance/total_cuota, 2)*100))
df_cuota_filtro = df_cuota_filtro[["VendedorNombre", "Cuota S/", "Avance", "Avance %", "Cuota Cob", "Avance PDV"]]

# CSS personalizado para hacer que el DataFrame sea responsivo
css = """
<style>
    .responsive-table {
        width: 100%;
        font-family: verdana;
        font-size: 12px;
    }
    .responsive-table table{
        width: 100%
    }
    .responsive-table table td:nth-child(7){
        text-align: right;
    }
    .responsive-table table td:nth-child(6){
        text-align: center;
    }
    .responsive-table table td:nth-child(5){
        text-align: center;
    }
    .responsive-table table td:nth-child(4){
        text-align: right;
    }
    .responsive-table table td:nth-child(3){
        text-align: right;
    }
    .responsive-table table td:nth-child(2){
        text-align: right;
    }
</style>
"""
st.markdown(css, unsafe_allow_html=True)
# st.dataframe(df_cuota_filtro)
with st.container():
    st.write("Avance de Ventas por Vendedor:")
    st.markdown(f'<div class="row"><div class="col-2"><div class="responsive-table">{df_cuota_filtro.to_html(index=False)}</div>', unsafe_allow_html=True)