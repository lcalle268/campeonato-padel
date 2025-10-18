# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 13:13:11 2025

@author: LCALLE
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Campeonato de Pádel", layout="wide")
st.title("🏆 Campeonato de Pádel - SGFAL")

# Leer los datos desde el Excel
partidos = pd.read_excel("padel.xlsx", sheet_name="partidos")
clasificacion = pd.read_excel("padel.xlsx", sheet_name="clasificacion")

# Selección de categoría
categoria = st.selectbox("Selecciona categoría:", partidos["categoria"].unique())

# Mostrar resultados
st.subheader("Resultados")
st.dataframe(partidos[partidos["categoria"] == categoria])

# Mostrar clasificación
st.subheader("Clasificación")
clasif_filtrada = clasificacion[clasificacion["categoria"] == categoria].sort_values(
    by="puntos", ascending=False
)
st.dataframe(clasif_filtrada)