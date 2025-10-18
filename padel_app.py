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

# === Cargar datos ===
try:
    clasif = pd.read_excel("padel.xlsx", sheet_name="clasificacion")
    resultados = pd.read_excel("padel.xlsx", sheet_name="resultados")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'padel.xlsx'.")
    st.stop()

# === Normalizar nombres de columnas ===
clasif.columns = clasif.columns.str.strip().str.upper()
resultados.columns = resultados.columns.str.strip().str.upper()

# === FILTRO POR GRUPO ===
clasif_f = clasif[clasif["GRUPO"].str.lower() == grupo.lower()].sort_values("CLASIFICACION")
resultados_f = resultados[
    (resultados["GRUPO"].str.lower() == grupo.lower()) &
    (resultados["VUELTA"].str.lower() == vuelta.lower())
]

# === Mostrar tabla de clasificación ===
st.subheader(f"📊 Clasificación - {grupo} ({vuelta})")
cols = [
    "CLASIFICACION", "PAREJA", "PUNTOS", "P. JUGADOS",
    "P GANADOS", "P EMPATADOS", "P. PERDIDOS",
    "SET GANADOS", "SET PERDIDOS"
]
clasif_cols = [c for c in cols if c in clasif_f.columns]
st.dataframe(clasif_f[clasif_cols], use_container_width=True)

# === MATRIZ DE RESULTADOS ===
parejas = clasif_f["PAREJA"].tolist()
matriz = pd.DataFrame(index=parejas, columns=parejas)

# Rellenar la matriz con resultados
for _, row in resultados_f.iterrows():
    p1, p2, res = row["PAREJA1"], row["PAREJA2"], row["RESULTADO"]
    if p1 in matriz.index and p2 in matriz.columns:
        matriz.loc[p1, p2] = res
        matriz.loc[p2, p1] = res  # simétrica

# Rellenar diagonales con guiones
for p in parejas:
    matriz.loc[p, p] = "🎾"

st.subheader(f"🎾 Resultados {vuelta}")
st.dataframe(matriz, use_container_width=True)
