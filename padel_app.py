# -*- coding: utf-8 -*-
"""
Created on Fri Oct 17 13:13:11 2025

@author: LCALLE
"""

import streamlit as st
import pandas as pd

st.title("🏆 Campeonato de Pádel - Oficina")

# Leer los datos
partidos = pd.read_excel("padel.xlsx", sheet_name="partidos")
clasificacion = pd.read_excel("padel.xlsx", sheet_name="clasificacion")

# Seleccionar categoría
categoria = st.selectbox("Selecciona categoría:", partidos["categoria"].unique())

# Filtrar y mostrar
st.subheader("Resultados")
st.dataframe(partidos[partidos["categoria"] == categoria])

st.subheader("Clasificación")
st.dataframe(clasificacion[clasificacion["categoria"] == categoria])
