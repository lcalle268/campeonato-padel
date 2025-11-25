# -*- coding: utf-8 -*-
"""
Created on Sat Oct 18 12:14:33 2025
@author: LCALLE
"""

import streamlit as st
import pandas as pd
import altair as alt

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

    # === Normalizar columnas ===
    clasif.columns = clasif.columns.str.strip().str.upper()
    resultados.columns = resultados.columns.str.strip().str.upper()

    # === Filtrar grupo seleccionado ===
    clasif_f = clasif[clasif["GRUPO"].str.lower() == grupo.lower()]
    resultados_f = resultados[
        (resultados["GRUPO"].str.lower() == grupo.lower()) &
        (resultados["VUELTA"].str.lower() == vuelta.lower())
    ]
    # === Calcular progreso de partidos jugados ===
    # Filtrar solo el grupo y vuelta seleccionados
    resultados_f = resultados[
        (resultados["GRUPO"].str.lower() == grupo.lower()) &
        (resultados["VUELTA"].str.lower() == vuelta.lower())
    ]
    
    # Obtener lista de parejas del grupo (para saber cuántos partidos posibles hay)
    parejas_grupo = clasif[clasif["GRUPO"].str.lower() == grupo.lower()]["PAREJA"].nunique()
    
    # Total de partidos posibles (combinaciones sin repetición)
    partidos_totales = int(parejas_grupo * (parejas_grupo - 1) / 2)
    
    # Partidos realmente jugados (con resultado rellenado)
    partidos_jugados = resultados_f["RESULTADO_P1P2"].notna().sum()
    
    # Calcular porcentaje
    porcentaje = (partidos_jugados / partidos_totales) * 100 if partidos_totales > 0 else 0
    
    # === Mostrar barra de progreso ===
    st.markdown(f"### 🏁 Progreso de partidos jugados ({vuelta} - {grupo})")
    st.progress(porcentaje / 100)
    st.write(f"**Partidos jugados:** {partidos_jugados} / {partidos_totales}  →  ({porcentaje:.1f}%) completado")
    
    # === Mostrar mensaje según porcentaje ===
    #if porcentaje < 50:
    #    st.warning(f"⏳ Solo {porcentaje:.1f}% completado")
    #elif porcentaje < 90:
    #    st.info(f"✅ Buen progreso ({porcentaje:.1f}%)")
    #else:
    #    st.success(f"🏆 Vuelta completada ({porcentaje:.1f}%)")


    # === Mostrar tabla de clasificación ===
    st.subheader(f"📊 Clasificación - {grupo}")

    cols = [
        "CLASIFICACION", "PAREJA", "PUNTOS", "P. JUGADOS",
        "P. GANADOS", "P. EMPATADOS", "P. PERDIDOS",
        "SET GANADOS", "SET PERDIDOS"
    ]
    clasif_cols = [c for c in cols if c in clasif_f.columns]

    st.dataframe(clasif_f[clasif_cols], use_container_width=True, hide_index=True)

    # === Crear matriz de resultados ===
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

    # === Comentarios por fecha ===
    informes = {
        "21/10/2025": """
        🗓️ **Informe del 21/10/2025**

        Güenas a tod@s.  
        
        Ya están actualizados los resultados de ayer. 
        
        En el **Mediocre alto**, debut a lo campeón de los campeones, y un empate de los subcampeones sin mucha gloria que les mantiene arriba.  
        
        En el **Mediocre medio**, *Teresa y Leticia* dan un puñetazo en la mesa y afeitan sin espuma a *Las Barbas*, que pasan a ser *Los sin barba*, al menos hasta que les crezca algún pelillo… si lo hacen.
        """,

        "07/11/2025": """
        🗓️ **Informe del 07/11/2025**

        Güenas.  
        En primer lugar, decir que el torneo va avanzando a buen ritmo, así que felicidades por ello.  
        A ver si para antes de Navidad tenemos toda la primera fase acabada.  

        En el **Mediocre alto**, *Los Luises* van líderes sólidos después de infringir la primera derrota en dos años a *Fla-Delicatessen*, que no pasan por su mejor momento (ni en el pádel ni en el Tinder 😅).  
        Destacar también la victoria de *Nuño y Jorge* (los otrora *Truño y Morgue*), que nadie apostaba por ellos, pero siempre dan coletazos — normalmente a los mismos.  

        En el **Mediocre medio**, *Marta y Salva* caminan con paso firme, a la espera de ver la progresión de *Víctor y Tito* (en adelante “el Tito Víctor”), que aún no han perdido un juego, y eso siempre da respeto.  

        En el **Mediocre bajo**, las *hermanas atómicas* no tienen rival y se postulan para el liderato y optar a subir de nivel.  

        En este sentido, se ha cambiado el criterio anterior:  
        - El que **asciende** entrará con los mismos puntos que tenga el 4º del grupo superior (o el 5º en el caso del grupo 2).  
        - El que **baja** heredará los puntos del **segundo** de su nuevo grupo (no del primero como antes).  
        
        Parece lioso, pero después de unas copas lo veréis clarinete.  

        Para finalizar, recordaros que aún hay gente que no ha pagado la cuota del torneo.  
        No vamos a ser como Montoro de sacar el listado de morosos... de momento.  

        _Saludos cordiales desde Alberto Bosch 16, planta sexta, sector B._
        """,

        "25/11/2025": """
        🗓️ **Informe del 25/11/2025**

        Güenas.  
        Quería recordaros que la primera fase debe acabarse antes de las entrañables fiestas,  
        así que hay que ponerse las pilas — sobre todo algunas parejas que han jugado más bien poco.  

        Es clave que los grupos estén sincronizados, puesto que hasta que no se jueguen los partidos de ascensos y descensos se paralizará todo.  
        Si tenéis problemas de agenda, jugad en horario de trabajo: seguro que vuestros jefes os dejan, al menos en esta semana del *Black Friday*.  

        Por lo demás, todo muy bien y muy contentos con el desarrollo del campeonato.  
        Por poner un pero, aún queda alguna pareja sin pagar la cuota 💸.  
        Decid a vuestros jefes (ya de paso) que os suban la productividad si es necesario.  

        _Saludos cordiales desde Jazmín 35 (siempre tengo cerveza en la nevera 🍺)._
        """
    }

    # === Selector de fecha ===
    fecha_sel = st.selectbox("📅 Selecciona el día del informe:", sorted(list(informes.keys()), reverse=True))

    # === Mostrar el texto ===
    st.markdown(informes[fecha_sel])


