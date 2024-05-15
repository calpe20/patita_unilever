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
    page_title="Avance por Vendedor",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.title("Avance por Vendedor")

df = pd.read_excel("./data/actualizada.xlsx")
df_cuota = pd.read_excel("./data/cuota.xlsx")
col1, col2, = st.columns(2)
vendedores = col2.multiselect('Vendedores', sorted(df['VendedorNombre'].unique()))
canales = col1.multiselect('Canal', sorted(df_cuota['Canal'].unique()))


# Suponiendo que df es tu DataFrame y ya has leído los datos
# Obtener el nombre del día de la semana en español para todas las fechas en la columna "Fecha"
df["NombreDia"] = df["Fecha"].dt.strftime("%A")

# Mapear los nombres de los días de la semana en español
nombres_dias_espanol = {'Friday': 'Viernes', 'Tuesday': 'Martes', 'Monday': 'Lunes', 'Thursday': 'Jueves', 'Wednesday': 'Miércoles', 'Saturday': 'Sábado'}
df["NombreDia"] = df["NombreDia"].map(nombres_dias_espanol)

# Ordenar el DataFrame por el día de la semana
df = df.sort_values(by="NombreDia")

# Eliminar la columna auxiliar de representación numérica del día de la semana
# df = df.drop(columns=["NombreDia"])

if len(canales) > 0:
    vendedor_canal = df_cuota[df_cuota["Canal"].isin(canales)]
else:
    vendedor_canal = df_cuota

def filter_vendedor(df, vendedores):
    df_copy = df.copy()

    if len(vendedores)>0:
        df_copy = df_copy[df_copy['VendedorNombre'].isin(vendedores)]
    return df_copy

df_new = filter_vendedor(df, vendedores)
df_new = df_new[df_new["VendedorNombre"].isin(vendedor_canal["VendedorNombre"])]

df_new['Fecha'] = df_new['Fecha'].dt.strftime('%Y-%m-%d')
vendedor_clientes = df_new.groupby(["VendedorNombre", "Fecha"])["ClienteCodigo"].nunique()
vendedor_ventas = df_new.groupby(["VendedorNombre", "Fecha"])["Total"].sum()
vendedor_dias = df_new.groupby(["VendedorNombre", "NombreDia"])["Total"].sum()
## vendedor_ventas["Total"] = round(vendedor_ventas["Total"], 2)
vendedor_ventas = vendedor_ventas.unstack(fill_value=0)
vendedor_clientes = vendedor_clientes.unstack(fill_value=0)
vendedor_dias = vendedor_dias.unstack(fill_value=0)
# Inserta el CSS personalizado
with st.expander("**Promedio Ventas: Vendedor por día de Semana**"):
    st.markdown(css, unsafe_allow_html=True)
    # Calcular totales de ventas por vendedor
    total_ventas_por_dias = vendedor_dias.sum(axis=0)
    # Crear un nuevo DataFrame con los totales de ventas por vendedor
    total_ventas_dias_df = total_ventas_por_dias.rename('Total').to_frame().T
    # Concatenar el DataFrame de totales al DataFrame original
    vendedor_ventas_tot = pd.concat([vendedor_dias, total_ventas_dias_df])
    st.dataframe(vendedor_ventas_tot)
    st.line_chart(vendedor_dias.T)

#######
# Calcular totales de ventas por vendedor
total_ventas_por_clientes = vendedor_clientes.sum(axis=0)
# Crear un nuevo DataFrame con los totales de ventas por vendedor
total_ventas_df = total_ventas_por_clientes.rename('Total').to_frame().T
# Concatenar el DataFrame de totales al DataFrame original
vendedor_clientes_to = pd.concat([vendedor_clientes, total_ventas_df])

with st.expander("**Avance de Ventas: Efectividad diaria PDV**"):
    st.dataframe(vendedor_clientes_to)
    st.line_chart(vendedor_clientes.T, use_container_width=True)
#######
# Calcular totales de ventas por vendedor
total_ventas_por_vendedor = vendedor_ventas.sum(axis=0)
# Crear un nuevo DataFrame con los totales de ventas por vendedor
total_ventas_df = total_ventas_por_vendedor.rename('Total').to_frame().T
# Concatenar el DataFrame de totales al DataFrame original
vendedor_ventas_tot = pd.concat([vendedor_ventas, total_ventas_df])
# Mostrar el DataFrame actualizado con los totales
with st.expander("**Avance de Ventas: Efectividad diaria Soles**"):
    st.dataframe(vendedor_ventas_tot)
    #######
    st.line_chart(vendedor_ventas.T, use_container_width=True)


with st.expander("**Otros Detalles en Construcciòn**"):

    df_group = df_new.groupby('VendedorNombre')['Total'].sum()
    df_clien = df_new.groupby(['ClienteNombre'])['Total'].sum()
    col1, col2 = st.columns(2)
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
        .responsive-table table td:nth-child(2){
            text-align: right;
        }
    </style>
    """

    # Insertar CSS personalizado
    st.markdown(css, unsafe_allow_html=True)
    df_clien = df_clien.reset_index()
    df_clien['Total'] = round(df_clien['Total'],2)
    df_group = df_group.reset_index()
    df_group['Total'] = round(df_group['Total'],2)
    # Mostrar el DataFrame en un contenedor HTML personalizado para hacerlo responsivo
    col1, col2 = st.columns(2)
    with st.container():
        col1.write("Ventas por Vendedor:")
        col1.markdown(f'<div class="responsive-table">{df_group.to_html(index=False)}</div>', unsafe_allow_html=True)

        col2.write("Ventas Vendedor/Clientes:")
        col2.markdown(f'<div class="responsive-table">{df_clien.to_html(index=False)}</div>', unsafe_allow_html=True)