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

# === Cargar datos del Excel ===
try:
    df = pd.read_excel("padel.xlsx", sheet_name="clasificación")
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'padel.xlsx'. Súbelo al mismo directorio que este script.")
    st.stop()

# Normalizamos los nombres de columnas por si hay espacios o mayúsculas diferentes
df.columns = df.columns.str.strip().str.upper()

# === Filtrar por grupo ===
df_filtrado = df[df["GRUPO"].str.lower() == grupo.lower()]

if df_filtrado.empty:
    st.warning(f"No hay datos disponibles para el grupo **{grupo}**.")
else:
    # Seleccionamos las columnas deseadas
    columnas = [
        "CLASIFICACION", "PAREJA", "PUNTOS", "P. JUGADOS",
        "P GANADOS", "P EMPATADOS", "P. PERDIDOS",
        "SET GANADOS", "SET PERDIDOS"
    ]

    # Verificamos que todas existan en el Excel
    columnas_validas = [c for c in columnas if c in df_filtrado.columns]
    df_filtrado = df_filtrado[columnas_validas].sort_values("CLASIFICACION")

    st.subheader(f"📊 Clasificación - {grupo} ({vuelta})")
    st.dataframe(df_filtrado, use_container_width=True)

# === Crear plantilla vacía de resultados ===
parejas = df_filtrado["PAREJA"].tolist() if not df_filtrado.empty else []
if parejas:
    resultados = pd.DataFrame(index=parejas, columns=parejas)
    for i in range(len(parejas)):
        for j in range(len(parejas)):
            resultados.iloc[i, j] = "🎾" if i == j else ""
    
    st.subheader(f"🎾 Resultados {vuelta}")
    st.dataframe(resultados, use_container_width=True)