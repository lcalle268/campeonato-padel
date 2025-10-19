# =============================
# === ACTUALIZAR CLASIFICACIÓN (AUTO + FINAL)
# =============================

library(readxl)
library(dplyr)
library(stringr)
library(openxlsx)
library(tidyr)

archivo <- "padel.xlsx"

# === 1) Leer resultados ===
resultados <- read_excel(archivo, sheet = "resultados")
names(resultados) <- toupper(str_trim(names(resultados)))

# Normalizar nombres
resultados <- resultados %>%
  mutate(
    GRUPO   = str_squish(GRUPO),
    PAREJA1 = str_squish(PAREJA1),
    PAREJA2 = str_squish(PAREJA2)
  )

# === 2) Función para contar sets ganados/perdidos ===
contar_sets <- function(txt){
  if (is.na(txt) || txt == "") return(c(SG=0, SP=0))
  m <- str_match_all(txt, "(\\d+)[\\-–—](\\d+)")
  m <- m[[1]]
  if (nrow(m) == 0) return(c(SG=0, SP=0))
  a <- as.numeric(m[,2]); b <- as.numeric(m[,3])
  c(SG = sum(a > b, na.rm=TRUE),
    SP = sum(a < b, na.rm=TRUE))
}

# === 3) Construir estadísticas por partido ===
stats <- list()
for (i in seq_len(nrow(resultados))){
  r <- resultados[i,]
  sg1sp1 <- contar_sets(r$RESULTADO_P1P2)
  sg2sp2 <- contar_sets(r$RESULTADO_P2P1)
  
  stats[[length(stats)+1]] <- tibble(
    GRUPO = r$GRUPO, PAREJA = r$PAREJA1,
    PJ = 1,
    PG = as.integer(sg1sp1["SG"] > sg1sp1["SP"]),
    PP = as.integer(sg1sp1["SG"] < sg1sp1["SP"]),
    PE = as.integer(sg1sp1["SG"] == sg1sp1["SP"]),
    SG = unname(sg1sp1["SG"]),
    SP = unname(sg1sp1["SP"]),
    PUNTOS = ifelse(sg1sp1["SG"] > sg1sp1["SP"], 3,
                    ifelse(sg1sp1["SG"] == sg1sp1["SP"], 1, 0))
  )
  
  stats[[length(stats)+1]] <- tibble(
    GRUPO = r$GRUPO, PAREJA = r$PAREJA2,
    PJ = 1,
    PG = as.integer(sg2sp2["SG"] > sg2sp2["SP"]),
    PP = as.integer(sg2sp2["SG"] < sg2sp2["SP"]),
    PE = as.integer(sg2sp2["SG"] == sg2sp2["SP"]),
    SG = unname(sg2sp2["SG"]),
    SP = unname(sg2sp2["SP"]),
    PUNTOS = ifelse(sg2sp2["SG"] > sg2sp2["SP"], 3,
                    ifelse(sg2sp2["SG"] == sg2sp2["SP"], 1, 0))
  )
}

# === 4) Agrupar resultados y calcular totales ===
clasificacion_auto <- bind_rows(stats) %>%
  mutate(
    GRUPO = tolower(str_squish(GRUPO)),
    PAREJA = str_squish(PAREJA)
  ) %>%
  group_by(GRUPO, PAREJA) %>%
  summarise(
    PJ = sum(PJ),
    PG = sum(PG),
    PP = sum(PP),
    PE = sum(PE),
    SG = sum(SG),
    SP = sum(SP),
    PUNTOS = sum(PUNTOS),
    .groups = "drop"
  )

# === Ranking dentro de cada grupo (sin empates) ===
clasificacion_auto <- clasificacion_auto %>%
  mutate(DIF_SETS = SG - SP) %>%
  arrange(GRUPO, desc(PUNTOS), desc(PG), desc(DIF_SETS), SP, PAREJA) %>%
  group_by(GRUPO) %>%
  mutate(CLASIFICACION = row_number()) %>%
  ungroup() %>%
  select(GRUPO, CLASIFICACION, PAREJA, PUNTOS, PJ, PG, PE, PP, SG, SP)

