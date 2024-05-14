import streamlit as st
import pandas as pd
import os


def eliminar(archivo_excel: str):
    # Verificar si el archivo existe antes de intentar eliminarlo
    if os.path.exists(archivo_excel):
        # Eliminar el archivo
        os.remove(archivo_excel)
        print(f"El archivo {archivo_excel} ha sido eliminado.")
    else:
        print(f"El archivo {archivo_excel} no existe.")


@st.cache_data
def load_data(path: str):
    data = pd.read_excel(path)
    return data

def dias_transcurridos():
    from datetime import datetime

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Obtener el número de días en el mes actual
    dias_mes_actual = fecha_actual.day

    # Mostrar el número de días transcurridos en el mes actual
    return dias_mes_actual

import calendar

def contar_domingos(year, month):
    # Obtener el número total de días en el mes y el día de la semana del primer día del mes
    total_dias = calendar.monthrange(year, month)[1]
    primer_dia_semana = calendar.weekday(year, month, 1)  # 0 para lunes, 6 para domingo
    
    # Calcular el número de domingos
    domingos_pasados = (total_dias + primer_dia_semana) // 7
    
    return domingos_pasados