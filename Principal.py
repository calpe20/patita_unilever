import streamlit as st
import pandas as pd
from funtions import load_data, dias_transcurridos, contar_domingos
import altair as alt

st.set_page_config(
    page_title="Dashboard Unilever",
    page_icon=":bar_chart:",
    layout="wide"
)
#st.title("Unilever")
#st.markdown("v1.0.0")



# df = load_data("./venta detalle unilever al 10052024.xlsx")
df = pd.read_excel("./data/actualizada.xlsx")
df_cuota = pd.read_excel("./data/cuota.xlsx")

df_totales = df.groupby('VendedorNombre')['Total'].sum()
df['Fecha'] = df['Fecha'].dt.strftime('%Y-%m-%d')

df_dias_totales_ = df.groupby('Fecha')['Total'].sum() 
df_dias_totales = df_dias_totales_.reset_index()
df_dias_totales = df_dias_totales.pivot_table(index=None, columns='Fecha', values='Total')

df_total_cuota = df_cuota['VOL ONE UL'].sum()
df_total = df['Total'].sum()
df_dias_totales['Totales'] = df_total
# Ejemplo de uso
año = 2024
mes = 5  # Mayo
dias = dias_transcurridos()

col1, col2, col3, col4, col5, col6 = st.columns(6)
diaspro = col1.number_input("Dias Programados :", min_value=1, max_value=26, value=26)
diastra = col2.number_input("Dias Trabajados :", min_value=1, max_value=26, value=dias)
diasfal = diaspro - diastra
avance = round((df_total/df_total_cuota)*100)
proyeccion = round((df_total/diastra)*diaspro, 2)
proyeccpor = round((proyeccion / df_total_cuota)*100,2)
cta_mercad = round((diastra / diaspro)*100,2)
col3.metric(label="Días Faltante", value=diasfal)
col6.metric(label="Deficit", value='{:,.0f}%'.format(avance - cta_mercad))
st.write('**Indicadores Generales**')
col1, col2, col3, col4, col5, col6 = st.columns(6)
st.write('---')
# diaspro = col1.number_input("Dias Programados", min_value=1, max_value=26, value=26)
col1.metric(label="Cuota Periodo", value='{:,.2f}'.format(df_total_cuota))
col2.metric(label="Venta Total", value='{:,.2f}'.format(df_total))
col3.metric(label="Proyeccion", value='{:,.2f}'.format(proyeccion))
col4.metric(label="Avance", value='{:,.0f}%'.format(avance))
col5.metric(label="Proyeccion %", value='{:,.0f}'.format(proyeccpor))
col6.metric(label="Cta Mercado", value='{:,.0f}%'.format(cta_mercad))
#col1.title('{:,.2f}'.format(df_total))
col1, col2, col3, col4 = st.columns(4)

# Crear el DataFrame
df_avance = [['Cuota', df_total_cuota], ['Avance', df_total]]
df_avance = pd.DataFrame(df_avance, columns=['Indicador', 'Monto'])

# Establecer la columna 'Indicador' como el índice
df_avance.set_index('Indicador', inplace=True)

# Tratar de trazar un gráfico de barras usando Altair con etiquetas encima de cada barra
st.dataframe(df_dias_totales)
st.line_chart(df_dias_totales_)
col1.bar_chart(df_avance, width=10)
st.write('**Ventas por Vendedor**')
st.bar_chart(df_totales, height=500)