# === 5) Añadir parejas que no han jugado (de 'clasificacion') ===
if ("clasificacion" %in% excel_sheets(archivo)) {
  clasif_base <- read_excel(archivo, sheet = "clasificacion")
  names(clasif_base) <- toupper(str_trim(names(clasif_base)))
  
  clasif_base <- clasif_base %>%
    mutate(
      GRUPO = tolower(str_squish(GRUPO)),
      PAREJA = str_squish(PAREJA)
    )
  
  if (!"CLASIFICACION" %in% names(clasif_base)){
    clasif_base <- mutate(clasif_base, CLASIFICACION = NA_integer_)
  }
  
  clasif_base_min <- clasif_base %>% select(GRUPO, PAREJA, CLASIFICACION)
  
  clasificacion_auto <- clasif_base_min %>%
    left_join(clasificacion_auto, by = c("GRUPO","PAREJA")) %>%
    mutate(
      CLASIFICACION = coalesce(CLASIFICACION.y, CLASIFICACION.x),
      PUNTOS = coalesce(PUNTOS, 0),
      PJ = coalesce(PJ, 0),
      PG = coalesce(PG, 0),
      PE = coalesce(PE, 0),
      PP = coalesce(PP, 0),
      SG = coalesce(SG, 0),
      SP = coalesce(SP, 0)
    ) %>%
    select(GRUPO, CLASIFICACION, PAREJA, PUNTOS, PJ, PG, PE, PP, SG, SP) %>%
    arrange(GRUPO, CLASIFICACION, PAREJA)
}

# === 6) Guardar resultados en Excel ===
wb <- loadWorkbook(archivo)

if ("clasificacion_auto" %in% names(wb)) removeWorksheet(wb, "clasificacion_auto")
addWorksheet(wb, "clasificacion_auto")
writeData(wb, "clasificacion_auto", clasificacion_auto)

# === Clasificación “bonita” para Streamlit ===
clasificacion_final <- clasificacion_auto %>%
  # Volver a poner los nombres de grupo en el formato exacto
  mutate(
    GRUPO = case_when(
      GRUPO == "mediocre alto" ~ "Mediocre alto",
      GRUPO == "mediocre medio" ~ "Mediocre medio",
      GRUPO == "mediocre bajo" ~ "Mediocre bajo",
      TRUE ~ str_to_sentence(GRUPO)
    ),
    # 👇 Aquí definimos el orden 
    GRUPO = factor(
      GRUPO,
      levels = c("Mediocre alto", "Mediocre medio", "Mediocre bajo")
    )
  ) %>%
  arrange(GRUPO, CLASIFICACION) %>%  # respeta el orden definido arriba
  rename(
    `P. JUGADOS` = PJ,
    `P GANADOS` = PG,
    `P EMPATADOS` = PE,
    `P. PERDIDOS` = PP,
    `SET GANADOS` = SG,
    `SET PERDIDOS` = SP
  ) %>%
  select(
    GRUPO, CLASIFICACION, PAREJA, PUNTOS,
    `P. JUGADOS`, `P GANADOS`, `P EMPATADOS`,
    `P. PERDIDOS`, `SET GANADOS`, `SET PERDIDOS`
  )

# === Escribir hoja “clasificacion” ===
if ("clasificacion" %in% names(wb)) removeWorksheet(wb, "clasificacion")
addWorksheet(wb, "clasificacion")
writeData(wb, "clasificacion", clasificacion_final)

saveWorkbook(wb, archivo, overwrite = TRUE)

cat("✅ Clasificación generada correctamente (hojas 'clasificacion_auto' y 'clasificacion')\n")
