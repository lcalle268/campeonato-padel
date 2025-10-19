# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 12:14:33 2025

@author: LCALLE
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Campeonato de Pádel", page_icon="🏆", layout="wide")

st.title("🏆 Campeonato de Pádel - SGFAL")

# === Barra de navegación principal ===
pagina = st.sidebar.radio(
    "Navegación",
    [
        "Clasificación 🏅",
        "Participantes 👥",
        "Estadísticas 📊",
        "Campeonato Final 🏆"
    ]
)

# === PESTAÑA 1: CLASIFICACIÓN ===
if pagina == "Clasificación 🏅":
    st.header("📈 Clasificación por grupo y vuelta")

    # Selección de grupo y vuelta
    col1, col2 = st.columns(2)
    grupo = col1.selectbox("Selecciona el grupo:", ["Mediocre alto", "Mediocre medio", "Mediocre bajo"])
    vuelta = col2.selectbox("Selecciona la vuelta:", ["1ª vuelta", "2ª vuelta"])

    # Cargar datos
    try:
        clasif = pd.read_excel("padel.xlsx", sheet_name="clasificacion")
        resultados = pd.read_excel("padel.xlsx", sheet_name="resultados")
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'padel.xlsx'.")
        st.stop()

    # Normalizar nombres
    clasif.columns = clasif.columns.str.strip().str.upper()
    resultados.columns = resultados.columns.str.strip().str.upper()

    # Filtrar por selección
    clasif_f = clasif[clasif["GRUPO"].str.lower() == grupo.lower()].sort_values("CLASIFICACION")
    resultados_f = resultados[
        (resultados["GRUPO"].str.lower() == grupo.lower()) &
        (resultados["VUELTA"].str.lower() == vuelta.lower())
    ]

    # Mostrar tabla de clasificación
    st.subheader(f"📊 Clasificación - {grupo}")

    cols = [
        "CLASIFICACION", "PAREJA", "PUNTOS", "P. JUGADOS",
        "P GANADOS", "P EMPATADOS", "P. PERDIDOS",
        "SET GANADOS", "SET PERDIDOS"
    ]
    clasif_cols = [c for c in cols if c in clasif_f.columns]

    clasif_f = clasif_f.sort_values(by="CLASIFICACION", ascending=True)
    st.dataframe(clasif_f[clasif_cols], use_container_width=True, hide_index=True)

    # Crear matriz de resultados
    parejas = clasif_f["PAREJA"].tolist()
    matriz = pd.DataFrame(index=parejas, columns=parejas)

    for _, row in resultados_f.iterrows():
        p1, p2 = row["PAREJA1"], row["PAREJA2"]
        r12 = row.get("RESULTADO_P1P2", "")
        r21 = row.get("RESULTADO_P2P1", "")

        if p1 in matriz.index and p2 in matriz.columns:
            matriz.loc[p1, p2] = r12
        if p2 in matriz.index and p1 in matriz.columns:
            matriz.loc[p2, p1] = r21

    for p in parejas:
        matriz.loc[p, p] = "🎾"

    st.subheader(f"🎾 Resultados {vuelta}")
    st.dataframe(matriz, use_container_width=True)

# === PESTAÑA 2: PARTICIPANTES ===
elif pagina == "Participantes 👥":
    st.header("👥 Información de los participantes")
    st.info("Aquí podrás mostrar fotos, nombres y detalles de las parejas.")

# === PESTAÑA 3: ESTADÍSTICAS ===
elif pagina == "Estadísticas 📊":
    st.header("📊 Estadísticas de las parejas")
    st.info("En esta sección podrás añadir gráficos y comparativas entre parejas.")

# === PESTAÑA 4: CAMPEONATO FINAL ===
elif pagina == "Campeonato Final 🏆":
    st.header("🏆 Cuadro final")
    st.info("Aquí se podrá visualizar el cuadro de semifinales y finales.")


