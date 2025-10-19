# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 12:14:33 2025

@author: LCALLE
"""

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Campeonato de Pádel", page_icon="🏆", layout="wide")

st.title("🏆 Campeonato de Pádel - SGFAL")

# === Barra lateral de navegación ===
pagina = st.sidebar.radio(
    "Navegación",
    [
        "Clasificación 🏅",
        "Participantes 👥",
        "Informe semanal 🗞️", 
        "Estadísticas 📊",
        "Campeonato Final 🏆"
    ]
)

# =============================
# === PESTAÑA 1: CLASIFICACIÓN
# =============================
if pagina == "Clasificación 🏅":
    st.header("📈 Clasificación por grupo y vuelta")

    col1, col2 = st.columns(2)
    grupo = col1.selectbox("Selecciona el grupo:", ["Mediocre alto", "Mediocre medio", "Mediocre bajo"])
    vuelta = col2.selectbox("Selecciona la vuelta:", ["1ª vuelta", "2ª vuelta"])

    try:
        clasif = pd.read_excel("padel.xlsx", sheet_name="clasificacion")
        resultados = pd.read_excel("padel.xlsx", sheet_name="resultados")
    except FileNotFoundError:
        st.error("❌ No se encontró el archivo 'padel.xlsx'.")
        st.stop()

    clasif.columns = clasif.columns.str.strip().str.upper()
    resultados.columns = resultados.columns.str.strip().str.upper()

    clasif_f = clasif[clasif["GRUPO"].str.lower() == grupo.lower()].sort_values("CLASIFICACION")
    resultados_f = resultados[
        (resultados["GRUPO"].str.lower() == grupo.lower()) &
        (resultados["VUELTA"].str.lower() == vuelta.lower())
    ]

    st.subheader(f"📊 Clasificación - {grupo}")

    cols = [
        "CLASIFICACION", "PAREJA", "PUNTOS", "P. JUGADOS",
        "P GANADOS", "P EMPATADOS", "P. PERDIDOS",
        "SET GANADOS", "SET PERDIDOS"
    ]
    clasif_cols = [c for c in cols if c in clasif_f.columns]

    clasif_f = clasif_f.sort_values(by="CLASIFICACION", ascending=True)
    st.dataframe(clasif_f[clasif_cols], use_container_width=True, hide_index=True)

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

# =============================
# === PESTAÑA 2: PARTICIPANTES
# =============================
elif pagina == "Participantes 👥":
    st.header("👥 Información de los participantes")

    grupo = st.selectbox(
        "Selecciona el grupo:",
        ["Todos", "Mediocre alto", "Mediocre medio", "Mediocre bajo"]
    )

    try:
        participantes = pd.read_excel("padel.xlsx", sheet_name="participantes")
    except FileNotFoundError:
        st.error("❌ No se encontró la hoja 'participantes' en el archivo 'padel.xlsx'.")
        st.stop()

    participantes.columns = participantes.columns.str.strip().str.upper()

    if grupo != "Todos":
        df = participantes[participantes["GRUPO"].str.lower() == grupo.lower()]
    else:
        df = participantes.copy()

    grupos_pareja = df.groupby(["GRUPO", "PAREJA"])

    orden_grupos = ["Mediocre alto", "Mediocre medio", "Mediocre bajo"]

    for grupo_name in orden_grupos:
        parejas_grupo = [(g, p, d) for (g, p), d in grupos_pareja if g.lower() == grupo_name.lower()]
        if not parejas_grupo:
            continue

        st.markdown(f"## 🎾 {grupo_name}")
        for _, pareja_id, data in parejas_grupo:
            st.markdown(f"<div class='grupo-titulo'>Pareja {pareja_id}</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, (_, row) in enumerate(data.iterrows()):
                with cols[i % 2]:
                    st.markdown(
                        f"""
                        <div class='card'>
                            <h4>{row['NOMBRE']}</h4>
                            <p>✉️ {row['CORREO ELECTRONICO']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            st.divider()

# =============================
# === PESTAÑA 3: INFORME SEMANAL
# =============================
elif pagina == "Informe semanal 🗞️":
    st.header("🗞️ Informe semanal del campeonato")
    st.info("Aquí se irán comentando los partidos, tanto los éxitos como los fracasos (en proceso⚙️)")

# =============================
# === PESTAÑA 4: ESTADÍSTICAS
# =============================
elif pagina == "Estadísticas 📊":
    st.header("📊 Estadísticas de las parejas")
    st.info("Aquí se podrán ver gráficos de la evolución de cada pareja (en proceso⚙️)")

# =============================
# === PESTAÑA 5: CAMPEONATO
# =============================
elif pagina == "Campeonato Final 🏆":
    st.header("🏆 Cuadro final")
    st.info("Aquí se podrá visualizar el cuadro de semifinales y finales🏁.")











