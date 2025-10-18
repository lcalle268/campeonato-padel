# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 12:14:33 2025

@author: LCALLE
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Campeonato de Pádel", page_icon="🏆", layout="wide")

st.title("🏆 Campeonato de Pádel - SGFAL")

# === Selección de grupo y vuelta ===
col1, col2 = st.columns(2)
grupo = col1.selectbox("Selecciona el grupo:", ["Mediocre alto", "Mediocre medio", "Mediocre bajo"])
vuelta = col2.selectbox("Selecciona la vuelta:", ["1ª vuelta", "2ª vuelta"])

# === Cargar datos según selección ===
# Puedes reemplazar esto con la lectura desde un Excel si tienes varias hojas
# Ejemplo: pd.read_excel("padel.xlsx", sheet_name=f"{grupo}_{vuelta}")
# Por ahora creamos datos de ejemplo:

parejas = [
    "Teresa-Leticia", "las barbas", "Alba-Luis",
    "Vicente-Victor", "Salvador-Marta", "Alberto-Esperanza"
]

clasificacion = pd.DataFrame({
    "CLASIFICACION": range(1, len(parejas) + 1),
    "PAREJA": parejas,
    "PUNTOS": [0]*6,
    "P. JUGADOS": [0]*6,
    "P. GANADOS": [0]*6,
    "P. EMPATADOS": [0]*6,
    "P. PERDIDOS": [0]*6,
    "SET GANADOS": [0]*6,
    "SET PERDIDOS": [0]*6
})

st.subheader(f"📊 Clasificación - {grupo} ({vuelta})")
st.dataframe(clasificacion, use_container_width=True)

# === Crear matriz de resultados ===
resultados = pd.DataFrame(index=parejas, columns=parejas)
for i in range(len(parejas)):
    for j in range(len(parejas)):
        if i == j:
            resultados.iloc[i, j] = "-"
        else:
            resultados.iloc[i, j] = ""

st.subheader(f"🎾 Resultados {vuelta}")
st.dataframe(resultados, use_container_width=True)