# =============================
# === PESTAÑA 4: ESTADÍSTICAS
# =============================
elif pagina == "Estadísticas 📊":
    st.header("📊 Estadísticas de las parejas")

    try:
        hist = pd.read_excel("padel.xlsx", sheet_name="historial_partidos")
    except FileNotFoundError:
        st.error("❌ No se encontró la hoja 'historial_partidos' en el archivo 'padel.xlsx'.")
        st.stop()

    # Normalizar
    hist.columns = hist.columns.str.strip().str.upper()
    hist["GRUPO"] = hist["GRUPO"].str.title()

    grupos = hist["GRUPO"].unique().tolist()
    grupo_sel = st.selectbox("Selecciona el grupo:", grupos)
    parejas = hist[hist["GRUPO"] == grupo_sel]["PAREJA"].unique().tolist()
    pareja_sel = st.selectbox("Selecciona una pareja (o 'Todas'):", ["Todas"] + parejas)

    # Filtrar
    if pareja_sel != "Todas":
        df_plot = hist[(hist["GRUPO"] == grupo_sel) & (hist["PAREJA"] == pareja_sel)]
    else:
        df_plot = hist[hist["GRUPO"] == grupo_sel]

    # === Gráfico de evolución de puntos ===
    st.subheader("📈 Evolución de puntos acumulados")

    chart = (
        alt.Chart(df_plot)
        .mark_line(point=True, strokeWidth=3)
        .encode(
            x=alt.X("PARTIDO:Q", title="Número de partido"),
            y=alt.Y("PUNTOS_ACUM:Q", title="Puntos acumulados"),
            color=alt.Color(
                "PAREJA:N",
                legend=alt.Legend(title="Pareja"),
                scale=alt.Scale(scheme="set2")  # 🎨 Paleta de colores suave y diferenciada
            ),
            tooltip=["PAREJA", "RESULTADO", "PUNTOS_ACUM", "PG", "PE", "PP"]
        )
        .properties(height=420, width="container")
        .configure_axis(
            labelFontSize=13,
            titleFontSize=14
        )
        .configure_legend(
            titleFontSize=13,
            labelFontSize=12
        )
    )

    st.altair_chart(chart, use_container_width=True)


    # === Tabla resumen de rendimiento ===
    st.subheader("📋 Rendimiento acumulado")
    resumen = (
        df_plot.groupby("PAREJA")
        .agg({"PG": "max", "PE": "max", "PP": "max", "PUNTOS_ACUM": "max"})
        .reset_index()
        .rename(columns={"PG": "Ganados", "PE": "Empatados", "PP": "Perdidos", "PUNTOS_ACUM": "Puntos Totales"})
    )

    st.dataframe(resumen, use_container_width=True, hide_index=True)


# =============================
# === PESTAÑA 5: CAMPEONATO
# =============================
elif pagina == "Campeonato Final 🏆":
    st.header("🏆 Cuadro final")
    st.info("Aquí se podrá visualizar el cuadro de semifinales y finales🏁.")

  























