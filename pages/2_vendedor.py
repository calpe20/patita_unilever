import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Avance por Vendedor",
    page_icon=":bar_chart:",
    layout="wide"
)
st.title("Avance por Vendedor")

df = pd.read_excel("./data/actualizada.xlsx")
df_cuota = pd.read_excel("./data/cuota.xlsx")

vendedores = st.multiselect('Vendedores', sorted(df['VendedorNombre'].unique()))

def filter_vendedor(df, vendedores):
    df_copy = df.copy()

    if len(vendedores)>0:
        df_copy = df_copy[df_copy['VendedorNombre'].isin(vendedores)]
    return df_copy
# Define el estilo CSS para la celda que abarca varias columnas
css = """
<style>
    .colspan-cell {
        grid-column: span 2; /* Esta clase abarcará dos columnas */
    }
</style>
"""

# Inserta el CSS personalizado
st.markdown(css, unsafe_allow_html=True)

df_new = filter_vendedor(df, vendedores)
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
    col1.markdown(f'<div class="row"><div class="col-2"><div class="responsive-table">{df_group.to_html(index=False)}</div>', unsafe_allow_html=True)

    col2.write("Ventas Vendedor/Clientes:")
    col2.markdown(f'<div class="row"><div class="col-8"><div class="responsive-table">{df_clien.to_html(index=False)}</div>', unsafe_allow_html=True)